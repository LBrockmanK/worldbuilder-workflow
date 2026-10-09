"""Tests for create_project_docs.py. Run: python tests/test_create_project_docs.py

The script lays down a new worldbuilder project: the three project
documents under `project/`. These tests run it against a
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
                         {'project'})

    def test_the_three_project_documents_are_written(self):
        self.assertEqual(
            set(os.listdir(os.path.join(self.root, 'project'))),
            {'foundation.md', 'plan.md', 'direction.md'})

    def test_the_project_documents_are_born_with_empty_tags(self):
        for name in ('foundation', 'plan', 'direction'):
            with open(os.path.join(self.root, 'project', f'{name}.md'),
                      encoding='utf-8') as f:
                front, _ = split_front_matter(f.read())
            self.assertEqual(front['tags'], [], name)

    def test_the_plan_keeps_its_cast_plan_and_has_no_phase_status(self):
        with open(os.path.join(self.root, 'project', 'plan.md'),
                  encoding='utf-8') as f:
            text = f.read()
        self.assertIn('## Cast Plan', text)
        self.assertNotIn('## Phase Status', text)

    def test_a_second_run_refuses_rather_than_overwriting(self):
        second = run(self.root)
        self.assertEqual(second.returncode, 1)


class ExportDiffLookupTests(unittest.TestCase):
    """export_diff.py needs a .sbworld to get any further, so these tests
    check the foundation lookup, the narrowest point a small fixture
    reaches: with project/foundation.md the run gets past it and stops at
    the missing .sbworld; with only project/seed.md it stops at the
    lookup and names foundation.md."""

    EXPORT_DIFF = os.path.join(ROOT, 'scripts', 'export_diff.py')

    def run_diff(self, filename):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        project = os.path.join(tmp.name, 'world', 'project')
        os.makedirs(project)
        os.makedirs(os.path.join(tmp.name, 'exports', 'ainime'))
        with open(os.path.join(project, filename), 'w',
                  encoding='utf-8') as f:
            f.write('# Foundation' + chr(10))
        return subprocess.run([sys.executable, self.EXPORT_DIFF, tmp.name],
                              capture_output=True, text=True)

    def test_foundation_md_passes_the_lookup(self):
        r = self.run_diff('foundation.md')
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn('foundation.md not found', r.stderr)
        self.assertIn('.sbworld', r.stderr)

    def test_only_seed_md_fails_naming_foundation_md(self):
        r = self.run_diff('seed.md')
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('foundation.md not found', r.stderr)


if __name__ == '__main__':
    unittest.main()
