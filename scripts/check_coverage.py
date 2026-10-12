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
code 1. FLAGGED lists ledger rows for claims left unwritten for want of a
source, and PENDING lists relationships that name a cast member with no note
yet; neither fails. Standard library only, plus pyyaml for the note
frontmatter.
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
# Sections whose entries are labelled blocks (card-format.md): an entry
# starts at a bullet, a bold title line or a #### heading.
BLOCK_SECTIONS = {'Voice / Dialogue', 'Story Seeds'}
PET_WORDS = (['pet', 'dog', 'cat', 'horse', 'chicken', 'bird', 'animal', 'companion', 'familiar', 'mount', 'puppy', 'kitten', 'goat', 'sheep', 'cow', 'pig', 'rabbit', 'duck', 'hen', 'rooster', 'donkey', 'llama', 'alpaca', 'fish', 'turtle', 'lizard', 'snake', 'ferret', 'hamster', 'mouse', 'rat'])
PET_NOUNS = '|'.join(PET_WORDS)


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


def sections(lines, level):
    """Map the titles of headings of exactly `level` to their lines, up to
    the next heading of the same or a shallower level."""
    if isinstance(lines, str):
        lines = lines.split('\n')
    out, title, buf = {}, None, []
    for line in lines:
        m = re.match(r'(#+) (.*)', line)
        if m and len(m.group(1)) <= level:
            if title is not None:
                out[title] = buf
            title = m.group(2).strip() if len(m.group(1)) == level else None
            buf = []
        elif title is not None:
            buf.append(line)
    if title is not None:
        out[title] = buf
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

def split_entries(title, lines):
    """Return the entries of a card section as lists of lines."""
    if title in BLOCK_SECTIONS:
        start = re.compile(r'([-*]\s+\S|\*\*|#### )')
    else:
        start = re.compile(r'[-*]\s+\S')
    entries = []
    for line in lines:
        if start.match(line):
            entries.append([line])
        elif entries:
            entries[-1].append(line)
    return entries


class Note:
    def __init__(self, path):
        self.name = os.path.splitext(os.path.basename(path))[0]
        front, body = split_front_matter(read(path))
        self.front = front
        self.sections = sections(body, 2)
        self.ledger = self._ledger()
        self.entries = {}
        self.preamble = ''
        for title in CARD_SECTIONS:
            if title not in self.sections:
                continue
            lines = self.sections[title]
            self.entries[title] = split_entries(title, lines)
            if title == 'Body':
                self.preamble = self._preamble(lines)

    @staticmethod
    def _preamble(lines):
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
        lines = sections(design, 3).get(LEDGER_HEADING)
        if lines is None:
            return None
        return table_rows(lines)[1]

    def is_character(self):
        return str(self.front.get('type', '')).strip('[] ') == 'character'

    def preamble_clauses(self):
        return [s for s in re.split(r'(?<=[.;!?])\s+', self.preamble) if s]

    def expected_entries(self):
        keys = []
        for title, entries in self.entries.items():
            keys += [(title, str(i + 1)) for i in range(len(entries))]
        keys += [('Body', f'preamble {i + 1}')
                 for i in range(len(self.preamble_clauses()))]
        return keys

    def relationship_names(self):
        names = []
        for entry in self.entries.get('Relationships', []):
            first = re.sub(r'^[-*]\s+', '', entry[0])
            m = re.match(r'\*\*(.+?)\*\*', first)
            if m:
                label = m.group(1).rstrip(':').strip()
                names.append(re.split(r'\s+[—–-]\s+|:', label)[0].strip())
        return names


# -- the reference sheet --------------------------------------------------

class Sheet:
    def __init__(self, path):
        _, body = split_front_matter(read(path))
        top = sections(body, 2)
        chars = sections(top.get('Characters', []), 3)
        self.cast = list(chars)
        self.occupations = {}
        for name, lines in chars.items():
            rows = table_rows(sections(lines, 4).get('Occupations', []))[1]
            self.occupations[name.casefold()] = [
                r.get('Occupation', '') for r in rows if r.get('Occupation')]
        self.connections = table_rows(top.get('Connections', []))[1]
        self.contradiction_header, self.contradictions = table_rows(
            top.get('Contradictions', []))
        self.assets = {name: table_rows(lines)[1] for name, lines in
                       sections(top.get('Asset inventory', []), 3).items()}

    def owners_of(self, name):
        return {r['From'] for r in self.connections
                if r.get('Kind', '').casefold() == 'ownership'
                and r.get('To', '').casefold() == name.casefold()}


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
    """True when `item` is a file that resolves to a place inside the
    world's reference/ folder."""
    item = item.strip().strip('[]').split('|')[0].split('#')[0].strip()
    if item.startswith('reference/'):
        item = item[len('reference/'):]
    if not item:
        return False
    base = os.path.realpath(os.path.join(root, 'reference'))
    target = os.path.realpath(os.path.join(base, *item.split('/')))
    try:
        inside = os.path.commonpath([base, target]) == base
    except ValueError:  # a path on another drive
        return False
    return inside and os.path.isfile(target)


def entry_key(entry):
    """Split a ledger Entry cell into (entry, claim suffix)."""
    m = re.fullmatch(r'(preamble \d+|\d+|unwritten)(?:[. ](\S+))?',
                     entry.strip())
    return (m.group(1), m.group(2)) if m else (entry.strip(), None)


