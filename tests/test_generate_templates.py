"""Tests for generate_templates.py. Run: python tests/test_generate_templates.py

The generator reads the plugin's own `defaults/types.json` — there is no
per-project config path and no `--config` argument. These tests therefore
assert against the shipped roster itself, which is the single source of
truth for worldbuilder's types and status tags.
"""
import json
import re
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, 'scripts', 'generate_templates.py')
TYPES_JSON = os.path.join(ROOT, 'defaults', 'types.json')
TEMPLATE_DIR = os.path.join(ROOT, 'defaults', 'templates')


def load_roster():
    with open(TYPES_JSON, encoding='utf-8') as f:
        return json.load(f)


class RosterTests(unittest.TestCase):
    """The plugin-internal roster is the config source: pin the members
    generate_templates.py consumes."""

    def setUp(self):
        self.roster = load_roster()

    def test_roster_has_types_and_tags_only(self):
        self.assertEqual(set(self.roster), {'types', 'tags'})
        # enforced_paths is retired with the registry — scope is scraibe's
        # reserved-space exclusion rule now, not a per-project path list.
        self.assertNotIn('enforced_paths', self.roster)

    def test_every_type_carries_a_fields_map(self):
        for name, spec in self.roster['types'].items():
            self.assertIsInstance(spec.get('fields'), dict,
                                  f'{name} has no fields map')

    # Every type's fields map and template_file association, exactly as
    # the retired okf.base.json carried them. The seam's contract is that
    # nothing generate_templates.py consumes changed in the move, so all
    # ten types are pinned — not a sample.
    EXPECTED = {
        'character': ({'factions': {'type': 'list'},
                       'sex': {'type': 'text'}}, 'character.md'),
        'location': ({'region': {'type': 'text'},
                      'function': {'type': 'text'},
                      'primary-characters': {'type': 'list'}}, 'location.md'),
        'faction': ({'members': {'type': 'list'},
                     'function': {'type': 'text'}}, 'faction.md'),
        'event': ({'characters': {'type': 'list'},
                   'location': {'type': 'text'},
                   'layer': {'type': 'text'}}, 'event.md'),
        'concept': ({'layer': {'type': 'text', 'required': True},
                     'trigger-context': {'type': 'text'},
                     'keywords': {'type': 'list', 'required': False}},
                    'concept.md'),
        'story': ({'scope': {'type': 'text', 'required': True},
                   'up': {'type': 'text'}}, 'story.md'),
        'foundation': ({}, 'foundation.md'),
        'plan': ({}, 'plan.md'),
        'direction': ({}, None),
        'reference': ({}, None),
    }

    def test_field_maps_preserved_from_the_registry(self):
        types = self.roster['types']
        self.assertEqual(set(types), set(self.EXPECTED),
                         'roster type set changed')
        for name, (fields, _) in self.EXPECTED.items():
            self.assertEqual(types[name]['fields'], fields,
                             f'{name}: fields map changed')

    def test_template_file_associations_preserved(self):
        types = self.roster['types']
        for name, (_, ref) in self.EXPECTED.items():
            self.assertEqual(types[name].get('template_file'), ref,
                             f'{name}: template_file association changed')

    def test_template_file_references_resolve(self):
        refs = 0
        for name, spec in self.roster['types'].items():
            ref = spec.get('template_file')
            if ref is None:
                # A type may ship an inline empty body instead.
                self.assertEqual(spec.get('template', ''), '',
                                 f'{name}: inline body but no template_file')
                continue
            refs += 1
            self.assertTrue(os.path.isfile(os.path.join(TEMPLATE_DIR, ref)),
                            f'{name}: missing template file {ref}')
        self.assertGreater(refs, 0)

    def test_status_tag_vocabulary_preserved(self):
        status = self.roster['tags']['status']
        self.assertEqual(status['values'],
                         ['complete', 'deprecated', 'abandoned', 'archived'])
        self.assertNotIn('open', status)
        self.assertNotIn('closed', status)


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def run_gen(self, *args):
        return subprocess.run(
            [sys.executable, SCRIPT, '--out', self.dir, *args],
            capture_output=True, text=True)

    def read(self, rel):
        with open(os.path.join(self.dir, rel), encoding='utf-8') as f:
            return f.read()

    def test_no_config_argument(self):
        """The per-project config path is gone: --config is not accepted."""
        r = self.run_gen('--config', os.path.join(self.dir, 'okf.json'))
        self.assertEqual(r.returncode, 2)
        self.assertIn('--config', r.stderr)

    def test_type_template_skeleton(self):
        r = self.run_gen('--dir', 'notes/=character,event')
        self.assertEqual(r.returncode, 0, r.stderr)
        t = self.read('_templates/type-character.md')
        self.assertIn('type: character', t)
        self.assertIn('title: <% tp.file.title %>', t)
        self.assertIn(chr(10) + 'tags: []' + chr(10), t)           # born open: no closure tag
        # The birth date is `created`, a date-LINK; `modified` is left to
        # the frontmatter-modified-date plugin, so no template stamps it.
        self.assertIn('created: "[[<% moment.utc().format("YYYY-MM-DD") %>]]"', t)
        self.assertNotIn('timestamp:', t)
        self.assertNotIn('\ndate:', t)
        self.assertIn('sex: ""', t)               # text field -> ""
        self.assertIn('factions: []', t)           # list field -> []
        self.assertNotIn('aliases', t)             # optional universal skipped
        self.assertNotIn('human-ready', t)

    def test_template_file_body_is_embedded(self):
        """The compilation contract absorbed from build-okf.py: a type's
        `template_file` body reaches the generated Templater template.

        Covers every type carrying a reference, so a swapped or wrong
        reference fails here and not only in the roster assertions."""
        roster = load_roster()['types']
        refs = {n: s['template_file'] for n, s in roster.items()
                if s.get('template_file')}
        self.assertTrue(refs)
        r = self.run_gen()
        self.assertEqual(r.returncode, 0, r.stderr)
        for tname, ref in refs.items():
            with open(os.path.join(TEMPLATE_DIR, ref), encoding='utf-8') as f:
                body = f.read().strip()
            generated = self.read(f'_templates/type-{tname}.md')
            self.assertIn(body, generated,
                          f'{tname}: body of {ref} not embedded')

    def test_text_field_and_empty_body(self):
        self.run_gen('--dir', 'notes/=event', '--dir', 'project/=direction')
        e = self.read('_templates/type-event.md')
        self.assertIn('layer: ""', e)              # text field -> ""
        self.assertIn('characters: []', e)         # list field -> []
        d = self.read('_templates/type-direction.md')
        self.assertTrue(d.rstrip().endswith('---'))  # empty body tolerated

    def test_picker_for_mixed_dir_only(self):
        self.run_gen('--dir', 'notes/=character,event',
                     '--dir', 'project/=plan')
        picker = self.read('_templates/new-notes.md')
        self.assertIn('"character"', picker)
        self.assertIn('"event"', picker)
        self.assertIn('tp.system.suggester', picker)
        self.assertIn('tp.file.include', picker)
        self.assertIn('tp.system.prompt', picker)   # name prompt
        self.assertIn('tp.file.rename', picker)     # rename before include
        self.assertIn('let content = await tp.file.include(tmpl);', picker)
        self.assertIn(
            "content = content.replace(/^title: .*$/m, () => 'title: \"' + safe + '\"');",
            picker)
        self.assertIn('if (!type) { return; }', picker)
        self.assertIn('try { await tp.file.rename(name); }', picker)
        self.assertIn('tR += content;', picker)
        entry = self.read('_templates/new-project.md')
        self.assertNotIn('tp.system.suggester', entry)  # single type: no picker
        self.assertIn('tp.system.prompt', entry)
        self.assertIn('tp.file.rename', entry)
        self.assertIn('"_templates/type-plan"', entry)

    def test_obsidian_config_written_and_merged(self):
        cfgdir = os.path.join(self.dir, '.obsidian', 'plugins',
                              'templater-obsidian')
        os.makedirs(cfgdir)
        with open(os.path.join(cfgdir, 'data.json'), 'w') as f:
            json.dump({"command_timeout": 5}, f)
        self.run_gen('--dir', 'notes/=character,event',
                     '--dir', 'project/=plan', '--obsidian')
        data = json.loads(self.read('.obsidian/plugins/templater-obsidian/data.json'))
        self.assertEqual(data['command_timeout'], 5)          # merged, not clobbered
        self.assertEqual(data['templates_folder'], '_templates')
        self.assertEqual(data['trigger_on_file_creation_mode'], 'folder')
        self.assertIs(data['trigger_on_file_creation'], True)   # 2.20.x boolean key
        self.assertIs(data['enable_folder_templates'], True)    # 2.20.x boolean key
        self.assertIn({'folder': 'notes', 'template': '_templates/new-notes.md'},
                      data['folder_templates'])
        self.assertIn({'folder': 'project', 'template': '_templates/new-project.md'},
                      data['folder_templates'])

    def test_unknown_type_fails(self):
        r = self.run_gen('--dir', 'notes/=dragon')
        self.assertEqual(r.returncode, 2)
        self.assertIn('dragon', r.stderr)

    def test_default_all_types_one_picker(self):
        """No --dir: every roster type, one picker. With enforced_paths
        retired there is no path list to fan out over."""
        r = self.run_gen()
        self.assertEqual(r.returncode, 0, r.stderr)
        picker = self.read('_templates/new-note.md')
        for t in load_roster()['types']:
            self.assertIn(f'"{t}"', picker)

    def test_empty_type_list_fails(self):
        r = self.run_gen('--dir', 'notes/=')
        self.assertEqual(r.returncode, 2)
        self.assertIn('no types', r.stderr)


