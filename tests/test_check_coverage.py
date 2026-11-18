"""Tests for check_coverage.py. Run: python tests/test_check_coverage.py

The checker reads a world (character notes with coverage ledgers, and the
reference sheet) and reports what a script can check. These tests build a
small passing world in a temporary directory, change one thing per test, and
assert on the checker's exit code and report lines.
"""
import json
import os
import shutil
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

| Section | Entry | Claim | Source | Derived copies |
|---|---|---|---|---|
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

ALICE_LEDGER = """| Background | 1 | claim | alice-source.md | |
| Body | preamble 1 | claim | alice-source.md#looks | appearance |
| Body | preamble 2 | claim | alice-source.md#looks | appearance |
| Body | 1 | claim | alice-source.md | |
| Soul | 1 | claim | alice-source.md | |
| Soul | 2 | claim | alice-source.md; bob-source.md | |
| Relationships | 1 | claim | bob-source.md | |
| Voice / Dialogue | 1 | claim | alice-source.md | |
| Story Seeds | 1 | claim | alice-source.md | |"""

BOB_LEDGER = """| Background | 1 | claim | bob-source.md | |
| Soul | 1 | claim | bob-source.md | |
| Relationships | 1 | claim | alice-source.md | |"""

OCC_HEAD = "| Occupation | Source | Ids |\n|---|---|---|"
CONN_HEAD = "| Kind | From | To | Fact | Source | Ids |\n|---|---|---|---|---|---|"
CONTRA_HEAD = ("| Fact | Side A | Source A | Side B | Source B | Settled reading "
               "| Reason | Ids |\n|---|---|---|---|---|---|---|---|")
ASSET_HEAD = "| Set | File | Hash | Ids |\n|---|---|---|---|"


def char_sheet(name, facts="", occupations="", connections="",
               contradictions="", assets="", aliases=None):
    front = f"type: reference\ntitle: {name}\ndescription: x\n"
    if aliases is not None:
        front += "aliases: [" + ", ".join(aliases) + "]\n"
    return (f"---\n{front}tags: []\n---\n\n## Profile\n\n- Name: {name}\n\n"
            f"## Facts\n\n{facts}\n\n"
            f"## Occupations\n\n{occupations}\n\n"
            f"## Connections\n\n{connections}\n\n"
            f"## Contradictions\n\n{contradictions}\n\n"
            f"## Asset inventory\n\n{assets}\n\n"
            "## Provenance\n\n- none\n")


ALICE_SHEET = char_sheet(
    'Alice', facts="- Alice keeps goats (source: alice-source.md)",
    occupations=OCC_HEAD + "\n| gardener | alice-source.md | 1 |"
                "\n| General Store | alice-source.md | 2 |",
    connections=CONN_HEAD + "\n| friend | Alice | Bob | Alice and Bob are "
                "friends | alice-source.md | 1 |",
    contradictions=CONTRA_HEAD + "\n| Alice's age | 20 | alice-source.md | 21 "
                   "| bob-source.md | 21 | newer file | 1 |")

BOB_SHEET = char_sheet(
    'Bob', facts="- Bob owns a dog called Rex (source: bob-source.md)",
    occupations=OCC_HEAD + "\n| smith | bob-source.md | 1 |",
    connections=CONN_HEAD + "\n| ownership | Bob | Rex | Bob owns Rex "
                "| bob-source.md | 1 |")

REX_SHEET = char_sheet(
    'Rex', facts="- Rex is a dog (source: bob-source.md)",
    occupations=OCC_HEAD,
    assets=ASSET_HEAD + "\n| spring | rex/spring/a.png | h1 | 1 |"
           "\n| spring | rex/spring/b.png | h2 | 1 |"
           "\n| winter | rex/winter/a.png | h3 | 1 |"
           "\n| winter | rex/winter/b.png | h4 | 1 |")

WORLD_SHEET = ("---\ntype: reference\ntitle: world 1\ndescription: x\n"
               "tags: []\n---\n\n## Facts\n\n- The town is small.\n")


