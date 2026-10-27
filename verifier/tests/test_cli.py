# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""The command line, end to end, on exports written to disk."""

import json
from pathlib import Path

import pytest

from ilorium_verifier.__main__ import main

VECTORS = Path(__file__).resolve().parents[2] / "vectors"


def _case(file: str, case_id: str) -> dict:
    cases = json.loads((VECTORS / file).read_text(encoding="utf-8"))["cases"]
    return next(c for c in cases if c["id"] == case_id)


def _export(tmp_path: Path, case: dict) -> tuple[Path, Path]:
    inp = case["input"]
    export = tmp_path / "export"
    export.mkdir()
    (export / "records.jsonl").write_bytes(inp["records_jsonl"].encode())
    if "checkpoints_jsonl" in inp:
        (export / "checkpoints.jsonl").write_bytes(inp["checkpoints_jsonl"].encode())
    if "pulses_jsonl" in inp:
        (export / "pulses.jsonl").write_bytes(inp["pulses_jsonl"].encode())
    trust = tmp_path / "trust.json"
    trust.write_text(json.dumps(inp["trust"]), encoding="utf-8")
    return export, trust


@pytest.mark.parametrize(
    "file,case_id,code,verdict",
    [
        ("strata-checkpoints.json", "healthy", 0, "PASS"),
        ("strata-log.json", "record-altered", 1, "FAIL"),
        ("strata-log.json", "uncheckpointed-tail", 2, "UNKNOWN"),
    ],
)
def test_exit_codes_follow_the_verdict(tmp_path, capsys, file, case_id, code, verdict):
    case = _case(file, case_id)
    export, trust = _export(tmp_path, case)
    argv = ["strata", str(export), "--trust", str(trust), "--json"]
    if "now" in case["input"]:
        argv += ["--now", case["input"]["now"]]
    assert main(argv) == code
    report = json.loads(capsys.readouterr().out)
    assert report["verdict"] == verdict
    assert report["report"] == "1.0" and report["limitations"]
    assert [c["id"] for c in report["checks"]]


def test_missing_records_file_is_a_usage_error(tmp_path, capsys):
    trust = tmp_path / "trust.json"
    trust.write_text("{}")
    assert main(["strata", str(tmp_path), "--trust", str(trust)]) == 64


def test_invalid_trust_is_a_usage_error(tmp_path, capsys):
    export = tmp_path / "e"
    export.mkdir()
    (export / "records.jsonl").write_bytes(b"")
    trust = tmp_path / "trust.json"
    trust.write_text(json.dumps({"trust": "1.0"}))
    assert main(["strata", str(export), "--trust", str(trust)]) == 64


def test_text_report_lists_limitations(tmp_path, capsys):
    case = _case("strata-checkpoints.json", "healthy")
    export, trust = _export(tmp_path, case)
    main(["strata", str(export), "--trust", str(trust), "--now", case["input"]["now"]])
    out = capsys.readouterr().out
    assert out.startswith("PASS") and "limitations:" in out


def test_canon_command(tmp_path, capsysbinary):
    source = tmp_path / "a.json"
    source.write_text('{ "b": 1, "a": [2, 1] }')
    assert main(["canon", str(source)]) == 0
    assert capsysbinary.readouterr().out == b'{"a":[2,1],"b":1}\n'
    source.write_text('{"a": 1.5}')
    assert main(["canon", str(source)]) == 1
