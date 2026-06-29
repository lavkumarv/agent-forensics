# agent-forensics

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Checked with mypy](https://img.shields.io/badge/mypy-strict-2a6db2.svg)](https://mypy-lang.org/)
[![Linted with ruff](https://img.shields.io/badge/lint-ruff-261230.svg)](https://docs.astral.sh/ruff/)

> A flight recorder for AI agent memory. When an agent does something bad, trace it back to the
> exact poisoned memory, see the blast radius, and roll it back — without changing how your agent runs.

**agent-forensics** is the DFIR (digital forensics & incident response) layer for AI agent memory.
It intercepts every memory **read** and **write** an agent performs, stamps each with
cryptographically-signed, tamper-evident provenance, and stores those records in an append-only
ledger plus a provenance DAG. After an incident it can trace an action back to the originating
memory write and its source, compute the blast radius of a poisoned source, detect belief drift,
verify the ledger has not been tampered with, and produce a rollback plan.

## Quickstart

```bash
pipx install agent-forensics
agent-forensics init      # create the ledger, signing key, and profile
agent-forensics demo      # plant a poison, then trace, blast-radius, and roll it back
```

`demo` runs the full incident replay end-to-end with zero configuration: a
poisoned document is planted, a later turn retrieves it and acts harmfully, and
the tool traces it to the exact memory, shows the blast radius, rolls it back, and
proves the re-run is no longer harmful — all while the ledger keeps verifying.

```text
$ agent-forensics demo
=== agent-forensics incident replay ===

Poison planted:        019f14b7-2ba6-7e2b-aa6c-ea5e727dd9a8
Harmful action taken:  019f14b7-2ba8-718f-92d9-c917790cb7fa (HARMFUL)
trace -> root cause:   019f14b7-2ba6-7e2b-aa6c-ea5e727dd9a8 (correct)
blast radius:          3 record(s)
rollback affected:     3 record(s)
Re-run after rollback: no longer harmful
Ledger integrity:      VERIFIED
```

## What it does

- **trace** — walk any agent action back to the memory writes and sources that caused it.
- **blast-radius** — compute the forward closure of a poisoned source.
- **drift** — detect when a write contradicts the trusted majority of its semantic cluster.
- **verify** — prove the ledger has not been edited, gapped, or had rows removed.
- **rollback** — produce (and apply) a plan that quarantines poison without deleting history.

## How it integrates

Three capture paths, all backed by the same append-only ledger:

- **Library wrapper** — wrap your memory client in-process (adapters for Mem0,
  Chroma, Letta, pgvector, and the `MEMORY.md`/`CLAUDE.md`/`AGENTS.md` file surface).
- **MCP gateway** — proxy an MCP memory server; backend-agnostic.
- **Sidecar** — reverse proxy in front of a hosted vector DB (Pinecone, Qdrant,
  Weaviate, Mongo Atlas).

`agent-forensics reconcile` is the honesty check: it flags backend entries that
have no ledger record (writes that bypassed capture).

## Library usage

```python
from agent_forensics.capture.engine import Forensics
from agent_forensics.crypto import keys
from agent_forensics.model.records import Source, SourceType, TrustLevel
from agent_forensics.query.trace import trace

forensics = Forensics.open("forensics.db", keys.generate())

# Record a write, a retrieval that surfaced it, and an action it informed.
source = Source(source_type=SourceType.document_ingest, trust_level=TrustLevel.untrusted,
                locator="https://example.test/onboarding.md")
note = forensics.record_write("ingested onboarding note", source, namespace="agent")
read = forensics.record_retrieval("onboarding policy", returned=[note.record_id], namespace="agent")
act = forensics.record_action("email.send", "sent onboarding email",
                              context_retrievals=[read.retrieval_id], namespace="agent")

# Later: trace the action back to its root-cause memory.
result = trace(forensics.ledger, forensics.dag, act.action_id)
print(result.primary.record_id, result.primary.trust_level)  # -> note.record_id untrusted
```

## Integrity model

The ledger is **append-only**: rollbacks append new events, never edit or delete. A BLAKE3
hash-chain proves no row was edited; a periodically-checkpointed, signed Merkle root proves no row
was removed. Every entry is Ed25519-signed by a key the agent never sees.

## Development

```bash
uv sync --all-extras
uv run pytest
uv run ruff check .
uv run mypy
```

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) — conceptual model, data model, and algorithms
- [docs/spec.md](docs/spec.md) — versioned ProvenanceRecord schema
- [docs/threat-model.md](docs/threat-model.md) — assets, adversary, and mitigations
- [CONTRIBUTING.md](CONTRIBUTING.md) — dev setup and how to add a detector or adapter
- [SECURITY.md](SECURITY.md) — disclosure policy and the tool's own integrity posture

## Status

Early development; APIs may change before 1.0. The tamper-evident ledger,
provenance DAG, query engine, detectors, adapters, MCP gateway, and CLI are
implemented and tested. See [`ARCHITECTURE.md`](ARCHITECTURE.md) for what is built
and what is on the roadmap (notably external transparency-log anchoring).

This is **post-incident reconstruction** — provenance, blast radius, and rollback.
It does not block attacks at runtime; pair it under your runtime guardrails.

## License

Apache-2.0. See [LICENSE](LICENSE). Contributions are accepted under Apache-2.0
with a DCO sign-off (`git commit -s`).
