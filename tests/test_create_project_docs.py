"""Tests for create_project_docs.py. Run: python tests/test_create_project_docs.py

The script lays down a new worldbuilder project: the three project
documents under `project/`, and the definition note for the one term the
export platform names differently. These tests run it against a
temporary project root and assert on what lands there.
"""
import os
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, 'scripts', 'create_project_docs.py')


def run(project_root):
    return subprocess.run(
        [sys.executable, SCRIPT, '--project-root', project_root,
         '--name', 'Test World'],
        capture_output=True, text=True)


def split_front_matter(text):
    _, front, body = text.split('---', 2)
    return yaml.safe_load(front), body.lstrip('\n')


class ProjectRootTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = self.tmp.name
        self.result = run(self.root)

    def test_the_run_succeeds(self):
        self.assertEqual(self.result.returncode, 0, self.result.stderr)

    def test_the_root_holds_only_what_the_script_declares(self):
        self.assertEqual(set(os.listdir(self.root)),
                         {'project', 'lorebook.md'})

    def test_the_three_project_documents_are_written(self):
        self.assertEqual(
            set(os.listdir(os.path.join(self.root, 'project'))),
            {'seed.md', 'plan.md', 'direction.md'})

    def test_the_project_documents_are_born_with_empty_tags(self):
        for name in ('seed', 'plan', 'direction'):
            with open(os.path.join(self.root, 'project', f'{name}.md'),
                      encoding='utf-8') as f:
                front, _ = split_front_matter(f.read())
            self.assertEqual(front['tags'], [], name)

    def test_a_second_run_refuses_rather_than_overwriting(self):
        second = run(self.root)
        self.assertEqual(second.returncode, 1)


class ExistingDefinitionNoteTests(unittest.TestCase):
    """A project root that already holds the definition note, and nothing
    else. The script must refuse rather than overwrite it."""

    SENTINEL = 'sentinel body the script must not touch\n'

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = self.tmp.name
        self.note = os.path.join(self.root, 'lorebook.md')
        with open(self.note, 'w', encoding='utf-8', newline='') as f:
            f.write(self.SENTINEL)
        self.result = run(self.root)

    def test_the_run_refuses(self):
        self.assertNotEqual(self.result.returncode, 0, self.result.stdout)

    def test_the_existing_note_is_byte_for_byte_unchanged(self):
        with open(self.note, 'rb') as f:
            self.assertEqual(f.read(), self.SENTINEL.encode('utf-8'))


class DefinitionNoteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        result = run(self.tmp.name)
        self.assertEqual(result.returncode, 0, result.stderr)
        with open(os.path.join(self.tmp.name, 'lorebook.md'),
                  encoding='utf-8') as f:
            self.front, self.body = split_front_matter(f.read())

    def test_it_carries_the_universal_properties(self):
        self.assertEqual(set(self.front),
                         {'created', 'modified', 'aliases', 'tags',
                          'subjects', 'type', 'description'})
        self.assertEqual(self.front['aliases'], [])
        self.assertEqual(self.front['subjects'], [])
        self.assertIsNone(self.front['modified'])

    def test_it_is_born_a_definition_note_tagged_todo(self):
        self.assertEqual(self.front['type'], '[[definition]]')
        self.assertEqual(self.front['tags'], ['todo'])

    def test_created_is_a_daily_note_link(self):
        created = self.front['created']
        self.assertTrue(created.startswith('[['), created)
        self.assertTrue(created.endswith(']]'), created)
        self.assertEqual(len(created), 14, created)

    def test_the_description_is_the_operative_definition_on_one_line(self):
        self.assertIn('world info', self.front['description'])
        self.assertNotIn('\n', self.front['description'].strip())

    def test_the_body_leads_with_the_definition_and_names_the_synonym(self):
        lines = [line for line in self.body.splitlines() if line.strip()]
        self.assertIn('world info', lines[0])
        self.assertTrue(lines[-1].startswith('**Avoid.**'), lines[-1])
        self.assertIn('world info', lines[-1])


if __name__ == '__main__':
    unittest.main()
