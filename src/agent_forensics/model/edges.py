"""Provenance-DAG edge model.

Edges express lineage between records (writes, reads, actions). The store and
traversal live in :mod:`agent_forensics.dag` (M4); this module defines the shape.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from agent_forensics.model.records import utcnow


class EdgeType(StrEnum):
    """Type of a provenance-DAG edge."""

    DERIVED_FROM = "DERIVED_FROM"
    RETRIEVED = "RETRIEVED"
    INFLUENCED = "INFLUENCED"
    CONTEXTUALIZED = "CONTEXTUALIZED"
    CONTRIBUTED_TO = "CONTRIBUTED_TO"
    ROLLED_BACK_BY = "ROLLED_BACK_BY"


class Edge(BaseModel):
    """A directed lineage edge from ``src`` to ``dst``."""

    model_config = ConfigDict(extra="forbid")

    src: str
    dst: str
    edge_type: EdgeType
    created_at: datetime = Field(default_factory=utcnow)
