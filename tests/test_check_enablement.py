"""Tests for check_enablement.py. Run: python tests/test_check_enablement.py

The script decides whether plugins are enabled for a session root, reading the
root's committed and local settings and the user-level settings. Each test
builds a temporary session root plus a temporary user settings file and asserts
on the exit code and output lines.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, 'scripts', 'check_enablement.py')
PLUGINS = ['scraibe', 'worldbuilder-workflow']


class CheckEnablementTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = os.path.join(self._tmp.name, 'session')
        os.makedirs(os.path.join(self.root, '.claude'))
        self.user = os.path.join(self._tmp.name, 'user-settings.json')

    def _write(self, path, data, bom=False):
        with open(path, 'w', encoding='utf-8-sig' if bom else 'utf-8') as f:
            f.write(data if isinstance(data, str) else json.dumps(data))

    def committed(self, plugins=None, raw=None):
        path = os.path.join(self.root, '.claude', 'settings.json')
        if raw is not None:
            self._write(path, raw)
        elif plugins is None:
            self._write(path, {})
        else:
            self._write(path, {'enabledPlugins': plugins})

    def local(self, plugins):
        self._write(os.path.join(self.root, '.claude', 'settings.local.json'),
                    {'enabledPlugins': plugins})

    def user_file(self, plugins, bom=False):
        self._write(self.user, {'enabledPlugins': plugins}, bom=bom)

    def run_check(self, *plugins):
        r = subprocess.run(
            [sys.executable, SCRIPT, '--session-root', self.root,
             '--user-settings', self.user, *(plugins or PLUGINS)],
            capture_output=True, text=True, encoding='utf-8')
        return r.returncode, r.stdout, r.stderr

    def verdicts(self, out):
        rows = {}
        for line in out.splitlines():
            parts = line.split('\t')
            if len(parts) == 3:
                rows[parts[0]] = (parts[1], parts[2])
        return rows

    def test_a_project_true_user_absent(self):
        self.committed({'scraibe@m': True, 'worldbuilder-workflow@m': True})
        code, out, _ = self.run_check()
        self.assertEqual(code, 0)
        self.assertEqual(self.verdicts(out), {
            'scraibe': ('enabled', 'project'),
            'worldbuilder-workflow': ('enabled', 'project')})

    def test_b_no_selection_stops(self):
        self.committed(None)
        self.user_file({'scraibe@m': True, 'worldbuilder-workflow@m': True})
        code, out, err = self.run_check()
        self.assertEqual(code, 1)
        text = (out + err).lower()
        self.assertIn('no plugin selection', text)
        self.assertIn('fleet:setup', text)

    def test_c_empty_project_user_true(self):
        self.committed({})
        self.user_file({'scraibe@m': True, 'worldbuilder-workflow@m': True})
        code, out, _ = self.run_check()
        self.assertEqual(code, 0)
        self.assertEqual(self.verdicts(out), {
            'scraibe': ('enabled', 'user'),
            'worldbuilder-workflow': ('enabled', 'user')})

    def test_d_one_plugin_missing(self):
        self.committed({})
        self.user_file({'scraibe@m': True})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        rows = self.verdicts(out)
        self.assertEqual(rows['scraibe'], ('enabled', 'user'))
        self.assertEqual(rows['worldbuilder-workflow'][0], 'missing')
        self.assertIn('fleet:setup', out)

    def test_e_local_disable_beats_user(self):
        self.committed({'scraibe@m': True, 'worldbuilder-workflow@m': True})
        self.local({'worldbuilder-workflow@m': False})
        self.user_file({'scraibe@m': True, 'worldbuilder-workflow@m': True})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        rows = self.verdicts(out)
        self.assertEqual(rows['worldbuilder-workflow'][0], 'disabled')
        self.assertEqual(rows['scraibe'][0], 'enabled')
        self.assertIn('fleet:setup', out)
        self.assertIn('clear the disable through fleet:setup', out)

    def test_f_user_false_is_not_enabled(self):
        self.committed({})
        self.user_file({'scraibe@m': False, 'worldbuilder-workflow@m': True})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertEqual(self.verdicts(out)['scraibe'][0], 'missing')

    def test_g_suffix_differs_between_layers(self):
        self.committed({'scraibe@other': False, 'worldbuilder-workflow@m': True})
        self.user_file({'scraibe@harness': True})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertEqual(self.verdicts(out)['scraibe'][0], 'disabled')

    def test_g2_project_same_layer_conflict(self):
        self.committed({'scraibe@a': True, 'scraibe@b': False,
                        'worldbuilder-workflow@m': True})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertEqual(self.verdicts(out)['scraibe'], ('disabled', 'project'))

    def test_g3_user_same_layer_conflict(self):
        self.committed({})
        self.user_file({'scraibe@a': True, 'scraibe@b': False,
                        'worldbuilder-workflow@m': True})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertEqual(self.verdicts(out)['scraibe'][0], 'missing')

    def test_h_user_file_with_bom(self):
        self.committed({})
        self.user_file({'scraibe@m': True, 'worldbuilder-workflow@m': True},
                       bom=True)
        code, _, _ = self.run_check()
        self.assertEqual(code, 0)

    def test_i_non_object_file_exits_2(self):
        self.committed(raw='[1, 2]')
        code, out, err = self.run_check()
        self.assertEqual(code, 2)
        self.assertIn('settings.json', out + err)

    def test_j_writes_nothing(self):
        self.committed({})
        self.user_file({'scraibe@m': True})

        def snapshot():
            snap = {}
            for d, _, files in os.walk(self._tmp.name):
                for n in files:
                    p = os.path.join(d, n)
                    with open(p, 'rb') as f:
                        snap[p] = f.read()
            return snap
        before = snapshot()
        self.run_check()
        self.assertEqual(before, snapshot())


if __name__ == '__main__':
    unittest.main()
