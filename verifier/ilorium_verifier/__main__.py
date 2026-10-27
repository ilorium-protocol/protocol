# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Command line: ``python -m ilorium_verifier``.

Exit status: 0 PASS, 1 FAIL, 2 UNKNOWN, 64 usage or input error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .canon import CanonError, canonicalize, parse_strict
from .conformity import run_directory
from .bundle import verify_bundle
from .spore import verify_spore
from .vitalsigns import verify_vitalsigns
from .strata import verify_strata
from .trust import TrustError, load_trust

EXIT = {"PASS": 0, "FAIL": 1, "UNKNOWN": 2}
USAGE_ERROR = 64


def _read_optional(path: Path) -> bytes | None:
    return path.read_bytes() if path.is_file() else None


def _cmd_strata(args: argparse.Namespace) -> int:
    directory = Path(args.directory)
    records = _read_optional(directory / "records.jsonl")
    if records is None:
        print(f"error: {directory / 'records.jsonl'} not found", file=sys.stderr)
        return USAGE_ERROR
    try:
        trust = load_trust(json.loads(Path(args.trust).read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, TrustError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return USAGE_ERROR
    report = verify_strata(
        records=records,
        checkpoints=_read_optional(directory / "checkpoints.jsonl"),
        pulses=_read_optional(directory / "pulses.jsonl"),
        trust=trust,
        now=args.now,
    )
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"{report['verdict']}  {report['organism']}  {report['origin']}")
        print(f"summary: {json.dumps(report['summary'], ensure_ascii=False)}")
        for check in report["checks"]:
            line = f"  {check['verdict']:<8}{check['id']}"
            print(line + (f"  {check['detail']}" if check["detail"] else ""))
        for gap in report["gaps"]:
            print(f"  gap     {json.dumps(gap, ensure_ascii=False)}")
        print("limitations:")
        for item in report["limitations"]:
            print(f"  - {item}")
    return EXIT[report["verdict"]]


def _cmd_spore(args: argparse.Namespace) -> int:
    try:
        data = Path(args.file).read_bytes()
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return USAGE_ERROR
    report = verify_spore(data)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(report["verdict"])
        for check in report["checks"]:
            print(f"  {check['verdict']:<8}{check['id']}" + (f"  {check['detail']}" if check["detail"] else ""))
    return EXIT[report["verdict"]]


def _read_bundle(directory: Path) -> dict[str, bytes]:
    """Every entry of the directory by name; a subdirectory appears as an empty ``name/`` so it is reported as unlisted."""
    files: dict[str, bytes] = {}
    for entry in sorted(directory.iterdir()):
        files[entry.name if entry.is_file() else entry.name + "/"] = entry.read_bytes() if entry.is_file() else b""
    return files


def _print_report(report: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    print(f"{report['verdict']}  {report['organism']}  {report['origin']}")
    for check in report["checks"]:
        print(f"  {check['verdict']:<8}{check['id']}" + (f"  {check['detail']}" if check.get("detail") else ""))
    for gap in report.get("gaps", []):
        print(f"  gap     {json.dumps(gap, ensure_ascii=False)}")
    if "limitations" in report:
        print("limitations:")
        for item in report["limitations"]:
            print(f"  - {item}")


def _cmd_bundle(args: argparse.Namespace) -> int:
    directory = Path(args.directory)
    try:
        trust = load_trust(json.loads(Path(args.trust).read_text(encoding="utf-8")))
        files = _read_bundle(directory)
    except (OSError, json.JSONDecodeError, TrustError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return USAGE_ERROR
    report = verify_bundle(files, trust, args.now)
    _print_report(report, args.json)
    return EXIT[report["verdict"]]


def _cmd_vitalsigns(args: argparse.Namespace) -> int:
    try:
        data = Path(args.file).read_bytes()
        bundle = _read_bundle(Path(args.bundle)) if args.bundle else None
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return USAGE_ERROR
    report = verify_vitalsigns(data, bundle)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(report["verdict"])
        for check in report["checks"]:
            print(f"  {check['verdict']:<8}{check['id']}" + (f"  {check['detail']}" if check["detail"] else ""))
    return EXIT[report["verdict"]]


def _cmd_canon(args: argparse.Namespace) -> int:
    try:
        value = parse_strict(Path(args.file).read_bytes())
    except (OSError, CanonError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write(canonicalize(value) + b"\n")
    return 0


def _cmd_conformity(args: argparse.Namespace) -> int:
    results = run_directory(Path(args.directory))
    failed = [r for r in results if not r.ok]
    for item in failed:
        print(f"FAIL  {item.vector_id}: {item.message}")
    print(f"{len(results) - len(failed)} of {len(results)} vectors passed")
    return 1 if failed or not results else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ilorium-verifier", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    strata = sub.add_parser("strata", help="verify a Strata export directory")
    strata.add_argument("directory")
    strata.add_argument("--trust", required=True, help="trust configuration (JSON)")
    strata.add_argument("--now", help="current time (UTC, e.g. 2026-11-03T14:30:00Z) to check freshness")
    strata.add_argument("--json", action="store_true", help="print the report as JSON")
    strata.set_defaults(func=_cmd_strata)
    spore = sub.add_parser("spore", help="check a Spore document")
    spore.add_argument("file")
    spore.add_argument("--json", action="store_true", help="print the report as JSON")
    spore.set_defaults(func=_cmd_spore)
    bundle = sub.add_parser("bundle", help="verify an Evidence Bundle directory")
    bundle.add_argument("directory")
    bundle.add_argument("--trust", required=True, help="trust configuration (JSON), never part of the bundle")
    bundle.add_argument("--now", help="current time (UTC) to check freshness")
    bundle.add_argument("--json", action="store_true", help="print the report as JSON")
    bundle.set_defaults(func=_cmd_bundle)
    vital = sub.add_parser("vitalsigns", help="check Vital Signs against the Evidence Bundle they link to")
    vital.add_argument("file")
    vital.add_argument("--bundle", help="the bundle directory; without it the result is UNKNOWN")
    vital.add_argument("--json", action="store_true", help="print the report as JSON")
    vital.set_defaults(func=_cmd_vitalsigns)
    canon = sub.add_parser("canon", help="print the canonical form of a JSON file")
    canon.add_argument("file")
    canon.set_defaults(func=_cmd_canon)
    conformity = sub.add_parser("conformity", help="run conformity vectors")
    conformity.add_argument("directory")
    conformity.set_defaults(func=_cmd_conformity)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
