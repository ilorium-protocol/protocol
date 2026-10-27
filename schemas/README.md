# JSON Schemas (Apache-2.0)

Machine forms of the Evidence Format ([`../specs/evidence-format-v1.md`](../specs/evidence-format-v1.md), release 1.0, draft): `common`, `record`, `pulse`, `checkpoint-meta`, `trust`, `spore`, `bundle`, `vitalsigns`. JSON Schema 2020-12. The verifier loads them from here (`ILORIUM_SCHEMAS=schemas`); `tools/check_schemas.py` validates them in CI. Changing a schema is a method change (IIP) and changes the vectors in the same pull request.
