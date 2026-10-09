#!/usr/bin/env python3
"""Diff-based update for ainime .sbworld exports.

Reads the project's source documents (foundation.md, direction.md), generates
candidate field values, and diffs them against the world.json inside the
existing .sbworld archive.  The .sbworld is the only true export output;
no standalone world.json is required.

Changes are never applied silently -- the diff is shown first, and only
named fields are updated.

Usage:
    python export_diff.py <project-root>                     # show diff
    python export_diff.py <project-root> --apply field ...   # apply named fields
    python export_diff.py <project-root> --apply-all         # apply everything

<project-root> is the repo directory containing the worldvault project
(e.g. .../Fields of Mistria/repo).  The script locates project/foundation.md
and project/direction.md inside the first subdirectory that has a
project/ folder, and the .sbworld file inside exports/ainime/.
"""

import argparse
import difflib
import json
import os
import re
import sys
import textwrap
import zipfile
from datetime import datetime, timezone

# -- field map (source document -> world.json) -------------------------

FOUNDATION_TEXT_FIELDS = [
    ("Setting Summary", "settingSummary"),
    ("Genre and Tone", "genre"),
    ("Community", "communityDescription"),
    ("World Introduction", "introText"),
    ("Opening Situation", "initialStoryArc"),
    ("Era", "calendarConfig.eraReminder"),
]

FOUNDATION_LIST_FIELDS = [
    ("Inspirations", "inspirations"),
    ("Tonal Inspirations", "tonalInspirations"),
    ("Key Tropes and Themes", "keyTropesAndThemes"),
]

# -- helpers -----------------------------------------------------------

def find_sbworld(exports_dir):
    """Return the path to the first .sbworld file in exports_dir."""
    for f in os.listdir(exports_dir):
        if f.endswith(".sbworld"):
            return os.path.join(exports_dir, f)
    return None


def load_world_from_sbworld(sbworld_path):
    """Extract and parse world.json from inside the .sbworld archive."""
    with zipfile.ZipFile(sbworld_path, "r") as zf:
        return json.loads(zf.read("world.json"))


def extract_section(content, heading):
    """Text between a ## heading and the next ## heading or EOF."""
    pattern = rf"^## {re.escape(heading)}\n\n(.*?)(?=\n^## |\Z)"
    m = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    return m.group(1).strip() if m else None


def extract_list_items(content, heading):
    """Markdown list items under a ## heading, as a string array."""
    section = extract_section(content, heading)
    if section is None:
        return None
    return [line.strip()[2:] for line in section.split("\n")
            if line.strip().startswith("- ")]


def resolve_nested(obj, dotted_key):
    """Read a dotted key like 'calendarConfig.eraReminder' from a dict."""
    for part in dotted_key.split("."):
        if not isinstance(obj, dict):
            return None
        obj = obj.get(part)
    return obj


def set_nested(obj, dotted_key, value):
    """Write a dotted key into a nested dict."""
    parts = dotted_key.split(".")
    for part in parts[:-1]:
        obj = obj[part]
    obj[parts[-1]] = value


def field_diff(name, old, new):
    """Human-readable diff for one field.  Returns None if identical."""
    if old == new:
        return None

    if isinstance(old, list) and isinstance(new, list):
        removed = [x for x in old if x not in new]
        added = [x for x in new if x not in old]
        if not removed and not added:
            return None
        lines = []
        for r in removed:
            lines.append(f"  - {r}")
        for a in added:
            lines.append(f"  + {a}")
        return "\n".join(lines)

    if isinstance(old, str) and isinstance(new, str):
        diff = list(difflib.unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=f"{name} (.sbworld)",
            tofile=f"{name} (source doc)",
            lineterm="",
        ))
        return "\n".join(diff) if diff else None

    return f"  .sbworld: {repr(old)[:200]}\n  source:   {repr(new)[:200]}"


