# Supplementary — Dev tooling: CLIs & good coding practice (not mapped to a specific week)

> Source: [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) `s2_organisation_and_version_control/cli.md`
> and `good_coding_practice.md` (Apache 2.0), copied in full. Neither maps cleanly onto this course's 10
> named modules — CLIs (typer/invoke) and coding-style/typing/linting aren't named topics in any of our
> modules' bullet lists. Kept here as optional/enrichment material; could be folded into Sprint A as
> "extra polish" content if time allows, or offered as an optional reading.

---

## Part 1 — Command line interfaces (`cli.md`)

# Command line interfaces

As projects grow, `python my_script.py` stops being enough — a proper CLI gives users of your code a single,
documented entrypoint. Three complementary approaches:

### 1. Project scripts (via `pyproject.toml`)

```toml
[project.scripts]
train = "my_project.train:main"
```

```bash
pip install -e .
train              # now runs my_project.train:main directly, no `python` prefix needed
# or with uv:
uv run train
```

### 2. `typer` for argument parsing with subcommands

`argparse` handles simple flags but struggles with git-style subcommands (`git push`, `git pull`, ...). `typer`
extends `argparse`-like ergonomics to subcommands:

```python
import typer
app = typer.Typer()

@app.command()
def hello(count: int = 1, name: str = "World"):
    for _ in range(count):
        typer.echo(f"Hello {name}!")

if __name__ == "__main__":
    app()
```

Nested subcommands work the same way `git remote add/rename` does — e.g. `train svm --kernel linear` vs.
`train knn --n-neighbors 5`. Note: `_` in a variable name becomes `-` in the CLI flag (`n_neighbors` → `--n-neighbors`).

### 3. `invoke` for project task automation (a Python-native Makefile alternative)

```python
from invoke import task

@task
def git(ctx, message):
    ctx.run("git add .")
    ctx.run(f"git commit -m '{message}'")
    ctx.run("git push")
```

```bash
invoke --list          # see available tasks
invoke git --message "My commit message"
```

Key `ctx.run` arguments: `warn` (don't raise if the command fails), `pty` (run in a pseudo-terminal), `echo` (print
the command before running it).

A useful combined task: `dvc pull` (fetch data) as a prerequisite for a `train` task that then runs a CLI entrypoint —
demonstrates composing all three CLI layers together.

---

## Part 2 — Good coding practice (`good_coding_practice.md`)

# Good coding practice

!!! quote
    *Code is read more often than it is written.* — Guido Van Rossum

Consistency matters more than any specific rule.

### Documentation

* Under-documentation: obvious things get comments, hard things don't.
* Over-documentation: nobody reads walls of comments — they get skipped.
* *"Code tells you how; comments tell you why."* — Jeff Atwood. Comment intent/rationale, not mechanics.
* Add [docstrings](https://www.python.org/dev/peps/pep-0257/) with standardized keywords (`Args`, `Returns`, etc.)

### Styling

[PEP8](https://www.python.org/dev/peps/pep-0008/) is Python's official style guide. [ruff](https://github.com/astral-sh/ruff)
(fast, actively developed) has replaced `flake8`/`black`/`isort` as the modern all-in-one linter + formatter:

```bash
ruff check .          # lint
ruff format .         # auto-format (drop-in black replacement)
```

Configure via `pyproject.toml`:

```toml
[tool.ruff]
line-length = 120
lint.select = ["I"]   # import sorting
```

### Typing

Python doesn't require type hints, but they improve readability and enable static checking:

```python
def add2(x: int, y: int) -> int:
    return x + y

# python >= 3.10
def add2(x: int | float | Tensor, y: int | float | Tensor) -> int | float | Tensor:
    return x + y
```

[mypy](https://mypy.readthedocs.io/en/stable/index.html) statically checks that your type hints are internally
consistent (it doesn't execute your code, just scans it). [ty](https://docs.astral.sh/ty/) is a newer, faster
alternative from the `uv`/`ruff` team, still in beta.

### Knowledge check

* PEP8 class naming: `CapWords` (`MyClass`, not `myclass`); function/method naming: `snake_case` (`train_network`,
  not `TrainNetwork`).
* Google has [its own Python style guide](https://google.github.io/styleguide/pyguide.html) that diverges from PEP8
  in places — the point is internal team consistency, not literal PEP8 compliance.