def alice_note(ledger=ALICE_LEDGER, soul="- Soul one.\n- Soul two.",
               relationships="- **Bob:** She trusts him.",
               preamble="Red hair. Green eyes.",
               seeds="**Introduction**\n\nCondition: arrival. She waves."):
    return NOTE.format(
        name='Alice', ledger=ledger, background="- Fact one.",
        preamble=preamble, body="- Body one.", soul=soul,
        relationships=relationships, voice="- Snippet.", seeds=seeds)


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
        self.put('reference/sheets/1001 Alice.md', ALICE_SHEET)
        self.put('reference/sheets/1002 Bob.md', BOB_SHEET)
        self.put('reference/sheets/Rex.md', REX_SHEET)
        self.put('reference/sheets/world 1 town.md', WORLD_SHEET)
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
        ledger = ALICE_LEDGER.replace(
            '| Soul | 2 | claim | alice-source.md; bob-source.md | |\n', '')
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
        ledger = ALICE_LEDGER.replace(
            '| Body | preamble 2 | claim | alice-source.md#looks | appearance |\n',
            '')
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertTrue(any('preamble 2' in l for l in self.fails(result)),
                        result.stdout)

    def test_a_story_seed_block_with_no_row_fails(self):
        seeds = ("**Introduction**\n\nCondition: arrival. She waves.\n\n"
                 "**The market**\n\nCondition: market day. She haggles.")
        self.put('notes/Alice.md', alice_note(seeds=seeds))
        result = self.world()
        self.assertTrue(any('Story Seeds 2' in l for l in self.fails(result)),
                        result.stdout)
        self.assertFalse(any('Story Seeds 1' in l for l in self.fails(result)))

    def test_several_rows_may_cover_one_entry(self):
        ledger = ALICE_LEDGER.replace(
            '| Soul | 1 | claim | alice-source.md | |',
            '| Soul | 1.a | first claim | alice-source.md | |\n'
            '| Soul | 1.b | second claim | bob-source.md | |')
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_a_duplicate_claim_key_fails(self):
        ledger = ALICE_LEDGER + "\n| Soul | 1 | claim again | alice-source.md | |"
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertTrue(any('Soul 1' in l and 'twice' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_row_naming_an_entry_the_note_lacks_fails(self):
        ledger = ALICE_LEDGER + "\n| Soul | 3 | claim | alice-source.md | |"
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertTrue(any('Soul 3' in l and 'no such entry' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_row_whose_source_does_not_exist_fails(self):
        ledger = ALICE_LEDGER.replace(
            '| Soul | 1 | claim | alice-source.md |',
            '| Soul | 1 | claim | missing.md |')
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertTrue(any('missing.md' in l for l in self.fails(result)),
                        result.stdout)

    def test_a_source_outside_reference_fails(self):
        ledger = ALICE_LEDGER.replace(
            '| Soul | 1 | claim | alice-source.md |',
            '| Soul | 1 | claim | ../notes/Bob.md |')
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertTrue(any('Bob.md' in l and 'reference/' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_source_on_another_drive_is_reported_not_a_crash(self):
        drive = os.path.splitdrive(os.path.abspath(self.root))[0].upper()
        other = 'D:' if drive == 'C:' else 'C:'
        ledger = ALICE_LEDGER.replace(
            '| Soul | 1 | claim | alice-source.md |',
            '| Soul | 1 | claim | ' + other + chr(92) + 'source.md |')
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertTrue(any('source.md' in l and 'reference/' in l
                            for l in self.fails(result)), result.stdout)

    def test_an_unwritten_flagged_claim_is_listed_and_does_not_fail(self):
        ledger = ALICE_LEDGER + (
            "\n| Soul | unwritten | She fears water | flagged | |")
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)
        flagged = [l for l in result.stdout.splitlines()
                   if l.startswith('FLAGGED')]
        self.assertEqual(len(flagged), 1)
        self.assertIn('She fears water', flagged[0])

    def test_a_flagged_claim_that_is_written_into_the_card_fails(self):
        ledger = ALICE_LEDGER.replace(
            '| Soul | 1 | claim | alice-source.md |',
            '| Soul | 1 | claim | flagged |')
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any('Soul 1' in l and 'flagged' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_contradiction_with_one_source_fails(self):
        self.put('reference/sheets/1001 Alice.md', ALICE_SHEET.replace(
            '| 21 | bob-source.md |', '| 21 |  |'))
        result = self.world()
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any('Contradictions' in l and "Alice's age" in l
                            for l in self.fails(result)), result.stdout)

    def test_two_sets_with_identical_hashes_fail(self):
        self.put('reference/sheets/Rex.md', REX_SHEET.replace(
            '| winter | rex/winter/a.png | h3 | 1 |\n| winter | rex/winter/b.png | h4 | 1 |',
            '| winter | rex/winter/a.png | h1 | 1 |\n| winter | rex/winter/b.png | h2 | 1 |'))
        result = self.world()
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any('Rex' in l and 'spring' in l and 'winter' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_one_sided_relationship_passes(self):
        self.put('notes/Bob.md', bob_note(
            ledger="| Background | 1 | claim | bob-source.md | |\n"
                   "| Soul | 1 | claim | bob-source.md | |",
            relationships=""))
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.fails(result), [])

    def test_a_relationship_with_a_cast_member_who_has_no_note_is_not_pending(self):
        self.put('notes/Alice.md', alice_note(
            relationships="- **Bob:** She trusts him.\n- **Rex:** She pats him."
        ).replace('| Relationships | 1 | claim | bob-source.md | |',
                  '| Relationships | 1 | claim | bob-source.md | |\n'
                  '| Relationships | 2 | claim | bob-source.md | |'))
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual([l for l in result.stdout.splitlines()
                          if l.startswith('PENDING')], [])

    def test_an_inferred_row_on_a_written_entry_is_a_written_claim(self):
        evidence = ('inferred: alice sheet Facts; anime ep 3 02:10 # scene; '
                    'manga ch 5 p 12')
        ledger = ALICE_LEDGER.replace(
            '| Soul | 1 | claim | alice-source.md |',
            f'| Soul | 1 | claim | {evidence} |')
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.fails(result), [])
        self.assertEqual([l for l in result.stdout.splitlines()
                          if l.startswith('FLAGGED')], [])

    def test_an_inferred_row_on_an_unwritten_entry_fails(self):
        ledger = ALICE_LEDGER + (
            "\n| Soul | unwritten | She fears water | inferred: a sheet fact "
            "| |")
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any('unwritten' in l and 'must have Source flagged' in l
                            for l in self.fails(result)), result.stdout)

    def test_an_inferred_cell_with_no_evidence_fails(self):
        ledger = ALICE_LEDGER.replace(
            '| Soul | 1 | claim | alice-source.md |',
            '| Soul | 1 | claim | inferred:   |')
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any('Soul 1' in l and 'inferred' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_capitalised_inferred_cell_is_accepted(self):
        ledger = ALICE_LEDGER.replace(
            '| Soul | 1 | claim | alice-source.md |',
            '| Soul | 1 | claim | Inferred: Alice keeps goats (alice sheet Facts); anime ep 3 02:10 |')
        self.put('notes/Alice.md', alice_note(ledger=ledger))
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.fails(result), [])

    def test_a_clean_world_with_a_one_sided_relationship_has_a_zero_summary(self):
        self.put('notes/Bob.md', bob_note(
            ledger="| Background | 1 | claim | bob-source.md | |\n"
                   "| Soul | 1 | claim | bob-source.md | |",
            relationships=""))
        result = self.world()
        self.assertIn('0 failure(s), 0 flagged, 0 pending', result.stdout)


class ExportModeTests(CheckerCase):
    def setUp(self):
        super().setUp()
        self.put('notes/Rex.md', NOTE.format(
            name='Rex', ledger='', background='', preamble='', body='',
            soul='', relationships='', voice='', seeds=''))

    def good(self):
        return [
            {'name': 'Alice', 'role': 'Gardener and General Store clerk',
             'appearance': 'Red hair.  Green eyes.',
             'spriteSets': [{'name': 'default', 'description': 'Alice at rest'}]},
            {'name': 'Bob', 'role': 'Village smith', 'appearance': '',
             'spriteSets': []},
            {'name': 'Rex', 'role': 'A dog', 'appearance': '',
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

    def test_an_occupation_inside_another_word_does_not_count(self):
        chars = self.good()
        chars[1]['role'] = 'A wordsmith'
        result = self.export(chars)
        self.assertTrue(any('Bob' in l and 'smith' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_set_description_naming_a_wrong_owner_fails(self):
        chars = self.good()
        chars[2]['spriteSets'][0]['description'] = "Alice's dog, sitting"
        result = self.export(chars)
        self.assertTrue(any('Rex' in l and 'Alice' in l
                            for l in self.fails(result)), result.stdout)

    def test_an_owner_outside_the_cast_fails(self):
        chars = self.good()
        chars[2]['spriteSets'][0]['description'] = "Owned by Holt, sitting"
        result = self.export(chars)
        self.assertTrue(any('Rex' in l and 'Holt' in l
                            for l in self.fails(result)), result.stdout)

    def test_an_owner_named_where_the_table_lists_none_fails(self):
        chars = self.good()
        chars[0]['spriteSets'][0]['description'] = 'Pet of Bob, at rest'
        result = self.export(chars)
        self.assertTrue(any('Alice' in l and 'Bob' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_card_with_no_sheet_subsection_is_reported(self):
        self.put('notes/Dave.md', alice_note().replace(
            'title: Alice', 'title: Dave'))
        chars = self.good() + [{'name': 'Dave', 'role': 'x',
                                'appearance': 'Red hair. Green eyes.'}]
        result = self.export(chars)
        self.assertTrue(any('Dave' in l and 'sheet' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_multi_word_owner_name_is_read_whole(self):
        chars = self.good()
        chars[2]['spriteSets'][0]['description'] = (
            "Mary Jane Watson's dog, sitting")
        result = self.export(chars)
        self.assertTrue(any('Rex' in l and 'Mary Jane Watson' in l
                            for l in self.fails(result)), result.stdout)

    def know_mary(self):
        self.put('reference/sheets/1002 Bob.md', BOB_SHEET.replace(
            '| ownership | Bob | Rex | Bob owns Rex | bob-source.md | 1 |',
            '| ownership | Bob | Rex | Bob owns Rex | bob-source.md | 1 |\n'
            '| friend | Mary | Bob | Mary knows Bob | bob-source.md | 2 |'))

    def test_owned_by_matches_a_known_name_in_any_case(self):
        self.know_mary()
        chars = self.good()
        chars[2]['spriteSets'][0]['description'] = 'owned by mary, sitting'
        result = self.export(chars)
        self.assertTrue(any('Rex' in l and 'mary' in l
                            for l in self.fails(result)), result.stdout)

    def test_owned_by_nobody_is_not_an_owner(self):
        self.know_mary()
        for text in ('not owned by anyone, sitting', 'owned by no one',
                     'belongs to nobody', 'owned by a farmer'):
            chars = self.good()
            chars[2]['spriteSets'][0]['description'] = text
            result = self.export(chars)
            self.assertEqual(result.returncode, 0, text + result.stdout)

    def test_a_capital_letter_in_another_script_starts_a_name(self):
        chars = self.good()
        chars[2]['spriteSets'][0]['description'] = "Élodie's goat, sitting"
        result = self.export(chars)
        self.assertTrue(any('Rex' in l and 'lodie as owner' in l
                            for l in self.fails(result)), result.stdout)

    def test_both_a_wrong_appearance_and_a_missing_subsection_are_reported(self):
        self.put('notes/Dave.md', alice_note().replace(
            'title: Alice', 'title: Dave'))
        chars = self.good() + [{'name': 'Dave', 'role': 'x',
                                'appearance': 'Wrong.'}]
        result = self.export(chars)
        fails = self.fails(result)
        self.assertTrue(any('Dave' in l and 'appearance' in l
                            for l in fails), result.stdout)
        self.assertTrue(any('Dave' in l and 'sheet' in l
                            for l in fails), result.stdout)

    def test_a_farm_animal_word_counts_as_a_pet_word(self):
        chars = self.good()
        chars[2]['spriteSets'][0]['description'] = "Holt's goat, sitting"
        result = self.export(chars)
        self.assertTrue(any('Rex' in l and 'Holt' in l
                            for l in self.fails(result)), result.stdout)

    def test_an_appearance_that_differs_from_the_preamble_fails(self):
        chars = self.good()
        chars[0]['appearance'] = 'Brown hair. Green eyes.'
        result = self.export(chars)
        self.assertTrue(any('Alice' in l and 'appearance' in l
                            for l in self.fails(result)), result.stdout)

    def test_an_empty_appearance_against_a_preamble_fails(self):
        chars = self.good()
        chars[0]['appearance'] = ''
        result = self.export(chars)
        self.assertTrue(any('Alice' in l and 'appearance' in l
                            for l in self.fails(result)), result.stdout)

    def test_an_exported_character_with_no_note_fails(self):
        chars = self.good() + [{'name': 'Zed', 'role': 'x'}]
        result = self.export(chars)
        self.assertTrue(any('Zed' in l and 'no character note' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_last_name_is_part_of_the_identity(self):
        self.put('notes/Carol Smith.md', alice_note().replace(
            'title: Alice', 'title: Carol Smith'))
        self.put('reference/sheets/1003 Carol Smith.md', char_sheet(
            'Carol Smith', occupations=OCC_HEAD + '\n| baker | alice-source.md | 1 |'))
        chars = self.good() + [{'name': 'Carol', 'lastName': 'Smith',
                                'role': 'Cook',
                                'appearance': 'Red hair. Green eyes.'}]
        result = self.export(chars)
        self.assertTrue(any('Carol Smith' in l and 'baker' in l
                            for l in self.fails(result)), result.stdout)


WORLD_TWO = ("---\ntype: reference\ntitle: world 2\ndescription: x\n"
             "tags: []\n---\n\n## Facts\n\n- A fact.\n\n"
             "## Connections\n\n" + CONN_HEAD +
             "\n| ownership | Mary | Rex | Mary owns Rex | bob-source.md | 1 |"
             "\n| friend | Nobody | Alice | Nobody likes Alice "
             "| alice-source.md | 2 |\n\n"
             "## Contradictions\n\n" + CONTRA_HEAD +
             "\n| Town size | big | alice-source.md | small |  | small "
             "| newer | 1 |\n")


class SheetFolderTests(CheckerCase):
    def test_a_missing_sheet_folder_gives_one_line_in_world_mode(self):
        shutil.rmtree(os.path.join(self.root, 'reference', 'sheets'))
        result = self.world()
        self.assertEqual(result.returncode, 1)
        fails = self.fails(result)
        self.assertEqual(len(fails), 1, result.stdout)
        self.assertIn('reference/sheets/', fails[0])

    def test_a_missing_sheet_folder_gives_one_line_in_export_mode(self):
        shutil.rmtree(os.path.join(self.root, 'reference', 'sheets'))
        result = self.export([{'name': 'Alice', 'role': 'x'}])
        self.assertEqual(result.returncode, 1)
        fails = self.fails(result)
        self.assertEqual(len(fails), 1, result.stdout)
        self.assertIn('reference/sheets/', fails[0])

    def test_a_subfolder_and_a_stray_merged_sheet_change_nothing(self):
        self.put('reference/sheets/checks/9999 Zed.md', char_sheet(
            'Zed', contradictions=CONTRA_HEAD +
            "\n| Bad | a | s |  |  | a | r | 1 |"))
        self.put('reference/' + 'Reference ' + 'sheet.md',
                 '## Characters\n\n### Zed\n\n#### Occupations\n\n'
                 '| Occupation | Source |\n|---|---|\n| king | x |\n')
        self.put('notes/Alice.md', alice_note(
            relationships="- **Bob:** She trusts him.\n- **Zed:** Hm.")
            .replace('| Relationships | 1 | claim | bob-source.md | |',
                     '| Relationships | 1 | claim | bob-source.md | |\n'
                     '| Relationships | 2 | claim | bob-source.md | |'))
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn('Zed', result.stdout)

    def test_a_world_file_with_only_facts_and_empty_sections_read_fine(self):
        self.put('reference/sheets/1004 Dee.md',
                 '---\ntype: reference\n---\n\n## Facts\n\n- Dee exists.\n')
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_a_world_file_contradiction_with_one_source_fails_naming_it(self):
        self.put('reference/sheets/world 2 more.md', WORLD_TWO)
        result = self.world()
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any('world 2 more.md' in l and 'Town size' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_contradiction_fail_names_the_character_sheet_file(self):
        self.put('reference/sheets/1001 Alice.md', ALICE_SHEET.replace(
            '| 21 | bob-source.md |', '| 21 |  |'))
        result = self.world()
        self.assertTrue(any('1001 Alice.md' in l
                            for l in self.fails(result)), result.stdout)

    def test_a_world_file_adds_no_cast_member(self):
        self.put('reference/sheets/world 2 more.md',
                 WORLD_TWO.replace('| Town size | big | alice-source.md '
                                   '| small |  |', '| Town size | big | a '
                                   '| small | b |'))
        self.put('notes/Alice.md', alice_note(
            relationships="- **Bob:** She trusts him.\n- **Nobody:** Hm.")
            .replace('| Relationships | 1 | claim | bob-source.md | |',
                     '| Relationships | 1 | claim | bob-source.md | |\n'
                     '| Relationships | 2 | claim | bob-source.md | |'))
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual([l for l in result.stdout.splitlines()
                          if l.startswith('PENDING')], [])

    def test_the_same_asset_sets_in_two_sheets_do_not_fail(self):
        self.put('reference/sheets/Fido.md', char_sheet(
            'Fido', assets=ASSET_HEAD + "\n| spring | f/a.png | h1 | 1 |"
                          "\n| spring | f/b.png | h2 | 1 |"))
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_two_sheets_claiming_one_name_fail_naming_both_files(self):
        self.put('reference/sheets/2001 Alice.md', char_sheet('Alice'))
        result = self.world()
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any('1001 Alice.md' in l and '2001 Alice.md' in l
                            for l in self.fails(result)), result.stdout)


class AliasTests(CheckerCase):
    def setUp(self):
        super().setUp()
        self.put('reference/sheets/1001 Alice.md',
                 ALICE_SHEET.replace('description: x\n',
                                     'description: x\naliases: [Allie, '
                                     'Alice Liddell]\n'))
        self.put('reference/sheets/1002 Bob.md',
                 BOB_SHEET.replace('description: x\n',
                                   'description: x\naliases: [Robert]\n'))

    def card_names(self, rel, bob=None):
        if bob is not None:
            self.put('notes/Bob.md', bob_note(relationships=bob))
        self.put('notes/Alice.md', alice_note(relationships=rel))

    def test_a_one_sided_relationship_under_an_alias_passes(self):
        self.card_names("- **ROBERT:** She trusts him.")
        self.put('notes/Bob.md', bob_note(
            ledger="| Background | 1 | claim | bob-source.md | |\n"
                   "| Soul | 1 | claim | bob-source.md | |",
            relationships=""))
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.fails(result), [])
        self.assertEqual([l for l in result.stdout.splitlines()
                          if l.startswith('PENDING')], [])

    def test_a_mirror_written_under_an_alias_satisfies_the_check(self):
        self.card_names("- **Bob:** She trusts him.",
                        bob="- **allie — Friend:** He waves.")
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_a_relationship_under_an_alias_with_a_mirror_passes(self):
        self.card_names("- **Robert:** She trusts him.",
                        bob="- **Alice Liddell:** He waves.")
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_a_card_filed_under_an_alias_is_mirrored_by_canonical_names(self):
        os.remove(os.path.join(self.root, 'notes', 'Alice.md'))
        self.put('notes/Allie.md', alice_note().replace(
            'title: Alice', 'title: Allie'))
        result = self.world()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual([l for l in result.stdout.splitlines()
                          if l.startswith('PENDING')], [])


class ExportIdentityTests(CheckerCase):
    good = ExportModeTests.good

    def setUp(self):
        super().setUp()
        self.put('notes/Rex.md', NOTE.format(
            name='Rex', ledger='', background='', preamble='', body='',
            soul='', relationships='', voice='', seeds=''))
        self.put('reference/sheets/1002 Bob.md',
                 BOB_SHEET.replace('description: x\n',
                                   'description: x\naliases: [Robert]\n'))

    def test_an_exported_alias_resolves_to_the_card_and_the_sheet(self):
        chars = self.good()
        chars[1]['name'] = 'robert'
        self.assertEqual(self.export(chars).returncode, 0)
        chars[1]['role'] = 'Village baker'
        result = self.export(chars)
        self.assertTrue(any('smith' in l for l in self.fails(result)),
                        result.stdout)

    def test_a_single_string_alias_resolves_in_export_mode(self):
        self.put('reference/sheets/1002 Bob.md',
                 BOB_SHEET.replace('description: x\n',
                                   'description: x\naliases: Robert\n'))
        chars = self.good()
        chars[1]['name'] = 'robert'
        self.assertEqual(self.export(chars).returncode, 0)
        chars[1]['role'] = 'Village baker'
        result = self.export(chars)
        self.assertTrue(any('smith' in l for l in self.fails(result)),
                        result.stdout)

    def test_a_sheet_name_loses_only_its_leading_number(self):
        self.put('reference/sheets/1076 Sakura Laurel.md',
                 char_sheet('Sakura Laurel'))
        self.put('notes/Sakura Laurel.md', alice_note().replace(
            'title: Alice', 'title: Sakura Laurel'))
        chars = self.good() + [{'name': 'Sakura Laurel', 'role': '',
                                'appearance': 'Red hair. Green eyes.'}]
        result = self.export(chars)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn('no character sheet', result.stdout)

    def test_an_owner_written_under_an_alias_passes(self):
        chars = self.good()
        chars[2]['spriteSets'][0]['description'] = 'Pet of Robert, sitting'
        result = self.export(chars)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_an_ownership_row_in_a_world_file_counts_as_an_owner(self):
        self.put('reference/sheets/world 2 more.md', WORLD_TWO.replace(
            '| small |  |', '| small | b |'))
        chars = self.good()
        chars[2]['spriteSets'][0]['description'] = 'Pet of Mary, sitting'
        result = self.export(chars)
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == '__main__':
    unittest.main()
