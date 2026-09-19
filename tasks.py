import os

from invoke import task

WINDOWS = os.name == "nt"


@task
def install(ctx) -> None:
    """Create the environment for the course."""
    ctx.run("uv sync --all-extras", echo=True, pty=not WINDOWS)


@task
def precommit(ctx) -> None:
    """Install and run pre-commit checks."""
    ctx.run("uv run pre-commit install", echo=True, pty=not WINDOWS)
    ctx.run("uv run pre-commit run --all-files", echo=True, pty=not WINDOWS)


@task(aliases=["mkdocs"])
def docs(ctx) -> None:
    """Build and serve the documentation locally."""
    ctx.run("uv run mkdocs serve --dirty", echo=True, pty=not WINDOWS)


@task
def lint(ctx) -> None:
    """Run linters."""
    ctx.run("uv run ruff check . --fix", echo=True, pty=not WINDOWS, warn=True)
    ctx.run("uv run ruff format .", echo=True, pty=not WINDOWS, warn=True)


@task
def deploy(ctx) -> None:
    """Deploy the documentation to GitHub Pages."""
    ctx.run("uv run mkdocs gh-deploy --force", echo=True, pty=not WINDOWS)
