"""Drift: consensus-flip events over time.

The signature is fixed here in M6; the embedding-backed implementation lands in
M8. Until then ``drift`` returns an empty list so callers and the CLI can wire it
up without a hard dependency on the embedding backend.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agent_forensics.ledger.store import LedgerStore


@dataclass(frozen=True, slots=True)
class DriftEvent:
    """A point where the trusted consensus on a topic flipped."""

    topic: str
    record_id: str
    source_id: str | None
    timestamp: str
    detail: str


def drift(ledger: LedgerStore, topic_or_cluster: str) -> list[DriftEvent]:
    """Return consensus-flip events for a topic (implemented in M8)."""
    return []
