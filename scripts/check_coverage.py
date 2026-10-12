#!/usr/bin/env python3
"""Check a world's coverage ledgers and reference sheet.

Implements the checks of skills/source-extraction-standard.md that a script
can make. It reads meaning nowhere: whether a source supports a claim stays
with the writer and the critic.

Usage:
    python check_coverage.py world  --world-root <root>
    python check_coverage.py export --world-root <root> --world-json <file>

`world` mode checks every character note's coverage ledger, and the
reference sheet (contradictions, asset inventory), and the mirrored
relationships between cards. `export` mode compares the derived fields of an
exported world.json (`role`, `appearance`, `spriteSets[].description`) with
the reference sheet and the cards.

Report lines start with FAIL, FLAGGED or PENDING. FAIL lines make the exit
code 1. FLAGGED lists ledger rows marked flagged, and PENDING lists
relationships that name a cast member with no note yet; neither fails.
Standard library only, plus pyyaml for the note frontmatter.
"""

import argparse
import json
import os
import re
import sys

import yaml

SHEET_NAME = 'Reference sheet.md'
LEDGER_HEADING = 'Coverage ledger'
CARD_SECTIONS = ['Background', 'Body', 'Soul', 'Relationships',
                 'Intimate Dynamics', 'Voice / Dialogue', 'Story Seeds']


# -- markdown reading ---------------------------------------------------

def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read().replace('\r\n', '\n')


def split_front_matter(text):
    if text.startswith('---\n'):
        end = text.find('\n---', 4)
        if end != -1:
            try:
                front = yaml.safe_load(text[4:end]) or {}
            except yaml.YAMLError:
                front = {}
            return front, text[end + 4:].lstrip('\n')
    return {}, text


def sections(text, level):
    """Split text on headings of the given level into {title: lines}.

    Lines before the first heading of that level are dropped. A heading of a
    shallower level also ends the current section.
    """
    out, title, lines = {}, None, []
    marker = '#' * level + ' '
    for line in text.split('\n'):
        m = re.match(r'(#+) ', line)
        if m and len(m.group(1)) <= level:
            if title is not None:
                out[title] = lines
            title = line[len(marker):].strip() if line.startswith(marker) else None
            lines = []
        elif title is not None:
            lines.append(line)
    if title is not None:
        out[title] = lines
    return out


def table_rows(lines):
    """Return (header, rows) for the first markdown table in lines; each row
    is a dict keyed by header. A missing table gives ([], [])."""
    rows = [[c.strip() for c in l.strip().strip('|').split('|')]
            for l in lines if l.strip().startswith('|')]
    rows = [r for r in rows if not all(re.fullmatch(r':?-+:?', c) for c in r)]
    if not rows:
        return [], []
    header = rows[0]
    return header, [dict(zip(header, r)) for r in rows[1:]]


def normalize(text):
    return ' '.join(text.split())


# -- notes ----------------------------------------------------------------

class Note:
    def __init__(self, path):
        self.name = os.path.splitext(os.path.basename(path))[0]
        front, body = split_front_matter(read(path))
        self.front = front
        top = sections(body, 2)
        self.sections = {k: v for k, v in top.items()}
        self.ledger = self._ledger()
        self.entries = {}
        self.preamble = ''
        for title in CARD_SECTIONS:
            if title not in self.sections:
                continue
            lines = self.sections[title]
            bullets = [re.sub(r'^[-*]\s+', '', l) for l in lines
                       if re.match(r'[-*]\s+\S', l)]
            self.entries[title] = bullets
            if title == 'Body':
                self.preamble = self._preamble(lines)

    def _preamble(self, lines):
        kept = []
        for l in lines:
            if re.match(r'[-*](\s|$)', l):
                break
            s = l.strip()
            if not s or re.fullmatch(r'_.*_', s):
                continue
            kept.append(s)
        return normalize(' '.join(kept))

    def _ledger(self):
        design = self.sections.get('Design Notes')
        if design is None:
            return None
        subs = sections('\n'.join(design), 3)
        # sections() keys on '### ' headings inside the Design Notes lines
        sub = _sub_sections(design)
        lines = sub.get(LEDGER_HEADING)
        if lines is None:
            return None
        _, rows = table_rows(lines)
        return rows

    def is_character(self):
        kind = str(self.front.get('type', '')).strip('[] ')
        return kind == 'character'

    def preamble_clauses(self):
        if not self.preamble:
            return []
        return [s for s in re.split(r'(?<=[.;!?])\s+', self.preamble) if s]

    def expected_entries(self):
        keys = []
        for title, bullets in self.entries.items():
            keys += [(title, str(i + 1)) for i in range(len(bullets))]
        keys += [('Body', f'preamble {i + 1}')
                 for i in range(len(self.preamble_clauses()))]
        return keys

    def relationship_names(self):
        names = []
        for bullet in self.entries.get('Relationships', []):
            m = re.match(r'\*\*(.+?)\*\*', bullet)
            if m:
                label = m.group(1).rstrip(':').strip()
                names.append(re.split(r'\s+[—–-]\s+|:', label)[0].strip())
        return names


