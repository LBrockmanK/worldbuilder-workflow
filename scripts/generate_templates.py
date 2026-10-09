#!/usr/bin/env python
"""Generate Obsidian Templater templates from this plugin's type roster.

One Templater template per roster type (frontmatter skeleton + type
body) in <out>/_templates/, a suggester type-picker per mixed-type
directory, and (--obsidian) the folder_templates wiring in the vendored
Templater data.json.

The roster is plugin-internal data — `defaults/types.json`, the single
source of truth for worldbuilder's types and status tags. There is no
per-project config file: projects adopt worldbuilder by enabling the
plugin, not by receiving a copy of the registry. Type bodies live as
markdown in `defaults/templates/` and are referenced by each type's
`template_file`; this script resolves those references and embeds the
bodies at generation time (the contract the retired build-okf.py
compile step used to satisfy).
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPES_JSON = os.path.join(ROOT, 'defaults', 'types.json')
TEMPLATE_DIR = os.path.join(ROOT, 'defaults', 'templates')

MOMENT_DATE = '<% moment.utc().format("YYYY-MM-DD") %>'
UNIVERSAL_ORDER = ('type', 'title', 'description', 'tags', 'created',
                   'resources')


def load_roster():
    with open(TYPES_JSON, encoding='utf-8') as f:
        return json.load(f)


def type_body(spec):
    """The type's body content: the referenced template file if there is
    one, else the inline `template` string."""
    ref = spec.get('template_file')
    if ref is None:
        return spec.get('template') or ''
    path = os.path.join(TEMPLATE_DIR, ref)
    if not os.path.isfile(path):
        print(f'error: missing template file: {path}', file=sys.stderr)
        sys.exit(2)
    with open(path, encoding='utf-8') as f:
        return f.read()


def empty_value(ftype):
    return {'list': '[]', 'tags': '[]', 'checkbox': 'false',
            'number': ''}.get(ftype, '""')


def type_template(config, tname):
    spec = config['types'][tname]
    lines = ['---',
             f'type: {tname}',
             'title: <% tp.file.title %>',
             'description: ""',
             'tags: []',
             f'created: "[[{MOMENT_DATE}]]"',
             'resources: []']
    for fname, fspec in (spec.get('fields') or {}).items():
        if fname in UNIVERSAL_ORDER:
            continue
        lines.append(f'{fname}: {empty_value(fspec.get("type", "text"))}')
    lines.append('---')
    body = type_body(spec).strip()
    return '\n'.join(lines) + '\n' + (('\n' + body + '\n') if body else '')


def entry_template(types, type_dir='_templates'):
    """Entry template a folder attaches to: prompt for the note name,
    rename before the skeleton renders (tp.file.title must resolve to
    the real name, not 'Untitled'), then include the type template.
    Mixed-type dirs get a suggester; single-type dirs skip it."""
    lines = ['<%*']
    if len(types) == 1:
        lines.append(f'const type = {json.dumps(types[0])};')
        # For single-type, build the path directly as a literal string
        template_path = f'{type_dir}/type-{types[0]}'
        lines += [
            'const name = await tp.system.prompt("Note name");',
            'if (name) { try { await tp.file.rename(name); } catch (e) { } }',
            f'const tmpl = tp.file.find_tfile({json.dumps(template_path)});',
            'let content = await tp.file.include(tmpl);',
            '// tp.file.title is captured before the rename; stamp the real name',
            'if (name) {',
            '  const safe = name.replace(/\\\\/g, "\\\\\\\\").replace(/"/g, \'\\\\"\');',
            '  content = content.replace(/^title: .*$/m, () => \'title: "\' + safe + \'"\');',
            '}',
            'tR += content;',
        ]
    else:
        choices = json.dumps(types)
        lines.append(f'const choices = {choices};')
        lines.append('const type = await tp.system.suggester(choices, choices);')
        lines += [
            'if (!type) { return; }',
            'const name = await tp.system.prompt("Note name");',
            'if (name) { try { await tp.file.rename(name); } catch (e) { } }',
            f'const tmpl = tp.file.find_tfile({json.dumps(type_dir)} + "/type-" + type);',
            'let content = await tp.file.include(tmpl);',
            '// tp.file.title is captured before the rename; stamp the real name',
            'if (name) {',
            '  const safe = name.replace(/\\\\/g, "\\\\\\\\").replace(/"/g, \'\\\\"\');',
            '  content = content.replace(/^title: .*$/m, () => \'title: "\' + safe + \'"\');',
            '}',
            'tR += content;',
        ]
    lines.append('%>')
    return '\n'.join(lines)


def dir_slug(path):
    return path.strip('/').replace('/', '-') or 'note'


def parse_dirs(pairs, config):
    """[(path, [types])] from --dir path=a,b; validates type names."""
    out = []
    for pair in pairs:
        path, _, names = pair.partition('=')
        types = [t.strip() for t in names.split(',') if t.strip()]
        if not types:
            print(f'error: no types given in --dir {pair!r}', file=sys.stderr)
            sys.exit(2)
        for t in types:
            if t not in config['types']:
                print(f'error: unknown type {t!r} in --dir {pair!r}',
                      file=sys.stderr)
                sys.exit(2)
        out.append((path, types))
    return out


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)


def update_obsidian_config(out_root, attachments):
    p = os.path.join(out_root, '.obsidian', 'plugins',
                     'templater-obsidian', 'data.json')
    data = {}
    if os.path.isfile(p):
        with open(p, encoding='utf-8') as f:
            data = json.load(f)
    data['templates_folder'] = '_templates'
    data['trigger_on_file_creation_mode'] = 'folder'
    # Templater <=2.21 uses boolean keys; >=2.22 uses the _mode string.
    # Write both so the config works regardless of the vendored version.
    data['trigger_on_file_creation'] = True
    data['enable_folder_templates'] = True
    data['folder_templates'] = [
        {'folder': folder.strip('/'), 'template': template}
        for folder, template in attachments]
    write(p, json.dumps(data, indent=2) + '\n')


def main():
    ap = argparse.ArgumentParser(description='Generate Templater templates '
                                             'from the plugin type roster')
    ap.add_argument('--out', required=True)
    ap.add_argument('--dir', action='append', default=[],
                    help='path=type[,type...] — types allowed in that dir')
    ap.add_argument('--obsidian', action='store_true',
                    help='wire folder_templates into the vendored '
                         'Templater data.json')
    args = ap.parse_args()

    config = load_roster()

    if args.dir:
        dirs = parse_dirs(args.dir, config)
    else:
        # No --dir: one picker over the whole roster at the vault root.
        # enforced_paths is retired with the registry, so there is no
        # per-project path list to fan out over.
        dirs = [('', sorted(config['types']))]

    emitted = set()
    attachments = []
    for path, types in dirs:
        for t in types:
            if t not in emitted:
                write(os.path.join(args.out, '_templates', f'type-{t}.md'),
                      type_template(config, t))
                emitted.add(t)
        name = (f'new-{dir_slug(path)}.md' if args.dir else 'new-note.md')
        write(os.path.join(args.out, '_templates', name),
              entry_template(types))
        attachments.append((path, f'_templates/{name}'))

    if args.obsidian:
        update_obsidian_config(args.out, attachments)
    print(f'{len(emitted)} type template(s), '
          f'{len(attachments)} folder attachment(s).')


if __name__ == '__main__':
    main()
