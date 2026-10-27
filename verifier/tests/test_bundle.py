# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Bundles, Vital Signs and Spores through the command line, on directories written to disk."""

import json
from pathlib import Path

from ilorium_verifier.__main__ import main

VECTORS = Path(__file__).resolve().parents[2] / "vectors"


def _case(file: str, case_id: str) -> dict:
    cases = json.loads((VECTORS / file).read_text(encoding="utf-8"))["cases"]
    return next(c for c in cases if c["id"] == case_id)


def _write_bundle(root: Path, files: dict[str, str]) -> Path:
    root.mkdir()
    for name, text in files.items():
        (root / name).write_bytes(text.encode("utf-8"))
    return root


def _trust(tmp_path: Path, trust: dict) -> Path:
    path = tmp_path / "trust.json"
    path.write_text(json.dumps(trust), encoding="utf-8")
    return path


def test_bundle_command_exit_codes(tmp_path, capsys):
    for case_id, code, verdict in [("healthy", 0, "PASS"), ("record-altered-after-manifest", 1, "FAIL"),
                                   ("listed-file-missing", 2, "UNKNOWN")]:
        case = _case("bundle.json", case_id)
        directory = _write_bundle(tmp_path / case_id, case["input"]["files"])
        argv = ["bundle", str(directory), "--trust", str(_trust(tmp_path, case["input"]["trust"])),
                "--now", case["input"]["now"], "--json"]
        assert main(argv) == code
        report = json.loads(capsys.readouterr().out)
        assert report["verdict"] == verdict
        assert report["limitations"] and report["bundle"]["manifest_sha256"].startswith("sha256:")


def test_a_subdirectory_in_a_bundle_is_unlisted(tmp_path, capsys):
    case = _case("bundle.json", "healthy")
    directory = _write_bundle(tmp_path / "b", case["input"]["files"])
    (directory / "extra").mkdir()
    argv = ["bundle", str(directory), "--trust", str(_trust(tmp_path, case["input"]["trust"])), "--json"]
    assert main(argv) == 1
    checks = {c["id"]: c["verdict"] for c in json.loads(capsys.readouterr().out)["checks"]}
    assert checks["bundle.files"] == "FAIL"


def test_bundle_without_trust_is_a_usage_error(tmp_path):
    case = _case("bundle.json", "healthy")
    directory = _write_bundle(tmp_path / "b", case["input"]["files"])
    bad = tmp_path / "bad.json"
    bad.write_text("{}")
    assert main(["bundle", str(directory), "--trust", str(bad)]) == 64


def test_vitalsigns_command(tmp_path, capsys):
    case = _case("vitalsigns.json", "healthy")
    directory = _write_bundle(tmp_path / "b", case["input"]["bundle"])
    vital = tmp_path / "vital.json"
    vital.write_text(case["input"]["vitalsigns_json"], encoding="utf-8")
    assert main(["vitalsigns", str(vital), "--bundle", str(directory)]) == 0
    assert capsys.readouterr().out.startswith("PASS")
    # Without the bundle the answer is UNKNOWN, never PASS.
    assert main(["vitalsigns", str(vital)]) == 2
    assert main(["vitalsigns", str(tmp_path / "missing.json")]) == 64


def test_spore_command(tmp_path, capsys):
    good = tmp_path / "spore.json"
    good.write_text(_case("spore.json", "minimal")["input"]["spore_json"], encoding="utf-8")
    assert main(["spore", str(good), "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["verdict"] == "PASS"
    good.write_text(_case("spore.json", "duplicate-holder-id")["input"]["spore_json"], encoding="utf-8")
    assert main(["spore", str(good)]) == 1
    assert main(["spore", str(tmp_path / "nope.json")]) == 64
