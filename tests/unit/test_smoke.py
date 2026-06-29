"""Smoke tests that prove the package imports and the CLI is wired up."""

from __future__ import annotations

from typer.testing import CliRunner

import agent_forensics
from agent_forensics.cli import app


def test_package_imports() -> None:
    assert isinstance(agent_forensics.__version__, str)


def test_cli_version_command() -> None:
    result = CliRunner().invoke(app, ["version"])
    assert result.exit_code == 0
    assert agent_forensics.__version__ in result.stdout
