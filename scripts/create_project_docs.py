#!/usr/bin/env python3
"""Create the three worldbuilder project documents in one call.

Replaces the multi-step agent-executed prose of worldbuilder-setup Step 4
with a single mechanical invocation.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULTS_DIR = os.path.join(REPO_ROOT, 'defaults')
TYPES_FILE = os.path.join(DEFAULTS_DIR, 'types.json')
TEMPLATES_DIR = os.path.join(DEFAULTS_DIR, 'templates')

PROJECT_DOCS = [
    ('foundation', 'World Foundation', 'World foundation document for'),
    ('plan', 'Worldbuilding Plan', 'Cast plan for'),
    ('direction', 'Story Direction', 'Standing creative brief for'),
]


def read_template(doc_type, types_data):
    template_file = types_data.get(doc_type, {}).get('template_file', '')
    if not template_file:
        return ''
    path = os.path.join(TEMPLATES_DIR, template_file)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except OSError:
        return ''


def create_doc(project_dir, doc_type, title, description, template_content):
    now = datetime.now(timezone.utc)
    fm_data = {
        'type': doc_type,
        'title': title,
        'description': description,
        'tags': [],
        'created': f'[[{now.date().isoformat()}]]',
        'resources': [],
    }
    fm_text = yaml.safe_dump(fm_data, sort_keys=False, allow_unicode=True).strip()

    body = f'\n# {title}\n\n{template_content}' if template_content else f'\n# {title}\n'

    path = os.path.join(project_dir, f'{doc_type}.md')
    if os.path.exists(path):
        raise FileExistsError(f'Already exists: {path}')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f'---\n{fm_text}\n---\n{body}')
    return path


def main():
    parser = argparse.ArgumentParser(
        description='Create the three worldbuilder project documents')
    parser.add_argument('--project-root', required=True,
                        help='Root directory of the worldbuilder project')
    parser.add_argument('--name', required=True,
                        help='Project name (e.g. "Fields of Mistria")')
    args = parser.parse_args()

    project_dir = os.path.join(args.project_root, 'project')
    os.makedirs(project_dir, exist_ok=True)

    with open(TYPES_FILE, 'r', encoding='utf-8') as f:
        types_data = json.load(f)['types']

    for doc_type, title_suffix, desc_prefix in PROJECT_DOCS:
        title = f'{args.name} {title_suffix}'
        description = f'{desc_prefix} {args.name}'
        template = read_template(doc_type, types_data)
        try:
            path = create_doc(project_dir, doc_type, title, description, template)
        except FileExistsError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)
        print(f'Created {path}')


if __name__ == '__main__':
    main()
