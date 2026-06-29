# agent-forensics

> A flight recorder for AI agent memory. When an agent does something bad, trace it back to the
> exact poisoned memory, see the blast radius, and roll it back — without changing how your agent runs.

**agent-forensics** is the DFIR (digital forensics & incident response) layer for AI agent memory.
It intercepts every memory **read** and **write** an agent performs, stamps each with
cryptographically-signed, tamper-evident provenance, and stores those records in an append-only
ledger plus a provenance DAG. After an incident it can trace an action back to the originating
memory write and its source, compute the blast radius of a poisoned source, detect belief drift,
verify the ledger has not been tampered with, and produce a rollback plan.

> **Status:** early development. The build proceeds milestone by milestone (see the build plan).
> This README is a skeleton and will grow as functionality lands.

## Quickstart

```bash
pipx install agent-forensics
agent-forensics demo      # planned: plant a poison, then catch and roll it back
```

> The one-command incident-replay demo is implemented in milestone M11.

## What it does

- **trace** — walk any agent action back to the memory writes and sources that caused it.
- **blast-radius** — compute the forward closure of a poisoned source.
- **drift** — detect when a write contradicts the trusted majority of its semantic cluster.
- **verify** — prove the ledger has not been edited, gapped, or had rows removed.
- **rollback** — produce (and apply) a plan that quarantines poison without deleting history.

## How it integrates

Three capture paths, all backed by the same append-only ledger:

- **Library wrapper** — wrap your memory client in-process.
- **MCP gateway** — proxy an MCP memory server; backend-agnostic.
- **Sidecar** — reverse proxy in front of a hosted vector DB.

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

## License

Apache-2.0. See [LICENSE](LICENSE).