def _sub_sections(lines):
    """Map '### ' heading titles to their lines inside a section's lines."""
    out, title, buf = {}, None, []
    for line in lines:
        if line.startswith('### '):
            if title is not None:
                out[title] = buf
            title, buf = line[4:].strip(), []
        elif title is not None:
            buf.append(line)
    if title is not None:
        out[title] = buf
    return out


# -- the reference sheet --------------------------------------------------

class Sheet:
    def __init__(self, path):
        _, body = split_front_matter(read(path))
        top = sections(body, 2)
        chars = _sub_sections(top.get('Characters', []))
        self.cast = list(chars)
        self.occupations = {}
        for name, lines in chars.items():
            subs = _sub_sections_h4(lines)
            _, rows = table_rows(subs.get('Occupations', []))
            self.occupations[name.casefold()] = [
                r.get('Occupation', '') for r in rows if r.get('Occupation')]
        _, self.connections = table_rows(top.get('Connections', []))
        self.contradiction_header, self.contradictions = table_rows(
            top.get('Contradictions', []))
        self.assets = {}
        for name, lines in _sub_sections(top.get('Asset inventory', [])).items():
            _, rows = table_rows(lines)
            self.assets[name] = rows

    def owners_of(self, name):
        return {r['From'] for r in self.connections
                if r.get('Kind', '').casefold() == 'ownership'
                and r.get('To', '').casefold() == name.casefold()}


def _sub_sections_h4(lines):
    out, title, buf = {}, None, []
    for line in lines:
        if line.startswith('#### '):
            if title is not None:
                out[title] = buf
            title, buf = line[5:].strip(), []
        elif title is not None:
            buf.append(line)
    if title is not None:
        out[title] = buf
    return out


# -- the checks -------------------------------------------------------------

class Report:
    def __init__(self):
        self.fails, self.flagged, self.pending = [], [], []

    def fail(self, msg):
        self.fails.append(msg)

    def lines(self):
        out = ([f'FAIL {m}' for m in self.fails]
               + [f'FLAGGED {m}' for m in self.flagged]
               + [f'PENDING {m}' for m in self.pending])
        out.append(f'{len(self.fails)} failure(s), {len(self.flagged)} '
                   f'flagged, {len(self.pending)} pending')
        return out


def load_world(root):
    notes = {}
    notes_dir = os.path.join(root, 'notes')
    if os.path.isdir(notes_dir):
        for fn in sorted(os.listdir(notes_dir)):
            if fn.endswith('.md'):
                note = Note(os.path.join(notes_dir, fn))
                if note.is_character():
                    notes[note.name.casefold()] = note
    sheet_path = os.path.join(root, 'reference', SHEET_NAME)
    sheet = Sheet(sheet_path) if os.path.isfile(sheet_path) else None
    return notes, sheet


def source_exists(root, item):
    item = item.strip().strip('[]')
    item = item.split('|')[0].split('#')[0].strip()
    if item.startswith('reference/'):
        item = item[len('reference/'):]
    return bool(item) and os.path.isfile(
        os.path.join(root, 'reference', *item.split('/')))


def check_ledger(root, note, report):
    if note.ledger is None:
        report.fail(f'{note.name}: no "### {LEDGER_HEADING}" under Design Notes')
        return
    rows = {}
    for row in note.ledger:
        key = (row.get('Section', ''), row.get('Entry', ''))
        rows[key] = row
    expected = set(note.expected_entries())
    for key in note.expected_entries():
        if key not in rows:
            report.fail(f'{note.name}: {key[0]} {key[1]} has no ledger row')
    for key, row in rows.items():
        if key not in expected:
            report.fail(f'{note.name}: ledger row {key[0]} {key[1]}: '
                        'no such entry in the note')
            continue
        source = row.get('Source', '').strip()
        if source.casefold() == 'flagged':
            report.flagged.append(f'{note.name}: {key[0]} {key[1]} has no '
                                  'source and is returned to the human')
        elif not source:
            report.fail(f'{note.name}: ledger row {key[0]} {key[1]} names no '
                        'source (write the source, or mark the row flagged)')
        else:
            for item in source.split(';'):
                if not source_exists(root, item):
                    report.fail(f'{note.name}: ledger row {key[0]} {key[1]} '
                                f'names {item.strip()}, which is not under '
                                'reference/')


