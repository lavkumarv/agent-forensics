"""Command-line interface for agent-forensics.

The full command surface (init, demo, trace, blast-radius, drift, timeline,
verify, rollback, report, reconcile) is implemented in M11. This module
currently wires up the Typer application and the ``version`` command so the
``agent-forensics`` console script is functional from M0 onwards.
"""

from __future__ import annotations

import typer

from agent_forensics import __version__

app = typer.Typer(
    name="agent-forensics",
    help="Provenance and incident-reconstruction toolkit for AI agent memory.",
    no_args_is_help=True,
    add_completion=False,
)


@app.callback()
def _root() -> None:
    """agent-forensics command-line interface."""


@app.command()
def version() -> None:
    """Print the installed agent-forensics version."""
    typer.echo(__version__)


def main() -> None:
    """Console-script entry point."""
    app()


if __name__ == "__main__":
    main()
