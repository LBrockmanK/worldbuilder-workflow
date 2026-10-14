"""Tests for sbworld_tool.py: the standard .sbworld rebuild tool.

Run: python -m pytest tests/test_sbworld_tool.py
"""
import json
import os
import sys
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import sbworld_tool as tool  # noqa: E402

# The real-archive round trip runs only when SBWORLD_ARCHIVE names an existing
# .sbworld; the plugin ships no archive.
_real = os.environ.get("SBWORLD_ARCHIVE")
REAL_ARCHIVE = Path(_real) if _real else None

A1, A2, A3 = "11111111-1111-1111-1111-111111111111", "22222222-2222-2222-2222-222222222222", "33333333-3333-3333-3333-333333333333"


def make_fixture(root: Path, ids=(A1, A2), referenced=(A1, A2, A3), missing=1, counts_assets=None):
    """A tiny extracted-archive layout (world.json, manifest.json, assets/)."""
    root.mkdir()
    assets = root / "assets"
    assets.mkdir()
    for i in ids:
        (assets / f"{i}.png").write_bytes(b"png-" + i.encode())
    world = {"characters": [{"x": f"asset://sandboxWorldAssets/{r}"} for r in referenced], "moods": ["a"]}
    manifest = {
        "format": "sandbox-world", "worldName": "T", "exportedAt": "2026-09-14T13:56:34.422Z",
        "counts": {"characters": len(referenced), "moods": 1, "bundledAudio": 0,
                   "bundledAssets": len(ids) if counts_assets is None else counts_assets},
        "bundledMusic": [],
        "bundledAssets": [{"id": i, "path": f"assets/{i}.png", "mime": "image/png", "kind": "character_sprite"} for i in ids],
        "missingAssets": missing,
    }
    (root / "world.json").write_text(json.dumps(world, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")
    return root


def build_args(root: Path, out: Path, *extra):
    return ["build", "--world", str(root / "world.json"), "--manifest", str(root / "manifest.json"),
            "--assets", str(root / "assets"), "--out", str(out), *extra]


def crc_map(path: Path):
    with zipfile.ZipFile(path) as z:
        return sorted((i.filename, i.CRC, i.file_size) for i in z.infolist())


def test_synthetic_round_trip(tmp_path):
    fx = make_fixture(tmp_path / "fx")
    out = tmp_path / "a.sbworld"
    assert tool.main(build_args(fx, out)) == 0
    ex = tmp_path / "ex"
    assert tool.main(["extract", str(out), "--into", str(ex)]) == 0
    assert (ex / "world.json").read_bytes() == (fx / "world.json").read_bytes()
    assert (ex / "manifest.json").read_bytes() == (fx / "manifest.json").read_bytes()
    out2 = tmp_path / "b.sbworld"
    assert tool.main(build_args(ex, out2)) == 0
    assert crc_map(out) == crc_map(out2)
    with zipfile.ZipFile(out2) as z:
        assert [i.filename for i in z.infolist()][:3] == ["manifest.json", "world.json", "assets/"]
        assert {i.compress_type for i in z.infolist()} == {zipfile.ZIP_STORED}


def test_build_normalizes_crlf(tmp_path):
    fx = make_fixture(tmp_path / "fx")
    for f in ("world.json", "manifest.json"):
        p = fx / f
        p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
    out = tmp_path / "a.sbworld"
    assert tool.main(build_args(fx, out)) == 0
    with zipfile.ZipFile(out) as z:
        assert b"\r" not in z.read("world.json") and b"\r" not in z.read("manifest.json")


def test_build_refuses_existing_output(tmp_path):
    fx = make_fixture(tmp_path / "fx")
    out = tmp_path / "a.sbworld"
    out.write_bytes(b"keep")
    assert tool.main(build_args(fx, out)) == 1
    assert out.read_bytes() == b"keep"


def test_extract_refuses_existing_target(tmp_path):
    fx = make_fixture(tmp_path / "fx")
    out = tmp_path / "a.sbworld"
    tool.main(build_args(fx, out))
    target = tmp_path / "there"
    target.mkdir()
    assert tool.main(["extract", str(out), "--into", str(target)]) == 1
    assert list(target.iterdir()) == []


def test_build_fails_when_manifest_lists_missing_file(tmp_path):
    fx = make_fixture(tmp_path / "fx")
    (fx / "assets" / f"{A2}.png").unlink()
    assert tool.main(build_args(fx, tmp_path / "a.sbworld")) == 1
    assert not (tmp_path / "a.sbworld").exists()


def test_build_fails_on_file_without_entry(tmp_path):
    fx = make_fixture(tmp_path / "fx")
    (fx / "assets" / f"{A3}.png").write_bytes(b"x")
    assert tool.main(build_args(fx, tmp_path / "a.sbworld")) == 1


def test_build_fails_when_counts_disagree(tmp_path):
    fx = make_fixture(tmp_path / "fx", counts_assets=5)
    assert tool.main(build_args(fx, tmp_path / "a.sbworld")) == 1
    out = tmp_path / "b.sbworld"
    assert tool.main(build_args(fx, out, "--update-counts")) == 0
    with zipfile.ZipFile(out) as z:
        m = json.loads(z.read("manifest.json"))
    assert m["counts"]["bundledAssets"] == 2 and m["exportedAt"] == "2026-09-14T13:56:34.422Z"


def test_build_fails_when_missing_assets_disagree(tmp_path):
    fx = make_fixture(tmp_path / "fx", missing=0)
    assert tool.main(build_args(fx, tmp_path / "a.sbworld")) == 1
    out = tmp_path / "b.sbworld"
    assert tool.main(build_args(fx, out, "--accept-missing")) == 0
    with zipfile.ZipFile(out) as z:
        assert json.loads(z.read("manifest.json"))["missingAssets"] == 1


def prune_args(fx, *extra):
    return ["prune", "--world", str(fx / "world.json"), "--manifest", str(fx / "manifest.json"),
            "--assets", str(fx / "assets"), *extra]


def test_prune_dry_run_lists_and_writes_nothing(tmp_path, capsys):
    fx = make_fixture(tmp_path / "fx", referenced=(A1,), missing=0)
    before = sorted(p.name for p in fx.rglob("*"))
    original = (fx / "manifest.json").read_bytes()
    assert tool.main(prune_args(fx)) == 0
    assert A2 in capsys.readouterr().out
    assert sorted(p.name for p in fx.rglob("*")) == before
    assert (fx / "manifest.json").read_bytes() == original


def test_prune_apply_quarantines_files_and_writes_manifest_copy(tmp_path):
    fx = make_fixture(tmp_path / "fx", referenced=(A1,), missing=0)
    original = (fx / "manifest.json").read_bytes()
    assert tool.main(prune_args(fx, "--apply")) == 0
    assert (fx / "manifest.json").read_bytes() == original
    assert not (fx / "assets" / f"{A2}.png").exists() and (fx / "assets" / f"{A1}.png").exists()
    quarantine = list(fx.glob("assets-pruned-*"))
    assert len(quarantine) == 1 and (quarantine[0] / f"{A2}.png").read_bytes() == b"png-" + A2.encode()
    copies = list(fx.glob("manifest-pruned-*.json"))
    assert len(copies) == 1
    m = json.loads(copies[0].read_text(encoding="utf-8"))
    assert [a["id"] for a in m["bundledAssets"]] == [A1] and m["counts"]["bundledAssets"] == 1


def test_prune_apply_in_place_rewrites_the_manifest(tmp_path):
    fx = make_fixture(tmp_path / "fx", referenced=(A1,), missing=0)
    assert tool.main(prune_args(fx, "--apply", "--in-place")) == 0
    m = json.loads((fx / "manifest.json").read_text(encoding="utf-8"))
    assert [a["id"] for a in m["bundledAssets"]] == [A1]
    assert not list(fx.glob("manifest-pruned-*.json"))


def test_prune_apply_failure_midway_restores_files_and_manifest(tmp_path, monkeypatch):
    fx = make_fixture(tmp_path / "fx", ids=(A1, A2, A3), referenced=(), missing=0)
    original = (fx / "manifest.json").read_bytes()
    real_move = tool.shutil.move
    calls = {"n": 0}

    def flaky(src, dst):
        calls["n"] += 1
        if calls["n"] == 2:
            raise OSError("disk says no")
        return real_move(src, dst)

    monkeypatch.setattr(tool.shutil, "move", flaky)
    assert tool.main(prune_args(fx, "--apply", "--in-place")) == 1
    monkeypatch.undo()
    assert (fx / "manifest.json").read_bytes() == original
    for i in (A1, A2, A3):
        assert (fx / "assets" / f"{i}.png").read_bytes() == b"png-" + i.encode()
    assert not list(fx.glob("manifest-pruned-*.json"))


def test_prune_apply_refuses_when_manifest_target_exists(tmp_path, monkeypatch):
    fx = make_fixture(tmp_path / "fx", referenced=(A1,), missing=0)
    monkeypatch.setattr(tool, "stamp", lambda: "fixed")
    (fx / "manifest-pruned-fixed.json").write_text("keep", encoding="utf-8")
    assert tool.main(prune_args(fx, "--apply")) == 1
    assert (fx / "assets" / f"{A2}.png").exists()
    assert (fx / "manifest-pruned-fixed.json").read_text(encoding="utf-8") == "keep"


def test_prune_apply_loses_a_quarantine_race_without_touching_anything(tmp_path, monkeypatch):
    fx = make_fixture(tmp_path / "fx", referenced=(A1,), missing=0)
    monkeypatch.setattr(tool, "stamp", lambda: "fixed")
    quarantine = fx / "assets-pruned-fixed"
    quarantine.mkdir()
    (quarantine / "theirs.txt").write_text("keep", encoding="utf-8")
    original = (fx / "manifest.json").read_bytes()
    real_exists = Path.exists
    monkeypatch.setattr(Path, "exists", lambda self: False if self == quarantine else real_exists(self))
    assert tool.main(prune_args(fx, "--apply", "--in-place")) == 1
    monkeypatch.undo()
    assert (fx / "manifest.json").read_bytes() == original
    assert (fx / "assets" / f"{A2}.png").exists() and (fx / "assets" / f"{A1}.png").exists()
    assert [p.name for p in quarantine.iterdir()] == ["theirs.txt"]
    assert not list(fx.glob("manifest-pruned-*.json"))


class _FailingWrite:
    """File wrapper whose write fails after the real exclusive open succeeded."""

    def __init__(self, fh):
        self._fh = fh

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self._fh.close()
        return False

    def write(self, data):
        self._fh.write(b"partial")
        raise OSError("disk full")

    def close(self):
        self._fh.close()


def _fail_manifest_writes(monkeypatch):
    real_open = open

    def fake_open(path, mode="r", *a, **k):
        fh = real_open(path, mode, *a, **k)
        if "x" in mode and "manifest" in Path(path).name and not str(path).endswith("prune-lock"):
            return _FailingWrite(fh)
        return fh

    monkeypatch.setattr(tool, "open", fake_open, raising=False)


def test_prune_apply_in_place_write_failure_leaves_original_manifest_and_no_temp(tmp_path, monkeypatch):
    fx = make_fixture(tmp_path / "fx", referenced=(A1,), missing=0)
    original = (fx / "manifest.json").read_bytes()
    _fail_manifest_writes(monkeypatch)
    assert tool.main(prune_args(fx, "--apply", "--in-place")) == 1
    monkeypatch.undo()
    assert (fx / "manifest.json").read_bytes() == original
    assert sorted(p.name for p in fx.iterdir()) == ["assets", "manifest.json", "world.json"]
    assert (fx / "assets" / f"{A2}.png").exists()


def test_prune_apply_new_target_write_failure_leaves_no_partial_manifest(tmp_path, monkeypatch):
    fx = make_fixture(tmp_path / "fx", referenced=(A1,), missing=0)
    _fail_manifest_writes(monkeypatch)
    assert tool.main(prune_args(fx, "--apply")) == 1
    monkeypatch.undo()
    assert sorted(p.name for p in fx.iterdir()) == ["assets", "manifest.json", "world.json"]
    assert (fx / "assets" / f"{A2}.png").exists()


def test_prune_apply_refuses_when_lock_file_exists(tmp_path):
    fx = make_fixture(tmp_path / "fx", referenced=(A1,), missing=0)
    lock = fx / "manifest.json.prune-lock"
    lock.write_text("other run", encoding="utf-8")
    original = (fx / "manifest.json").read_bytes()
    assert tool.main(prune_args(fx, "--apply", "--in-place")) == 1
    assert lock.read_text(encoding="utf-8") == "other run"
    assert (fx / "manifest.json").read_bytes() == original
    assert (fx / "assets" / f"{A2}.png").exists() and not list(fx.glob("assets-pruned-*"))


def test_prune_apply_removes_its_lock_when_done(tmp_path):
    fx = make_fixture(tmp_path / "fx", referenced=(A1,), missing=0)
    assert tool.main(prune_args(fx, "--apply")) == 0
    assert not (fx / "manifest.json.prune-lock").exists()


def test_failed_build_never_deletes_a_file_it_did_not_create(tmp_path, monkeypatch):
    fx = make_fixture(tmp_path / "fx")
    out = tmp_path / "a.sbworld"
    out.write_bytes(b"someone else's archive")
    real_exists = Path.exists
    monkeypatch.setattr(Path, "exists", lambda self: False if self == out else real_exists(self))
    assert tool.main(build_args(fx, out)) == 1
    monkeypatch.undo()
    assert out.read_bytes() == b"someone else's archive"


@pytest.mark.skipif(REAL_ARCHIVE is None or not REAL_ARCHIVE.exists(),
                    reason="set SBWORLD_ARCHIVE to a real .sbworld to run this test")
def test_real_archive_round_trip(tmp_path):
    ex = tmp_path / "ex"
    assert tool.main(["extract", str(REAL_ARCHIVE), "--into", str(ex)]) == 0
    out = tmp_path / "rebuilt.sbworld"
    assert tool.main(build_args(ex, out)) == 0
    with zipfile.ZipFile(REAL_ARCHIVE) as a, zipfile.ZipFile(out) as b:
        for name in ("world.json", "manifest.json"):
            assert a.read(name) == b.read(name)
        orig = sorted((i.filename, i.CRC, i.file_size) for i in a.infolist())
        new = sorted((i.filename, i.CRC, i.file_size) for i in b.infolist())
        assert orig == new


def test_update_counts_persists_the_corrected_manifest(tmp_path):
    fx = make_fixture(tmp_path / "fx", counts_assets=99)
    out = tmp_path / "a.sbworld"
    assert tool.main(build_args(fx, out, "--update-counts")) == 0
    with zipfile.ZipFile(out) as z:
        packed = z.read("manifest.json")
    assert (fx / "manifest.json").read_bytes() == packed
    assert json.loads(packed)["counts"]["bundledAssets"] == 2
    out2 = tmp_path / "b.sbworld"
    assert tool.main(build_args(fx, out2)) == 0  # no flag needed any more
    assert not [p for p in fx.iterdir() if ".tmp" in p.name]


def test_accept_missing_persists_the_corrected_manifest(tmp_path):
    fx = make_fixture(tmp_path / "fx", missing=5)
    assert tool.main(build_args(fx, tmp_path / "a.sbworld", "--accept-missing")) == 0
    assert json.loads((fx / "manifest.json").read_text(encoding="utf-8"))["missingAssets"] == 1


def test_default_output_name_is_sanitized_and_stays_beside_the_manifest(tmp_path):
    fx = make_fixture(tmp_path / "fx")
    m = json.loads((fx / "manifest.json").read_text(encoding="utf-8"))
    BS = chr(92)
    m["worldName"] = ".." + BS + ".." + BS + "evil/Who: me?"
    (fx / "manifest.json").write_text(json.dumps(m, indent=2), encoding="utf-8", newline="\n")
    assert tool.main(["build", "--world", str(fx / "world.json"), "--manifest", str(fx / "manifest.json"),
                      "--assets", str(fx / "assets")]) == 0
    built = [p for p in fx.glob("*.sbworld")]
    assert len(built) == 1
    assert not any(c in built[0].name for c in '/:*?"<>|' + BS)
    assert not list(tmp_path.glob("*.sbworld"))


def test_absolute_world_name_cannot_redirect_the_output(tmp_path):
    fx = make_fixture(tmp_path / "fx")
    m = json.loads((fx / "manifest.json").read_text(encoding="utf-8"))
    m["worldName"] = str(tmp_path / "elsewhere")
    (fx / "manifest.json").write_text(json.dumps(m, indent=2), encoding="utf-8", newline="\n")
    assert tool.main(["build", "--world", str(fx / "world.json"), "--manifest", str(fx / "manifest.json"),
                      "--assets", str(fx / "assets")]) == 0
    assert len(list(fx.glob("*.sbworld"))) == 1


def test_write_atomic_leaves_a_colliding_temp_name_alone(tmp_path):
    target = tmp_path / "manifest.json"
    target.write_bytes(b"old")
    other = tmp_path / "manifest.json.tmp"
    other.write_bytes(b"another run")
    tool.write_atomic(target, b"new")
    assert target.read_bytes() == b"new"
    assert other.read_bytes() == b"another run"
    assert sorted(p.name for p in tmp_path.iterdir()) == ["manifest.json", "manifest.json.tmp"]