class OpenViewTests(unittest.TestCase):
    """Each of the eight setup bases has an Open view that excludes exactly
    the four closure tags and nothing else."""

    CLOSURE = {'complete', 'deprecated', 'abandoned', 'archived'}
    BASES = os.path.join(ROOT, 'skills', 'worldbuilder-setup', 'worldvault',
                         '_bases')

    def test_every_base_open_view_excludes_exactly_the_closure_tags(self):
        names = sorted(n for n in os.listdir(self.BASES)
                       if n.endswith('.base'))
        self.assertEqual(len(names), 8, names)
        for name in names:
            with open(os.path.join(self.BASES, name), encoding='utf-8') as f:
                base = yaml.safe_load(f)
            views = [v for v in base['views'] if v.get('name') == 'Open']
            self.assertEqual(len(views), 1, name)
            clauses = views[0]['filters']['and']
            excluded = set()
            for c in clauses:
                m = re.fullmatch(r'!tags\.contains\("([a-z]+)"\)', c)
                self.assertIsNotNone(m, f'{name}: unexpected filter {c}')
                excluded.add(m.group(1))
            self.assertEqual(excluded, self.CLOSURE, name)
            self.assertEqual(len(clauses), 4, name)


if __name__ == '__main__':
    unittest.main(verbosity=2)
