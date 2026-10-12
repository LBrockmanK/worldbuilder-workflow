"""Tests for check_coverage.py. Run: python tests/test_check_coverage.py

The checker reads a world (character notes with coverage ledgers, and the
reference sheet) and reports what a script can check. These tests build a
small passing world in a temporary directory, change one thing per test, and
assert on the checker's exit code and report lines.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, 'scripts', 'check_coverage.py')

NOTE = """---
type: character
title: {name}
tags: []
---

## Design Notes

### Coverage ledger

| Section | Entry | Source | Derived copies |
|---|---|---|---|
{ledger}

## Background

{background}

## Body

{preamble}

{body}

## Soul

{soul}

## Relationships

{relationships}

## Voice / Dialogue

{voice}

## Story Seeds

{seeds}
"""

ALICE_LEDGER = """| Background | 1 | alice-source.md | |
| Body | preamble 1 | alice-source.md#looks | appearance |
| Body | preamble 2 | alice-source.md#looks | appearance |
| Body | 1 | alice-source.md | |
| Soul | 1 | alice-source.md | |
| Soul | 2 | alice-source.md; bob-source.md | |
| Relationships | 1 | bob-source.md | |
| Voice / Dialogue | 1 | alice-source.md | |
| Story Seeds | 1 | alice-source.md | |"""

BOB_LEDGER = """| Background | 1 | bob-source.md | |
| Soul | 1 | bob-source.md | |
| Relationships | 1 | alice-source.md | |"""

SHEET = """---
type: reference
title: Reference sheet
tags: []
---

## Characters

### Alice

#### Facts

- Alice keeps goats (source: alice-source.md)

#### Occupations

| Occupation | Source |
|---|---|
| gardener | alice-source.md |
| General Store | alice-source.md |

### Bob

#### Facts

- Bob owns a dog called Rex (source: bob-source.md)

#### Occupations

| Occupation | Source |
|---|---|
| smith | bob-source.md |

### Rex

#### Facts

- Rex is a dog (source: bob-source.md)

#### Occupations

| Occupation | Source |
|---|---|

## Connections

| Kind | From | To | Fact | Source |
|---|---|---|---|---|
| ownership | Bob | Rex | Bob owns Rex | bob-source.md |
| friend | Alice | Bob | Alice and Bob are friends | alice-source.md |

## Contradictions

| Fact | Side A | Source A | Side B | Source B | Settled reading | Reason |
|---|---|---|---|---|---|---|
| Alice's age | 20 | alice-source.md | 21 | bob-source.md | 21 | newer file |

## Asset inventory

### Rex

