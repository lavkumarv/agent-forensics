"""Configuration loading for agent-forensics.

Resolves settings from (in priority order) explicit arguments, environment
variables (``AGENT_FORENSICS_*``), a TOML config file, then built-in local
defaults. Defaults are chosen so that ``init`` -> ``demo`` works with zero
configuration. The full schema is fleshed out in M11; this module currently
provides the defaults and the resolved-config container.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_HOME = Path.home() / ".agent-forensics"


@dataclass(frozen=True, slots=True)
class Config:
    """Resolved runtime configuration."""

    home: Path = DEFAULT_HOME
    ledger_path: Path = field(default=DEFAULT_HOME / "ledger.db")
    key_path: Path = field(default=DEFAULT_HOME / "signing.key")
    namespace: str = "default"
    async_flush: bool = False
    anchoring: bool = False


def default_config() -> Config:
    """Return the built-in local default configuration."""
    return Config()
