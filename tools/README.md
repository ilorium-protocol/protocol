# tools/

Repository tools. Python 3, standard library only unless stated.

| Tool | What it does | Used by |
| --- | --- | --- |
| `vectors_index.py` | Checks `vectors/index.json` (the index `gen_vectors.py` writes: operation, cases and SHA-256 per file, `total_cases`) against the files; `--write` rewrites the hashes and counts after regenerating. | `ci.yml`, `release.yml` |
| `gen_vectors.py` | The independent generator of the conformity vectors (shares no code with the verifier). From the M0 archive. | by hand, when a format changes |
| `check_docs.py` | UTF-8, no tabs, final newline, `.es.md` counterpart for every document. | `ci.yml` (`docs`) |
| `check_schemas.py` | Every JSON under `schemas/` is strict JSON and a valid JSON Schema (needs `jsonschema` when schemas exist; skips with a notice when `schemas/` is empty). | `ci.yml` (`docs`) |
| `check_agent_readable.py` | Scans agent-readable files for hidden-instruction patterns. | `agent-readable-files.yml` |
| `check_dco.py` | DCO sign-off on every commit; agent commits need a sign-off by someone else. | `dco.yml` |
| `check_translation_changelog.py` | Warns on a document change without its translation; fails without a changelog entry. | `translation-changelog.yml` |

The M0 archive (ilorium-m0.tar.gz) adds the verifier's own tools before the first release; see engineering/architecture-v1.md. Draft.