def repack_sbworld(sbworld_path, world):
    """Replace world.json inside the .sbworld archive, preserving assets."""
    with zipfile.ZipFile(sbworld_path, "r") as old_zip:
        manifest = json.loads(old_zip.read("manifest.json"))
        manifest["exportedAt"] = (
            datetime.now(timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        )
        other_entries = [
            n for n in old_zip.namelist()
            if n not in ("manifest.json", "world.json")
        ]

        tmp = sbworld_path + ".tmp"
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_STORED) as new_zip:
            new_zip.writestr(
                "manifest.json",
                json.dumps(manifest, indent=2, ensure_ascii=False),
            )
            new_zip.writestr(
                "world.json",
                json.dumps(world, indent=2, ensure_ascii=False) + "\n",
            )
            for name in other_entries:
                new_zip.writestr(name, old_zip.read(name))

    os.replace(tmp, sbworld_path)
    return os.path.getsize(sbworld_path)


# -- main --------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Diff source documents against the .sbworld export",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            examples:
              export_diff.py ./repo                                # show diff
              export_diff.py ./repo --apply communityDescription   # one field
              export_diff.py ./repo --apply-all                    # everything
        """),
    )
    parser.add_argument("project_root")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--apply", nargs="+", metavar="FIELD",
        help="apply only the named field(s)",
    )
    group.add_argument(
        "--apply-all", action="store_true",
        help="apply every differing field",
    )
    args = parser.parse_args()

    root = args.project_root

    # locate project subdirectory
    project_dir = None
    for d in os.listdir(root):
        if os.path.isdir(os.path.join(root, d, "project")):
            project_dir = os.path.join(root, d)
            break
    if not project_dir:
        sys.exit("No subdirectory with a project/ folder found.")

    foundation_path = os.path.join(project_dir, "project", "foundation.md")
    direction_path = os.path.join(project_dir, "project", "direction.md")
    exports_dir = os.path.join(root, "exports", "ainime")

    if not os.path.exists(foundation_path):
        sys.exit(f"foundation.md not found at {foundation_path}")

    sbworld_path = find_sbworld(exports_dir)
    if not sbworld_path:
        sys.exit(f"No .sbworld file found in {exports_dir}")

    # read sources
    with open(foundation_path, encoding="utf-8") as f:
        foundation = f.read()

    direction = None
    if os.path.exists(direction_path):
        with open(direction_path, encoding="utf-8") as f:
            direction = f.read().rstrip("\n")

    # build candidates from source documents
    candidates = {}
    for heading, field in FOUNDATION_TEXT_FIELDS:
        val = extract_section(foundation, heading)
        if val is not None:
            candidates[field] = val

    for heading, field in FOUNDATION_LIST_FIELDS:
        val = extract_list_items(foundation, heading)
        if val is not None:
            candidates[field] = val

    if direction:
        candidates["arcManagerGuidance"] = direction

    # load existing from .sbworld
    world = load_world_from_sbworld(sbworld_path)

    # diff
    diffs = {}
    for field, new_val in candidates.items():
        old_val = resolve_nested(world, field)
        diff_text = field_diff(field, old_val, new_val)
        if diff_text:
            diffs[field] = (old_val, new_val, diff_text)

    if not diffs:
        print("No differences between source documents and .sbworld.")
        return

    # display
    print(f"\n{'=' * 60}")
    print(f"  {len(diffs)} field(s) differ")
    print(f"{'=' * 60}")

    for field, (_, _, diff_text) in diffs.items():
        print(f"\n-- {field} --")
        print(diff_text)

    print(f"\n{'=' * 60}")
    print(f"  Differing fields: {', '.join(diffs.keys())}")
    print(f"{'=' * 60}\n")

    # apply?
    fields_to_apply = set()
    if args.apply_all:
        fields_to_apply = set(diffs.keys())
    elif args.apply:
        for f in args.apply:
            if f not in diffs:
                print(f"  Skipping {f} -- no difference found.")
            else:
                fields_to_apply.add(f)

    if not fields_to_apply:
        if not args.apply and not args.apply_all:
            print("  Run with --apply <field> ... or --apply-all to update.")
        return

    # apply to the in-memory world, then repack
    for field in fields_to_apply:
        _, new_val, _ = diffs[field]
        set_nested(world, field, new_val)
        print(f"  Updated: {field}")

    size = repack_sbworld(sbworld_path, world)
    print(f"  Repacked {os.path.basename(sbworld_path)} ({size:,} bytes)")
    print("Done.")


if __name__ == "__main__":
    main()
