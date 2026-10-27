# Copyright 2026 The Ilorium Authors
# SPDX-License-Identifier: Apache-2.0
"""Ilorium verifier: checks evidence against the Ilorium Evidence Format.

This package is isolated on purpose: it depends only on the evidence format and
its pinned libraries (``cryptography``, ``jsonschema``) and never imports the
Probe or any other part of the reference implementation.
"""

__version__ = "0.1.0"
