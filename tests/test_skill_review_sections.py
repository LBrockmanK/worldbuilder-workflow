"""Tests that every skill file holds exactly one Review section.

The critic and the completion checks read the `## Review` section of each
`skills/*/SKILL.md`. A skill with none, or with two, breaks that reading.
The count matches whole lines equal to `## Review` and skips fenced code
blocks, so `## Review criteria`, a backticked mention in prose and a heading
inside an example block do not count.
"""
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, 'skills')


def count_review_headings(text):
    """Count the lines equal to `## Review` outside fenced code blocks."""
    count = 0
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith('```') or stripped.startswith('~~~'):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.rstrip() == '## Review':
            count += 1
    return count


def test_each_skill_has_exactly_one_review_section():
    paths = sorted(glob.glob(os.path.join(SKILLS, '*', 'SKILL.md')))
    assert paths, 'no skills/*/SKILL.md files found'
    wrong = {}
    for path in paths:
        with open(path, encoding='utf-8') as handle:
            found = count_review_headings(handle.read())
        if found != 1:
            wrong[os.path.relpath(path, ROOT)] = found
    assert not wrong, f'skills without exactly one ## Review section: {wrong}'


def test_count_ignores_fenced_and_prose_mentions():
    assert count_review_headings('# Skill\n\nBody only.\n') == 0
    assert count_review_headings('## Review\ntext\n## Review\n') == 2
    assert count_review_headings('## Review\ntext\n') == 1
    fenced = '## Review\n\n```\n## Review\n```\n'
    assert count_review_headings(fenced) == 1
    prose = 'Open the `## Review criteria` section.\n\n## Review criteria\n'
    assert count_review_headings(prose) == 0
    assert count_review_headings('## Review   \n') == 1