| Set | File | Hash |
|---|---|---|
| spring | rex/spring/a.png | h1 |
| spring | rex/spring/b.png | h2 |
| winter | rex/winter/a.png | h3 |
| winter | rex/winter/b.png | h4 |
"""


def alice_note(ledger=ALICE_LEDGER, soul="- Soul one.\n- Soul two.",
               relationships="- **Bob:** She trusts him.",
               preamble="Red hair. Green eyes."):
    return NOTE.format(
        name='Alice', ledger=ledger, background="- Fact one.",
        preamble=preamble, body="- Body one.", soul=soul,
        relationships=relationships, voice="- Snippet.", seeds="- Seed.")


def bob_note(ledger=BOB_LEDGER, relationships="- **Alice — Friend:** He waves."):
    return NOTE.format(
        name='Bob', ledger=ledger, background="- Fact.", preamble="",
        body="", soul="- Soul.", relationships=relationships,
        voice="", seeds="")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


class CheckerCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = self.tmp.name
        self.put('notes/Alice.md', alice_note())
        self.put('notes/Bob.md', bob_note())
        self.put('reference/Reference sheet.md', SHEET)
        self.put('reference/alice-source.md', 'alice\n')
        self.put('reference/bob-source.md', 'bob\n')

    def put(self, rel, text):
        write(os.path.join(self.root, *rel.split('/')), text)

    def world(self):
        return subprocess.run(
            [sys.executable, SCRIPT, 'world', '--world-root', self.root],
            capture_output=True, text=True)

    def export(self, characters):
        path = os.path.join(self.root, 'world.json')
        write(path, json.dumps({'characters': characters}))
        return subprocess.run(
            [sys.executable, SCRIPT, 'export', '--world-root', self.root,
             '--world-json', path],
            capture_output=True, text=True)

    def fails(self, result):
        return [l for l in result.stdout.splitlines() if l.startswith('FAIL')]


class WorldModeTests(CheckerCase):
    def test_a_complete_world_passes(self):
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.fails(result), [])

    def test_a_note_without_a_ledger_fails(self):
        self.put('notes/Alice.md', alice_note().replace(
            '### Coverage ledger', '### Something else'))
        result = self.world()
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any('Alice' in l and 'ledger' in l
                            for l in self.fails(result)), result.stdout)
        self.assertFalse(any('Bob' in l for l in self.fails(result)))

    def test_an_entry_with_no_row_fails(self):
        ledger = ALICE_LEDGER.replace('| Soul | 2 | alice-source.md; bob-source.md | |\n', '')
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any('Soul 2' in l for l in self.fails(result)),
                        result.stdout)

    def test_an_intimate_dynamics_entry_with_no_row_fails(self):
        text = alice_note() + "\n## Intimate Dynamics\n\n- Entry one.\n"
        self.put('notes/Alice.md', text)
        result = self.world()
        self.assertTrue(any('Intimate Dynamics 1' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_body_preamble_clause_with_no_row_fails(self):
        ledger = ALICE_LEDGER.replace('| Body | preamble 2 | alice-source.md#looks | appearance |\n', '')
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertTrue(any('preamble 2' in l for l in self.fails(result)),
                        result.stdout)

    def test_a_row_naming_an_entry_the_note_lacks_fails(self):
        ledger = ALICE_LEDGER + "\n| Soul | 3 | alice-source.md | |"
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertTrue(any('Soul 3' in l and 'no such entry' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_row_whose_source_does_not_exist_fails(self):
        ledger = ALICE_LEDGER.replace('| Soul | 1 | alice-source.md |',
                                      '| Soul | 1 | missing.md |')
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertTrue(any('missing.md' in l for l in self.fails(result)),
                        result.stdout)

    def test_a_flagged_row_is_listed_and_does_not_fail(self):
        ledger = ALICE_LEDGER.replace('| Soul | 1 | alice-source.md |',
                                      '| Soul | 1 | flagged |')
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)
        flagged = [l for l in result.stdout.splitlines()
                   if l.startswith('FLAGGED')]
        self.assertEqual(len(flagged), 1)
        self.assertIn('Soul 1', flagged[0])

    def test_a_contradiction_with_one_source_fails(self):
        self.put('reference/Reference sheet.md', SHEET.replace(
            '| 21 | bob-source.md |', '| 21 |  |'))
        result = self.world()
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any('Contradictions' in l and "Alice's age" in l
                            for l in self.fails(result)), result.stdout)

    def test_two_sets_with_identical_hashes_fail(self):
        self.put('reference/Reference sheet.md', SHEET.replace(
            '| winter | rex/winter/a.png | h3 |\n| winter | rex/winter/b.png | h4 |',
            '| winter | rex/winter/a.png | h1 |\n| winter | rex/winter/b.png | h2 |'))
        result = self.world()
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any('Rex' in l and 'spring' in l and 'winter' in l
                            for l in self.fails(result)), result.stdout)

    def test_an_unmirrored_relationship_fails(self):
        self.put('notes/Bob.md', bob_note(
            ledger="| Background | 1 | bob-source.md | |\n"
                   "| Soul | 1 | bob-source.md | |",
            relationships=""))
        result = self.world()
        self.assertTrue(any('Alice' in l and 'Bob' in l and 'mirror' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_relationship_with_a_cast_member_who_has_no_note_is_pending(self):
        self.put('notes/Alice.md', alice_note(
            relationships="- **Bob:** She trusts him.\n- **Rex:** She pats him."
        ).replace('| Relationships | 1 | bob-source.md | |',
                  '| Relationships | 1 | bob-source.md | |\n'
                  '| Relationships | 2 | bob-source.md | |'))
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)
        pending = [l for l in result.stdout.splitlines()
                   if l.startswith('PENDING')]
        self.assertEqual(len(pending), 1)
        self.assertIn('Rex', pending[0])


class ExportModeTests(CheckerCase):
    def good(self):
        return [
            {'name': 'Alice', 'role': 'Gardener and General Store clerk',
             'appearance': 'Red hair.  Green eyes.',
             'spriteSets': [{'name': 'default', 'description': 'Alice at rest'}]},
            {'name': 'Rex', 'role': 'A dog',
             'spriteSets': [{'name': 'default',
                             'description': "Bob's dog, sitting"}]},
        ]

    def test_a_faithful_export_passes(self):
        result = self.export(self.good())
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_a_role_missing_an_occupation_fails(self):
        chars = self.good()
        chars[0]['role'] = 'Gardener'
        result = self.export(chars)
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any('Alice' in l and 'General Store' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_set_description_naming_a_wrong_owner_fails(self):
        chars = self.good()
        chars[1]['spriteSets'][0]['description'] = "Alice's dog, sitting"
        result = self.export(chars)
        self.assertTrue(any('Rex' in l and 'Alice' in l
                            for l in self.fails(result)), result.stdout)

    def test_an_appearance_that_differs_from_the_preamble_fails(self):
        chars = self.good()
        chars[0]['appearance'] = 'Brown hair. Green eyes.'
        result = self.export(chars)
        self.assertTrue(any('Alice' in l and 'appearance' in l
                            for l in self.fails(result)), result.stdout)


if __name__ == '__main__':
    unittest.main()
