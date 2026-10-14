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



class ExportDiffDurabilityAndLayoutTests(unittest.TestCase):

    def make_root(self, nested):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = tmp.name
        base = os.path.join(root, 'world') if nested else root
        os.makedirs(os.path.join(base, 'project'))
        with open(os.path.join(base, 'project', 'foundation.md'), 'w',
                  encoding='utf-8', newline='\n') as f:
            f.write(FOUNDATION)
        exports = os.path.join(root, 'exports', 'ainime')
        os.makedirs(exports)
        with open(os.path.join(exports, 'world.json'), 'w',
                  encoding='utf-8') as f:
            json.dump({'settingSummary': 'old'}, f, indent=2)
        return root, exports

    def run_diff(self, root, *args):
        return subprocess.run([sys.executable, SCRIPT, root, *args],
                              capture_output=True, text=True)

    def test_project_directly_under_the_root_is_found(self):
        root, exports = self.make_root(nested=False)
        r = self.run_diff(root, '--apply', 'settingSummary')
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(os.path.join(exports, 'world.json'), encoding='utf-8') as f:
            self.assertEqual(json.load(f)['settingSummary'],
                             'A new summary of the world.')

    def test_nested_project_is_the_fallback(self):
        root, exports = self.make_root(nested=True)
        r = self.run_diff(root, '--apply', 'settingSummary')
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_a_failed_replace_leaves_the_original_and_no_temp_file(self):
        import importlib.util
        from unittest import mock
        spec = importlib.util.spec_from_file_location('export_diff', SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        root, exports = self.make_root(nested=False)
        path = os.path.join(exports, 'world.json')
        with open(path, 'rb') as f:
            before = f.read()
        with mock.patch.object(mod.os, 'replace', side_effect=OSError('disk')):
            with self.assertRaises(OSError):
                mod.save_world(path, {'settingSummary': 'new'}, '\n', False)
        with open(path, 'rb') as f:
            self.assertEqual(f.read(), before)
        self.assertEqual(os.listdir(exports), ['world.json'])

    def test_a_colliding_temp_name_is_left_alone(self):
        import importlib.util
        from unittest import mock
        spec = importlib.util.spec_from_file_location('export_diff', SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        root, exports = self.make_root(nested=False)
        path = os.path.join(exports, 'world.json')
        other = os.path.join(exports, 'world.json.tmp')
        with open(other, 'wb') as f:
            f.write(b'another run')
        with mock.patch.object(mod.os, 'replace', side_effect=OSError('disk')):
            with self.assertRaises(OSError):
                mod.save_world(path, {'a': 1}, chr(10), False)
        with open(other, 'rb') as f:
            self.assertEqual(f.read(), b'another run')
        mod.save_world(path, {'a': 1}, chr(10), False)
        with open(other, 'rb') as f:
            self.assertEqual(f.read(), b'another run')


if __name__ == '__main__':
    unittest.main()
