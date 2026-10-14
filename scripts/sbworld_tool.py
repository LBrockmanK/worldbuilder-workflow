#!/usr/bin/env python3
"""Rebuild tool for ainime .sbworld export archives.

An .sbworld is a stored (uncompressed) zip: manifest.json, world.json, an
assets/ directory entry, then assets/<id>.<ext> files. A project keeps
world.json and manifest.json versioned beside an assets/ folder and builds
the archive from the three; the archive is never edited in place.

Usage:
    python sbworld_tool.py extract <archive> [--into DIR]
    python sbworld_tool.py build --world W --manifest M --assets A [--out FILE]
                                 [--accept-missing] [--update-counts]
                                 [--refresh-exported-at]
    python sbworld_tool.py prune --world W --manifest M --assets A
                                 [--apply [--in-place]]

Output is non-destructive: nothing existing is overwritten. Targets that
exist are refused; default names are timestamped. Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ASSET_URI = re.compile(r"asset://sandboxWorldAssets/([0-9A-Za-z-]+)")
ASSET_PATH = re.compile(r"^assets/([0-9A-Za-z-]+)\.([A-Za-z0-9]+)$")


class ToolError(Exception):
    """A refusal or validation failure; message is shown to the user."""


def stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def normalize_eol(raw: bytes) -> bytes:
    """CRLF -> LF. Safe for JSON (raw newlines cannot occur inside strings).

    A git checkout with autocrlf turns the versioned files into CRLF while
    the archive carries LF; the archive form is LF.
    """
    return raw.replace(b"\r\n", b"\n")


# ---------------------------------------------------------------- extract

def cmd_extract(archive: Path, into: Path | None) -> Path:
    if not archive.is_file():
        raise ToolError(f"archive not found: {archive}")
    if into is None:
        into = archive.parent / f"extract-{archive.stem}-{stamp()}"
    if into.exists():
        raise ToolError(f"refusing to extract: target exists: {into}")
    with zipfile.ZipFile(archive) as zf:
        members = zf.infolist()
        for info in members:
            name = info.filename
            if name in ("manifest.json", "world.json", "assets/"):
                continue
            if not ASSET_PATH.match(name):
                raise ToolError(f"unexpected archive member: {name!r}")
        into.mkdir(parents=True)
        (into / "assets").mkdir()
        for info in members:
            name = info.filename
            if name == "assets/":
                continue
            (into / name).write_bytes(zf.read(info))
    print(f"extracted {len(members)} members to {into}")
    return into


# ---------------------------------------------------------------- shared

def load_json(path: Path) -> tuple[dict, bytes]:
    if not path.is_file():
        raise ToolError(f"file not found: {path}")
    raw = normalize_eol(path.read_bytes())
    return json.loads(raw.decode("utf-8")), raw


def referenced_ids(world_raw: bytes) -> set[str]:
    return set(ASSET_URI.findall(world_raw.decode("utf-8")))


def serialize_manifest(manifest: dict, had_trailing_newline: bool) -> bytes:
    text = json.dumps(manifest, indent=2, ensure_ascii=False)
    if had_trailing_newline:
        text += "\n"
    return text.encode("utf-8")


def derived_counts(manifest: dict, world: dict) -> dict:
    """Counts that can be derived from the data; the rest stay as recorded."""
    counts = dict(manifest.get("counts", {}))
    counts["bundledAssets"] = len(manifest.get("bundledAssets", []))
    if "characters" in counts:
        counts["characters"] = len(world.get("characters", []))
    if "moods" in counts:
        counts["moods"] = len(world.get("moods", []))
    # bundledAudio is not derivable from world.json or the asset folder
    # (it counts audio files, of which the archive has no members); kept.
    return counts


def missing_assets(manifest: dict, world_raw: bytes) -> int:
    bundled = {a["id"] for a in manifest.get("bundledAssets", [])}
    return len(referenced_ids(world_raw) - bundled)


def check_asset_files(manifest: dict, assets: Path) -> None:
    if not assets.is_dir():
        raise ToolError(f"assets folder not found: {assets}")
    entries = manifest.get("bundledAssets", [])
    ids = [a["id"] for a in entries]
    if len(ids) != len(set(ids)):
        raise ToolError("manifest bundledAssets has duplicate ids")
    on_disk = {p.name for p in assets.iterdir()}
    expected = {}
    for a in entries:
        m = ASSET_PATH.match(a["path"])
        if not m or m.group(1) != a["id"]:
            raise ToolError(f"bundledAssets entry has unexpected path: {a}")
        expected[a["path"][len("assets/"):]] = a
    missing = sorted(set(expected) - on_disk)
    extra = sorted(on_disk - set(expected))
    problems = []
    if missing:
        problems.append(f"{len(missing)} manifest entries have no file (first: {missing[0]})")
    if extra:
        problems.append(f"{len(extra)} files have no manifest entry (first: {extra[0]})")
    if problems:
        raise ToolError("; ".join(problems))


# ---------------------------------------------------------------- build

def zip_date(manifest: dict) -> tuple:
    try:
        d = dt.datetime.strptime(manifest["exportedAt"][:19], "%Y-%m-%dT%H:%M:%S")
        return d.timetuple()[:6]
    except (KeyError, ValueError):
        return dt.datetime.now().timetuple()[:6]


def safe_basename(name: object) -> str:
    """A worldName reduced to a safe file name stem: no separators, no
    Windows-invalid characters, never absolute, never empty."""
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", str(name))
    text = text.strip(" .") or "world"
    return text.replace("..", "_")[:80]


def write_atomic(path: Path, data: bytes) -> None:
    """Write beside the target, then replace: an interrupted write never
    leaves a partial file in place of the original."""
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    tmp = Path(tmp_name)  # created exclusively by this call; the only file it may remove
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def cmd_build(world_path: Path, manifest_path: Path, assets: Path, out: Path | None,
              accept_missing: bool, update_counts: bool, refresh_exported_at: bool) -> Path:
    world, world_raw = load_json(world_path)
    manifest, manifest_raw = load_json(manifest_path)
    if out is None:
        out = manifest_path.parent / f"{safe_basename(manifest.get('worldName', 'world'))}-{stamp()}.sbworld"
        if out.resolve().parent != manifest_path.resolve().parent:
            raise ToolError(f"refusing to build: default output leaves the manifest folder: {out}")
    if out.exists():
        raise ToolError(f"refusing to build: output exists: {out}")

    check_asset_files(manifest, assets)

    new_manifest = json.loads(json.dumps(manifest))
    counts = derived_counts(manifest, world)
    if counts != manifest.get("counts"):
        if not update_counts:
            diff = {k: (manifest.get("counts", {}).get(k), v)
                    for k, v in counts.items() if manifest.get("counts", {}).get(k) != v}
            raise ToolError(f"manifest.counts disagrees with the data (recorded, computed): {diff}; "
                            "pass --update-counts to record the computed values")
        new_manifest["counts"] = counts
    missing = missing_assets(manifest, world_raw)
    if missing != manifest.get("missingAssets"):
        if not accept_missing:
            raise ToolError(f"manifest.missingAssets is {manifest.get('missingAssets')} but "
                            f"{missing} referenced asset ids have no bundledAssets entry; "
                            "pass --accept-missing to record the computed value")
        new_manifest["missingAssets"] = missing
    if refresh_exported_at:
        now = dt.datetime.now(dt.timezone.utc)
        new_manifest["exportedAt"] = now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"

    if new_manifest != manifest:
        manifest_bytes = serialize_manifest(new_manifest, manifest_raw.endswith(b"\n"))
    else:
        manifest_bytes = manifest_raw  # unchanged: copy the bytes as given

    if new_manifest != manifest:
        # the versioned manifest must match what is packed, or the next build fails again
        write_atomic(manifest_path, manifest_bytes)

    date = zip_date(new_manifest)

    def info(name: str) -> zipfile.ZipInfo:
        zi = zipfile.ZipInfo(name, date_time=date)
        zi.compress_type = zipfile.ZIP_STORED
        zi.create_system = 0
        return zi

    owned = False
    try:
        try:
            fh = open(out, "xb")  # exclusive: fails if the output appeared since the check above
        except FileExistsError:
            raise ToolError(f"refusing to build: output exists: {out}")
        owned = True
        with fh, zipfile.ZipFile(fh, "w", compression=zipfile.ZIP_STORED) as zf:
            zf.writestr(info("manifest.json"), manifest_bytes)
            zf.writestr(info("world.json"), world_raw)
            d = info("assets/")
            d.external_attr = 16
            zf.writestr(d, b"")
            for name in sorted(p.name for p in assets.iterdir()):
                zf.writestr(info(f"assets/{name}"), (assets / name).read_bytes())
    except BaseException:
        if owned:  # only remove what this invocation created
            out.unlink(missing_ok=True)
        raise
    n = len(new_manifest.get("bundledAssets", []))
    print(f"built {out} ({n} assets, missingAssets={new_manifest.get('missingAssets')})")
    return out


# ---------------------------------------------------------------- prune

def cmd_prune(world_path: Path, manifest_path: Path, assets: Path, in_place: bool, apply: bool = False) -> Path | None:
    """Dry run by default. With apply: write the new manifest, then move each
    dropped file into assets-pruned-<stamp>/ (never unlink); undo on failure."""
    world, world_raw = load_json(world_path)
    manifest, manifest_raw = load_json(manifest_path)
    check_asset_files(manifest, assets)
    refs = referenced_ids(world_raw)
    keep, drop = [], []
    for a in manifest["bundledAssets"]:
        (keep if a["id"] in refs else drop).append(a)
    for a in drop:
        print(f"{'removing' if apply else 'would remove'} {a['id']} ({a['kind']})")
    if not apply:
        print(f"dry run: {len(drop)} assets would be removed; nothing written (pass --apply)")
        return None
    lock = manifest_path.with_name(manifest_path.name + ".prune-lock")
    lock_owned = False
    try:
        try:
            with open(lock, "xb"):  # exclusive: one prune --apply at a time per manifest
                pass
        except FileExistsError:
            raise ToolError(f"refusing to prune: lock file exists (another run, or a stale lock "
                            f"to remove by hand): {lock}")
        lock_owned = True
        return _apply_prune(world, world_raw, manifest, manifest_raw, manifest_path, assets,
                            in_place, keep, drop)
    finally:
        if lock_owned:
            lock.unlink(missing_ok=True)


def _apply_prune(world, world_raw, manifest, manifest_raw, manifest_path, assets, in_place, keep, drop) -> Path:
    new_manifest = json.loads(json.dumps(manifest))
    new_manifest["bundledAssets"] = keep
    new_manifest["counts"] = derived_counts(new_manifest, world)
    new_manifest["missingAssets"] = missing_assets(new_manifest, world_raw)
    stamp_ = stamp()
    target = manifest_path if in_place else manifest_path.with_name(f"manifest-pruned-{stamp_}.json")
    quarantine = assets.parent / f"assets-pruned-{stamp_}"
    # refusals first
    if not in_place and target.exists():
        raise ToolError(f"refusing to write: target exists: {target}")
    if quarantine.exists():
        raise ToolError(f"refusing to quarantine: folder exists: {quarantine}")
    if new_manifest == manifest:
        manifest_bytes = manifest_raw
    else:
        manifest_bytes = serialize_manifest(new_manifest, manifest_raw.endswith(b"\n"))
    original_bytes = manifest_path.read_bytes() if in_place else None
    moved: list[tuple[Path, Path]] = []
    owns_quarantine = False
    target_owned = False      # new target created by this run
    replaced = False          # in-place manifest replaced by this run
    temp: Path | None = None  # in-place temporary file created by this run
    try:
        try:
            quarantine.mkdir()  # atomic: success is the ownership claim
        except FileExistsError:
            raise ToolError(f"refusing to quarantine: folder exists: {quarantine}")
        owns_quarantine = True
        if in_place:
            temp = target.with_name(target.name + f".tmp-{stamp_}")
            with open(temp, "xb") as fh:  # exclusive; the original is never opened for writing
                fh.write(manifest_bytes)
            os.replace(temp, target)  # atomic landing
            temp = None
            replaced = True
        else:
            try:
                fh = open(target, "xb")  # exclusive: never clobber another run's file
            except FileExistsError:
                raise ToolError(f"refusing to write: target exists: {target}")
            target_owned = True  # ours from the moment the open succeeded
            with fh:
                fh.write(manifest_bytes)
        for a in drop:
            src = assets / a["path"][len("assets/"):]
            dst = quarantine / src.name
            shutil.move(str(src), str(dst))
            moved.append((src, dst))
    except BaseException as exc:
        notes = []
        try:
            for src, dst in reversed(moved):
                shutil.move(str(dst), str(src))
            notes.append(f"{len(moved)} moved file(s) put back")
            if temp is not None:
                temp.unlink(missing_ok=True)
                notes.append("temporary manifest removed")
            if replaced:
                restore = target.with_name(target.name + f".restore-{stamp_}")
                with open(restore, "xb") as fh:
                    fh.write(original_bytes)
                os.replace(restore, target)
                notes.append("original manifest restored")
            elif in_place:
                notes.append("original manifest was never modified")
            if target_owned:
                target.unlink(missing_ok=True)
                notes.append("new manifest removed")
            if owns_quarantine and not any(quarantine.iterdir()):
                quarantine.rmdir()
                notes.append("empty quarantine folder removed")
        except OSError as rollback_exc:
            raise ToolError(f"prune failed ({exc}) and ROLLBACK ALSO FAILED ({rollback_exc}); "
                            f"done before that: {', '.join(notes) or 'nothing'}; check {quarantine} and {target}")
        if isinstance(exc, OSError):
            raise ToolError(f"prune failed ({exc}); rolled back: {', '.join(notes)}")
        raise
    print(f"pruned {len(drop)} assets (moved to {quarantine}); manifest written to {target}")
    return target


# ---------------------------------------------------------------- cli

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("extract", help="unpack an archive into a new directory")
    e.add_argument("archive", type=Path)
    e.add_argument("--into", type=Path)

    def common(sp):
        sp.add_argument("--world", type=Path, required=True)
        sp.add_argument("--manifest", type=Path, required=True)
        sp.add_argument("--assets", type=Path, required=True)

    b = sub.add_parser("build", help="write a stored archive from world, manifest and assets")
    common(b)
    b.add_argument("--out", type=Path)
    b.add_argument("--accept-missing", action="store_true",
                   help="record the computed missingAssets instead of failing on a mismatch")
    b.add_argument("--update-counts", action="store_true",
                   help="record the computed counts instead of failing on a mismatch")
    b.add_argument("--refresh-exported-at", action="store_true",
                   help="set manifest exportedAt to now (default: preserved)")

    r = sub.add_parser("prune", help="remove assets no world.json field references")
    common(r)
    r.add_argument("--apply", action="store_true",
                   help="really prune: move files to assets-pruned-<stamp>/ and write the manifest (default: dry run)")
    r.add_argument("--in-place", action="store_true",
                   help="with --apply, overwrite the manifest (default: timestamped copy beside it)")

    a = p.parse_args(argv)
    try:
        if a.cmd == "extract":
            cmd_extract(a.archive, a.into)
        elif a.cmd == "build":
            cmd_build(a.world, a.manifest, a.assets, a.out,
                      a.accept_missing, a.update_counts, a.refresh_exported_at)
        else:
            cmd_prune(a.world, a.manifest, a.assets, a.in_place, a.apply)
    except ToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