def check_sheet(sheet, report):
    sources = [h for h in sheet.contradiction_header
               if h.casefold().startswith('source')]
    for row in sheet.contradictions:
        count = sum(1 for h in sources if row.get(h, '').strip())
        if count < 2:
            report.fail(f'Contradictions: "{row.get("Fact", "")}" has '
                        f'{count} source(s); a contradiction needs two')
    for name, rows in sheet.assets.items():
        sets = {}
        for r in rows:
            sets.setdefault(r.get('Set', ''), set()).add(r.get('Hash', ''))
        names = list(sets)
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                if sets[a] == sets[b]:
                    report.fail(f'Asset inventory: {name}: sets "{a}" and '
                                f'"{b}" have identical file hashes; record '
                                'them as one set')


def check_mirrors(notes, sheet, report):
    cast = {n.casefold() for n in sheet.cast} if sheet else set()
    for note in notes.values():
        for other in note.relationship_names():
            key = other.casefold()
            if key == note.name.casefold():
                continue
            if key in notes:
                back = [n.casefold() for n in notes[key].relationship_names()]
                if note.name.casefold() not in back:
                    report.fail(f'Relationships: {note.name} names {other}, '
                                f'but {notes[key].name} has no mirror entry '
                                f'naming {note.name}')
            elif key in cast:
                report.pending.append(f'{note.name} names {other}, who has '
                                      'no note yet; mirror pending')


def check_world(root):
    report = Report()
    notes, sheet = load_world(root)
    for note in notes.values():
        check_ledger(root, note, report)
    if sheet is None:
        report.fail(f'reference/{SHEET_NAME} does not exist')
    else:
        check_sheet(sheet, report)
    check_mirrors(notes, sheet, report)
    return report


def check_export(root, world_json):
    report = Report()
    notes, sheet = load_world(root)
    if sheet is None:
        report.fail(f'reference/{SHEET_NAME} does not exist')
        return report
    with open(world_json, encoding='utf-8') as f:
        data = json.load(f)
    for char in data.get('characters', []):
        name = char.get('name', '')
        note = notes.get(name.casefold())
        role = char.get('role', '').casefold()
        for occ in sheet.occupations.get(name.casefold(), []):
            if occ.casefold() not in role:
                report.fail(f'{name}: role lacks the occupation "{occ}" '
                            'that the reference sheet lists')
        appearance = char.get('appearance')
        if (appearance and note is not None
                and normalize(appearance) != note.preamble):
            report.fail(f'{name}: appearance differs from the note\'s '
                        'Body preamble')
        owners = {o.casefold() for o in sheet.owners_of(name)}
        if owners:
            for sset in char.get('spriteSets', []):
                text = sset.get('description', '')
                for other in sheet.cast:
                    if (other.casefold() in owners
                            or other.casefold() == name.casefold()):
                        continue
                    n = re.escape(other)
                    pattern = (rf"\b{n}['’]s\b|owned by {n}\b|"
                               rf"belongs to {n}\b|pet of {n}\b")
                    if re.search(pattern, text, re.IGNORECASE):
                        report.fail(f'{name}: sprite set '
                                    f'"{sset.get("name", "")}" description '
                                    f'names {other} as owner; the reference '
                                    'sheet lists '
                                    + ', '.join(sorted(sheet.owners_of(name))))
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = parser.add_subparsers(dest='mode', required=True)
    for mode in ('world', 'export'):
        p = sub.add_parser(mode)
        p.add_argument('--world-root', required=True)
        if mode == 'export':
            p.add_argument('--world-json', required=True)
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if args.mode == 'world':
        report = check_world(args.world_root)
    else:
        report = check_export(args.world_root, args.world_json)
    print('\n'.join(report.lines()))
    return 1 if report.fails else 0


if __name__ == '__main__':
    sys.exit(main())
