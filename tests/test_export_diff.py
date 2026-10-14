"""Tests for export_diff.py: the diff workflow over the versioned world.json.

The project keeps world.json under exports/ainime/ and builds the .sbworld
archive from it with sbworld_tool.py. export_diff.py reads and writes the
versioned world.json only and never touches an archive.
Run: python -m pytest tests/test_export_diff.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, 'scripts', 'export_diff.py')

FOUNDATION = (
    '# Foundation\n\n'
    '## Setting Summary\n\nA new summary of the world.\n\n'
    '## Community\n\nA new community blurb.\n'
)


class ExportDiffApplyTests(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = tmp.name
        project = os.path.join(self.root, 'world', 'project')
        os.makedirs(project)
        with open(os.path.join(project, 'foundation.md'), 'w',
                  encoding='utf-8', newline='\n') as f:
            f.write(FOUNDATION)
        self.exports = os.path.join(self.root, 'exports', 'ainime')
        os.makedirs(self.exports)
        self.world_path = os.path.join(self.exports, 'world.json')
        self.world = {
            'settingSummary': 'An old summary.',
            'communityDescription': 'An old blurb.',
            'characters': [{'name': 'Adeline', 'baseProfile': 'kept'}],
        }
        self.write_world(self.world)

    def write_world(self, world, eol='\r\n', trailing=False):
        text = json.dumps(world, indent=2, ensure_ascii=False)
        if trailing:
            text += '\n'
        with open(self.world_path, 'wb') as f:
            f.write(text.replace('\n', eol).encode('utf-8'))

    def read_world_bytes(self):
        with open(self.world_path, 'rb') as f:
            return f.read()

    def run_diff(self, *args):
        return subprocess.run([sys.executable, SCRIPT, self.root, *args],
                              capture_output=True, text=True)

    def test_diff_alone_writes_nothing(self):
        before = self.read_world_bytes()
        r = self.run_diff()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('settingSummary', r.stdout)
        self.assertEqual(self.read_world_bytes(), before)

    def test_apply_changes_only_the_named_field(self):
        r = self.run_diff('--apply', 'settingSummary')
        self.assertEqual(r.returncode, 0, r.stderr)
        after = json.loads(self.read_world_bytes())
        self.assertEqual(after['settingSummary'], 'A new summary of the world.')
        self.assertEqual(after['communityDescription'], 'An old blurb.')
        self.assertEqual(after['characters'], self.world['characters'])

    def test_apply_keeps_line_endings_and_trailing_newline(self):
        self.write_world(self.world, eol='\r\n', trailing=False)
        self.run_diff('--apply', 'settingSummary')
        raw = self.read_world_bytes()
        self.assertIn(b'\r\n', raw)
        self.assertFalse(raw.endswith(b'\n'))
        self.write_world(self.world, eol='\n', trailing=True)
        self.run_diff('--apply', 'settingSummary')
        raw = self.read_world_bytes()
        self.assertNotIn(b'\r', raw)
        self.assertTrue(raw.endswith(b'\n'))

    def test_apply_writes_no_sbworld_and_leaves_an_existing_one_alone(self):
        archive = os.path.join(self.exports, 'World.sbworld')
        with open(archive, 'wb') as f:
            f.write(b'an archive this script must not touch')
        r = self.run_diff('--apply-all')
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(archive, 'rb') as f:
            self.assertEqual(f.read(), b'an archive this script must not touch')
        self.assertEqual(sorted(os.listdir(self.exports)),
                         ['World.sbworld', 'world.json'])

    def test_missing_world_json_fails_naming_it(self):
        os.remove(self.world_path)
        r = self.run_diff()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('world.json', r.stderr)

    def test_the_script_does_not_import_zipfile(self):
        with open(SCRIPT, encoding='utf-8') as f:
            self.assertNotIn('import zipfile', f.read())


if __name__ == '__main__':
    unittest.main()
