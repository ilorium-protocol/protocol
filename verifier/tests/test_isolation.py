# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""The verifier is auditable on its own: it imports nothing but the standard library and its pinned dependencies."""

import ast
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1] / "ilorium_verifier"
ALLOWED_THIRD_PARTY = {"cryptography", "jsonschema", "referencing"}
FORBIDDEN_NAMES = {"probe", "gate", "collectors", "correlator", "pulse", "a2a", "cli"}


def _imports(path: Path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name.split(".")[0], node.lineno
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                yield node.module.split(".")[0], node.lineno
            elif node.level > 0 and node.module:
                yield "." + node.module.split(".")[0], node.lineno


def test_imports_are_stdlib_pinned_dependencies_or_siblings():
    siblings = {p.stem for p in PACKAGE.glob("*.py")}
    problems = []
    for path in sorted(PACKAGE.glob("*.py")):
        for name, line in _imports(path):
            if name.startswith("."):
                if name[1:] not in siblings:
                    problems.append(f"{path.name}:{line} relative import of {name}")
            elif name in sys.stdlib_module_names or name in ALLOWED_THIRD_PARTY or name == "ilorium_verifier":
                continue
            else:
                problems.append(f"{path.name}:{line} imports {name}")
    assert not problems, "\n".join(problems)


def test_no_reference_implementation_module_is_named():
    for path in sorted(PACKAGE.glob("*.py")):
        for name, line in _imports(path):
            assert name.lstrip(".") not in FORBIDDEN_NAMES, f"{path.name}:{line} imports {name}"


def test_no_network_or_process_modules():
    banned = {"socket", "http", "urllib", "requests", "httpx", "subprocess", "ssl"}
    for path in sorted(PACKAGE.glob("*.py")):
        for name, line in _imports(path):
            assert name not in banned, f"{path.name}:{line} imports {name}"
