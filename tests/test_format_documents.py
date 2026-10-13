"""Tests for the entity skills' format documents.

Every entity skill in scope has a format document that ends with a
`## Review criteria` section holding `### Checks`, `### Exempt` and
`### Judgment calls`, in that order. The critic reads that section
(`skills/worldbuilder-review/SKILL.md`, Phase 1).

Part 1 covers character, location, faction, event and concept. The story
skill joins when the story framework lands.

The character skill also keeps each required doctrine entry name in
`card-format.md` only: one home per rule.
"""
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, 'skills')

# skill folder -> format document file name
FORMAT_DOCUMENTS = {
    'worldbuilder-character': 'card-format.md',
    'worldbuilder-location': 'note-format.md',
    'worldbuilder-faction': 'note-format.md',
    'worldbuilder-event': 'note-format.md',
    'worldbuilder-concept': 'note-format.md',
}

REQUIRED_ENTRY_NAMES = [
    'Core want',
    'Core fear',
    'False belief',
    'Value-conflict stance',
    'unresolved tension',
    'Values with costs',
    'Protective strategy',
]


def read(*parts):
    with open(os.path.join(SKILLS, *parts), encoding='utf-8') as f:
        return f.read()


class FormatDocumentTests(unittest.TestCase):

    def test_each_skill_has_its_format_document(self):
        for folder, name in FORMAT_DOCUMENTS.items():
            path = os.path.join(SKILLS, folder, name)
            self.assertTrue(os.path.isfile(path), f'{folder}/{name} missing')

    def test_review_criteria_holds_the_three_subsections_in_order(self):
        for folder, name in FORMAT_DOCUMENTS.items():
            lines = read(folder, name).splitlines()
            self.assertIn('## Review criteria', lines, f'{folder}/{name}')
            after = lines[lines.index('## Review criteria') + 1:]
            headings = [ln for ln in after if re.match(r'#{2,3} ', ln)]
            self.assertEqual(
                headings[:3],
                ['### Checks', '### Exempt', '### Judgment calls'],
                f'{folder}/{name}')

    def test_character_required_entry_names_have_one_home(self):
        folder = os.path.join(SKILLS, 'worldbuilder-character')
        card = read('worldbuilder-character', 'card-format.md')
        others = {f: read('worldbuilder-character', f)
                  for f in sorted(os.listdir(folder))
                  if f.endswith('.md') and f != 'card-format.md'}
        for entry in REQUIRED_ENTRY_NAMES:
            self.assertIn(entry, card, f'{entry!r} missing from card-format.md')
            for fname, text in others.items():
                self.assertNotIn(entry, text,
                                 f'{entry!r} restated in {fname}')


if __name__ == '__main__':
    unittest.main(verbosity=2)
