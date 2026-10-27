#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright The Ilorium Authors
"""Check the Developer Certificate of Origin sign-off on a range of commits.

Rules (CONTRIBUTING.md, "Sign-off and signatures" and "Agents"):
  1. Every commit carries at least one `Signed-off-by: Name <email>` trailer.
  2. An agent commit must carry a sign-off by someone other than its author.
     A commit is an agent commit when its author name contains "(AI)" and its
     author email ends with "@ilorium.com", or when --agent-authored is given
     (the pull request carries the label `agent-authored`).

Merge commits are skipped. Standard library only; calls `git`.

Usage:
    python3 tools/check_dco.py BASE_SHA HEAD_SHA [--agent-authored]
"""

from __future__ import annotations

import re
import subprocess
import sys

SIGNOFF = re.compile(r"^Signed-off-by:\s*(.+?)\s*<([^>]+)>\s*$", re.M)
SEP = "\x1f"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def commits(base: str, head: str) -> list[dict]:
    fmt = SEP.join(["%H", "%an", "%ae", "%P", "%B"]) + "\x1e"
    out = git("log", "--format=" + fmt, f"{base}..{head}")
    result = []
    for rec in out.split("\x1e"):
        rec = rec.strip("\n")
        if not rec.strip():
            continue
        sha, an, ae, parents, body = rec.split(SEP, 4)
        result.append({"sha": sha, "an": an, "ae": ae, "merge": len(parents.split()) > 1, "body": body})
    return result


def is_agent(an: str, ae: str) -> bool:
    return "(AI)" in an and ae.lower().endswith("@ilorium.com")


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("-")]
    label_agent = "--agent-authored" in argv
    if "--help" in argv or "-h" in argv:
        print(__doc__)
        return 0
    if len(args) != 2:
        print(__doc__)
        return 2
    base, head = args
    problems: list[str] = []
    checked = 0
    for c in commits(base, head):
        if c["merge"]:
            continue
        checked += 1
        short = c["sha"][:10]
        signoffs = [(n.strip(), e.strip().lower()) for n, e in SIGNOFF.findall(c["body"])]
        if not signoffs:
            problems.append(f"{short}: no Signed-off-by trailer (use `git commit -s`)")
            continue
        agent = label_agent or is_agent(c["an"], c["ae"])
        if agent:
            others = [s for s in signoffs if s[1] != c["ae"].lower()]
            if not others:
                problems.append(f"{short}: agent commit by {c['an']} <{c['ae']}> signed off only by itself; a responsible human or organization must sign off")
            else:
                print(f"ok: {short}: agent commit, sign-off by {others[0][0]} <{others[0][1]}>")
        else:
            print(f"ok: {short}: sign-off by {signoffs[0][0]} <{signoffs[0][1]}>")
    for p in problems:
        print(f"error: {p}")
    print(f"check_dco: {checked} commit(s) checked, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
