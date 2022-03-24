#!/usr/bin/env python3

import logging
import pathlib
import typing

import structlog
import structlog.contextvars
import structlog.processors
import structlog.types
import typer

from . import parse_repo_url
from .clone import clone

app = typer.Typer()


@app.command()
def main(
    url: str = typer.Argument(..., help="Repo URl to clone"),
    prefix: str = typer.Option(
        "~/src", help="Prefix to clone to. Will clone to `{prefix}/{host}/{org}/{repo}`"
    ),
    verbose: bool = typer.Option(
        False, "--verbose/--no-verbose", "-v", help="Enable more verbose log output"
    ),
    debug: bool = typer.Option(
        False, "--debug/--no-debug", "-d", help="Enable more debug log output"
    ),
    json: bool = typer.Option(
        False,
        "--json/--no-json",
        "-j",
        envvar="CLONE_REPO_JSON_LOGS",
        help="Use JSON for log output",
    ),
    no_act: bool = typer.Option(
        False, "--no-act/--act", "-n", help="Simulate the clone"
    ),
    fetch: bool = typer.Option(
        False,
        "--fetch/--no-fetch",
        "-f",
        help="If the destination exists use a git fetch instead",
    ),
) -> None:
    """Clone the given repo URL to a common prefix"""
    prefix_path = pathlib.Path(prefix).expanduser().resolve()

    processors: typing.List[structlog.types.Processor] = (
        [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ]
        if json
        else [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ]
    )

    structlog.configure(
        cache_logger_on_first_use=True,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.INFO if verbose else (logging.DEBUG if debug else logging.WARNING)
        ),
        processors=processors,
    )

    structlog.contextvars.reset_contextvars()
    structlog.contextvars.bind_contextvars(
        url=url,
        prefix=prefix_path,
        verbose=verbose,
        debug=debug,
        json=json,
        no_act=no_act,
        fetch=fetch,
    )

    log = structlog.get_logger()

    log.debug("config", config=structlog.get_config())

    try:
        repo_url = parse_repo_url.parse_url(url)
        if repo_url is None:
            raise ValueError(f"Couldn't parse {url}")

        clone(
            repo_url=repo_url,
            no_act=no_act,
            fetch=fetch,
            prefix_path=prefix_path,
        )
    except Exception as e:
        log.fatal(f"Error: {e}", exc_info=debug or json)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
