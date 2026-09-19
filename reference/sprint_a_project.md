# Reference material for Week 6 — Project Sprint A

> Source: [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) `s2_organisation_and_version_control/code_structure.md`
> (Apache 2.0), copied in full. This is DTU's "code organization" module (their M6) — it doesn't map to
> any single one of this course's 10 named modules, but it's exactly the kind of project-scaffolding
> content Sprint A needs: by Sprint A, groups have covered Modules 1–5 (Intro, Stages, Git, CI/CD,
> Docker/K8s) and need a standardized way to actually lay out their project repo before continuing.
> See also `pages_projects_and_reports.md` for DTU's project-day structure, checklist, and report
> template, which is the other major input for both Sprint A and Sprint B.

---

# Code organization

!!! info "Core Module"

As developers we tend not to think about code organization much — it's something we let grow organically as needed.
But spending time organizing code upfront pays off in maintainability. The alternative is a "Big Ball of Mud":

!!! quote "Big Ball of Mud"
    *A Big Ball of Mud is a haphazardly structured, sprawling, sloppy, duct-tape-and-baling-wire, spaghetti-code
    jungle... Information is shared promiscuously among distant elements of the system, often to the point where
    nearly all the important information becomes global or duplicated.*
    <br> Brian Foote and Joseph Yoder, *Big Ball of Mud*, PLoP '97

Data science / ML projects differ from traditional software projects in one key way: **data**. That should influence
how we structure the codebase.

## Cookiecutter

[Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/README.html) creates projects from *templates* — a
standardized starting folder/file structure. DTU uses a custom
[MLOps template](https://github.com/SkafteNicki/mlops_template) (a fork of the
[cookiecutter data science template](https://github.com/drivendata/cookiecutter-data-science), specialized toward
MLOps). The point isn't that any one template is objectively best — it's that when a team standardizes on one
template, everyone can navigate each other's projects faster.

**Action item for this course**: either adopt/fork the same DTU/cookiecutter-data-science-style template, or build
our own template reflecting this course's own module structure (feature store folder, cloud-deployment configs per
provider, LLMOps prompt/eval folders, etc.) — this is a concrete decision to make before Sprint A.

## Python project essentials

* `__init__.py` marks a directory as a Python package.
* `pyproject.toml` is the modern, standardized way to describe project metadata (PEP 621) — build system, project
  metadata, dependencies, and (increasingly) other tools' configuration (ruff, mypy, coverage, etc.) all in one file.
  `setup.py`/`setup.cfg` is the older, non-standardized predecessor still seen in older projects.

```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package-name"
version = "0.1.0"
dependencies = [
    'torch==2.1.0',
    'matplotlib>=3.8.1'
]
```

Install in editable/developer mode so code changes take effect without reinstalling:

```bash
pip install -e .        # pip
uv sync                 # uv handles this automatically
```

## Exercises

1. Install cookiecutter: `pip install cookiecutter` (or `uvx cookiecutter`).

2. Start a new project from a template: `cookiecutter <url-to-template>`. Package names should be lowercase,
    underscore-separated, PEP8-compliant, and can't start with a digit.

    *src-layout* (`src/<project_name>/...`) vs. *flat-layout* (`<project_name>/...`) — DTU's template uses src-layout.

3. Create + activate a virtual environment, then install the project into it (`pip install -e .` or `uv sync`).

4. Fill out `data.py` — should take raw data and process/normalize it into an intermediate representation saved to
    `data/processed`.

5. Use `tasks.py` (via `invoke`) for common project tasks (`invoke preprocess-data`, `invoke train`, `invoke --list`).
    This course's own root `tasks.py` (install/precommit/docs/lint/deploy) is a repo-level example of the same
    pattern — worth pointing students at as a working reference.

6. `model.py` — printing model architecture + parameter count when run directly.

7. `train.py` — training logic, saving the trained model to `models/` and training curves/artifacts to
    `reports/figures/`.

8. `evaluate.py` — loads a saved model, prints test-set accuracy.

9. `visualize.py` — loads a pretrained model, extracts an intermediate feature representation, projects it to 2D
    with t-SNE, saves the plot to `reports/figures/`.

10. Update `README.md` with a short description of how to run the project's scripts.

11. Keep `requirements.txt`/`pyproject.toml` dependencies in sync with what the code actually imports.

12. (Optional) Forking/customizing your own cookiecutter template: edit `cookiecutter.json` to add new template
    variables, edit the `{{ cookiecutter.project_name }}` folder contents, test locally with
    `cookiecutter . -f --no-input`, then push to GitHub for reuse.

## Knowledge check

* From-scratch repo bootstrap sequence: create bare repo on GitHub (or `gh repo create`) → run `cookiecutter
  <template>` → `cd <project_name>` → `git init` → `git add .` → `git commit -m "Initial commit"` →
  `git remote add origin ...` → `git push origin master`.

If the chosen template ever needs updating across many already-created projects, [cruft](https://github.com/cruft/cruft)
(works alongside cookiecutter) can propagate template updates into existing projects and validate that a project still
matches its template's latest version — worth a mention for teams standardizing across many student/group projects.

---

## Sprint A framing (this course's own addition — no DTU equivalent)

Sprint A (Week 6) is the checkpoint after Modules 1–5. Suggested sprint deliverables, tied to the modules covered so
far (mirrors DTU's own module-tagged project checklist style, see `pages_projects_and_reports.md`):

* [ ] Git repository created, team has write access (Module 3)
* [ ] Standard branching strategy adopted (dev/feature/bugfix/release) (Module 3)
* [ ] Project scaffolded from a cookiecutter (or equivalent) template (this file)
* [ ] `pyproject.toml`/dependency file kept in sync with actual imports
* [ ] CI pipeline running on push (lint + at least one test) (Module 4)
* [ ] Pre-commit hooks installed
* [ ] Application containerized with a working Dockerfile (Module 5)
* [ ] (If applicable) initial Kubernetes/Compose setup drafted

## Still to source / decide

* Which cookiecutter template this course adopts (DTU's, or a custom one reflecting our 10-module structure)
* Whether Sprint A produces a graded deliverable (a short project-description writeup, mirroring DTU's Project
  Day 1 requirement of a 300-word project description) — see `pages_projects_and_reports.md`