def check_ledger(root, note, report):
    if note.ledger is None:
        report.fail(f'{note.name}: no "### {LEDGER_HEADING}" under Design Notes')
        return
    expected = set(note.expected_entries())
    covered, seen = set(), set()
    for row in note.ledger:
        section = row.get('Section', '')
        raw = row.get('Entry', '').strip()
        entry, _ = entry_key(raw)
        source = row.get('Source', '').strip()
        claim = row.get('Claim', '').strip()
        label = f'{section} {raw}'
        if (section, raw) in seen:
            report.fail(f'{note.name}: ledger key {label} appears twice')
        seen.add((section, raw))
        flagged = source.casefold() == 'flagged'
        if entry == 'unwritten':
            if not flagged:
                report.fail(f'{note.name}: ledger row {label} is unwritten '
                            'and must have Source flagged')
            else:
                report.flagged.append(
                    f'{note.name}: {section}: "{claim}" has no source and is '
                    'not written; returned to the human')
            continue
        if (section, entry) not in expected:
            report.fail(f'{note.name}: ledger row {label}: '
                        'no such entry in the note')
            continue
        covered.add((section, entry))
        if flagged:
            report.fail(f'{note.name}: ledger row {label} is flagged but the '
                        'claim is written into the card; remove it or find '
                        'its source')
        elif not source:
            report.fail(f'{note.name}: ledger row {label} names no source '
                        '(write the source, or leave the claim unwritten and '
                        'flagged)')
        else:
            for item in source.split(';'):
                if not source_exists(root, item):
                    report.fail(f'{note.name}: ledger row {label} names '
                                f'{item.strip()}, which is not a file under '
                                'reference/')
    for key in note.expected_entries():
        if key not in covered:
            report.fail(f'{note.name}: {key[0]} {key[1]} has no ledger row')


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


def full_name(char):
    return ' '.join(p for p in (char.get('name', ''), char.get('lastName', ''))
                    if p).strip()


NOT_OWNERS = {'anyone', 'anybody', 'someone', 'somebody', 'nobody',
              'noone', 'no', 'none', 'everyone'}
WORD = r"[^\W\d_][\w'’-]*"


def named_owners(text, name, known):
    """Names the description writes as an owner of the character `name`.

    A capitalised word (first character upper case, in any script) is a
    name, together with the capitalised words after it. After "owned by"
    and the like, a word in lower case counts only when it is one of the
    casefolded cast or connection names in `known`.
    """
    found = []
    phrase = (r"(?i:\bowned by|\bbelongs to|\bpet of|\bcompanion of)"
              rf"\s+({WORD}(?:\s+{WORD})*)")
    for m in re.finditer(phrase, text):
        words = m.group(1).split()
        first = words[0]
        if first.casefold() in NOT_OWNERS:
            continue
        if first[:1].isupper():
            run = []
            for w in words:
                if not w[:1].isupper():
                    break
                run.append(w)
            found.append(' '.join(run))
        elif any(k == first.casefold() or k.startswith(first.casefold() + ' ')
                 for k in known):
            found.append(first)
    possessive = (rf"({WORD})['’]s (?:\w+ ){{0,2}}"
                  rf"(?i:{PET_NOUNS}|{re.escape(name)})\b")
    for m in re.finditer(possessive, text):
        if not m.group(1)[:1].isupper():
            continue
        run = [m.group(1)]
        for w in reversed(text[:m.start(1)].split()):
            if not (re.fullmatch(WORD, w) and w[:1].isupper()):
                break
            run.insert(0, w)
        found.append(' '.join(run))
    return found


def check_export(root, world_json):
    report = Report()
    notes, sheet = load_world(root)
    if sheet is None:
        report.fail(f'reference/{SHEET_NAME} does not exist')
        return report
    with open(world_json, encoding='utf-8') as f:
        data = json.load(f)
    for char in data.get('characters', []):
        name = full_name(char)
        note = notes.get(name.casefold())
        if note is None:
            report.fail(f'{name}: exported character has no character note')
            continue
        if normalize(char.get('appearance') or '') != note.preamble:
            report.fail(f'{name}: appearance differs from the note\'s '
                        'Body preamble')
        if name.casefold() not in {c.casefold() for c in sheet.cast}:
            report.fail(f'{name}: exported character has a card but no '
                        'subsection under Characters in the reference sheet')
            continue
        role = char.get('role', '')
        for occ in sheet.occupations.get(name.casefold(), []):
            if not re.search(rf'(?<!\w){re.escape(occ)}(?!\w)', role,
                             re.IGNORECASE):
                report.fail(f'{name}: role lacks the occupation "{occ}" '
                            'that the reference sheet lists')
        owners = sheet.owners_of(name)
        allowed = {o.casefold() for o in owners}
        known = ({c.casefold() for c in sheet.cast}
                 | {r.get(k, '').casefold() for r in sheet.connections
                    for k in ('From', 'To')})
        for sset in char.get('spriteSets', []):
            for owner in named_owners(sset.get('description', ''), name,
                                      known):
                if not any(owner.casefold() == a
                           or a.startswith(owner.casefold() + ' ')
                           for a in allowed):
                    listed = ', '.join(sorted(owners)) or 'no owner'
                    report.fail(f'{name}: sprite set "{sset.get("name", "")}" '
                                f'description names {owner} as owner; the '
                                f'Connections table lists {listed}')
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
