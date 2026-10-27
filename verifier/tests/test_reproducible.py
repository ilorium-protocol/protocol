# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""The published vectors are exactly what the independent generator produces."""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def test_generator_reproduces_the_published_vectors(tmp_path):
    pytest.importorskip("dilithium_py")
    pytest.importorskip("rfc8785")
    done = subprocess.run([sys.executable, "-I", str(ROOT / "tools" / "gen_vectors.py"), str(tmp_path)],
                          capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    published = {p.name: p.read_bytes() for p in (ROOT / "vectors").glob("*.json")}
    regenerated = {p.name: p.read_bytes() for p in tmp_path.glob("*.json")}
    assert regenerated.keys() == published.keys()
    different = [name for name in published if published[name] != regenerated[name]]
    assert not different, f"not reproducible: {different}"
