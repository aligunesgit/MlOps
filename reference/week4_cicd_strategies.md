# Reference material for Week 4 — Module 4: CI/CD Strategies for AWS, Azure, GCP, and GitHub Actions

> Source: [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) `s5_continuous_integration/` modules
> (unittesting.md, github_actions.md, pre_commit.md, cml.md), Apache 2.0 licensed, copied in full.
> DTU's CI/CD material is GitHub-Actions-centric (no AWS/Azure/GCP DevOps pipelines) — this course's
> module additionally needs the AWS CodePipeline/CodeBuild/CodeDeploy/CodeCommit, GCP Cloud Build/Run/
> Deploy, and Azure DevOps (Boards/Repos/Pipelines/Artifacts/IaC) sections written from scratch; DTU
> does not cover those. Also see `week5_docker_kubernetes.md` for the IaC-with-Azure-DevOps cross-link
> from `s10_extra/infrastructure_as_code.md` (excluded from DTU's own published site, but present in
> their repo).

---

## Part 1 — Unit testing (`unittesting.md`)

# Unit testing

!!! info "Core Module"

What often comes to mind for many developers when discussing continuous integration (CI) is code testing.
Continuous integration should ensure that whenever a codebase is updated it is automatically tested such that if bugs
have been introduced in the codebase they will be caught early on. However, it should be noted that applying continuous
integration does not magically ensure that your code does not crash. Continuous integration is only as strong as the
tests that are automatically executed. Continuous integration simply structures and automates this.

!!! quote
    *Continuous Integration doesn't get rid of bugs, but it does make them dramatically easier to find and remove.*
    <br> Martin Fowler, Chief Scientist, ThoughtWorks

The kind of tests we are going to look at are called [unit tests](https://en.wikipedia.org/wiki/Unit_testing). Unit
testing refers to the practice of writing tests that test individual parts of your code base to test for correctness. By
unit, you can therefore think of a function, module or in general any object. By writing tests in this way it should be
very easy to isolate which part of the code broke after an update to the code base. Another way to test your code
base would be through [integration testing](https://en.wikipedia.org/wiki/Integration_testing).

Unit tests (and integration tests) are not a unique concept to MLOps but are a core concept of DevOps. However, it is
important to note that testing machine learning-based systems is much more difficult than traditional systems. The
reason for this is that machine learning systems depend on *data* that influences the state of our system. For this
reason, we not only need unit tests and integration tests of our code but also need data testing, infrastructure testing
and more monitoring to check that we stay within the data distribution we are training on (see Module 9 on model
monitoring).

### Pytest

Python offers a couple of different libraries for writing tests. We are going to use `pytest`.

### Exercises

1. The first part of doing continuous integration is writing the unit tests. Start by creating a `tests` folder.

2. Read the [getting started guide](https://docs.pytest.org/en/6.2.x/getting-started.html) for pytest.

3. Install pytest:

    ```bash
    pip install pytest        # or: uv add --dev pytest
    ```

4. Write some tests. Any files created (except `__init__.py`) should start with `test_*.py`, and any test function
    needs to start with `test_*`:

    ```python
    # this will be found and executed by pytest
    def test_something():
        ...

    # this will not be found and executed by pytest
    def something_to_test():
        ...
    ```

    1. `tests/__init__.py`:

        ```python
        import os
        _TEST_ROOT = os.path.dirname(__file__)
        _PROJECT_ROOT = os.path.dirname(_TEST_ROOT)
        _PATH_DATA = os.path.join(_PROJECT_ROOT, "data")
        ```

    2. Data testing (`tests/test_data.py`) — check that data loads correctly: correct dataset length, correct
        per-sample shape, all labels represented.

    3. Model testing (`tests/test_model.py`) — check that, given an input of shape *X*, the model output has shape *Y*.

    4. Training testing (`tests/test_training.py`) — assert something about the training script itself.

    5. Good code raises errors and warnings in appropriate places (e.g. checking input shape). Use
        `pytest.raises`/`pytest.warns` to test that these fire correctly:

        ```python
        def test_error_on_wrong_shape():
            model = MyModel()
            with pytest.raises(ValueError, match='Expected input to a 4D tensor'):
                model(torch.randn(1, 2, 3))
        ```

    6. Add descriptive messages to `assert` statements: `assert len(x) == N, "Dataset did not have the correct number of samples"`.

    7. Use `pytest.mark.skipif` to skip data-dependent tests when the data files aren't present:

        ```python
        @pytest.mark.skipif(not os.path.exists(file_path), reason="Data files not found")
        def test_something_about_data():
            ...
        ```

5. Make sure tests pass locally: `pytest tests/`.

6. Use `pytest.mark.parametrize` to run the same test with multiple input combinations:

    ```python
    @pytest.mark.parametrize("batch_size", [32, 64])
    def test_model(batch_size: int) -> None:
        model = MyModel()
        x = torch.randn(batch_size, 1, 28, 28)
        y = model(x)
        assert y.shape == (batch_size, 10)
    ```

7. Measure **code coverage** — the percentage of your codebase exercised when all tests run:

    ```bash
    pip install coverage
    coverage run -m pytest tests/
    coverage report -m
    ```

    Exclude files you don't want measured (e.g. the test files themselves) via `pyproject.toml`:

    ```toml
    [tool.coverage.run]
    omit = ["tests/*"]
    ```

### Knowledge check

* 100% code coverage does **not** guarantee a bug-free codebase — it only means every line ran during tests, not that
  every edge case was checked.
* `pytest.mark.parametrize` stacking multiplies out combinatorially — worth walking through with students on the board.

---

## Part 2 — GitHub Actions (`github_actions.md`)

# GitHub Actions

!!! info "Core Module"

Testing your code locally is cumbersome: you need to run it often to catch bugs early, and high coverage requires many
tests that take a long time to run. We want to automate testing so it runs every time we push to the repository. If we
combine this with a branch-protection workflow (push to branches, merge only when checks pass), our code stays fairly
safe against unwanted bugs — assuming test coverage is good.

GitHub Actions is GitHub's own CI solution. Each repository gets 2,000 free minutes/month. Workflow file anatomy:

* `name` — the workflow's name
* `on` — trigger events (push, pull_request, schedule, workflow_dispatch, etc.) and target branches
* `jobs` — parallel by default, can be made dependent on each other
* `runs-on` — the OS/runner
* `steps` — the actual commands to run

### Exercises

1. Create `.github/workflows/` in the repo root.

2. Read [GitHub's guide to testing Python](https://docs.github.com/en/actions/guides/building-and-testing-python).

3. A basic `tests.yaml` workflow: set up Python/uv → install deps → run `pytest`.

4. Push and check the *Actions* tab for a green check mark next to the commit.

5. Run on multiple OSes and Python versions using a build matrix:

    ```yaml
    jobs:
      build:
        runs-on: ${{ matrix.os }}
        strategy:
          fail-fast: false
          matrix:
            os: ["ubuntu-latest", "windows-latest", "macos-latest"]
            python-version: ["3.10", "3.11", "3.12"]
        steps:
          - uses: actions/checkout@v5
          - uses: actions/setup-python@v5
            with:
              python-version: ${{ matrix.python-version }}
    ```

    `fail-fast: false` keeps running the rest of the matrix even if one combination fails.

6. Add caching to speed up dependency installs:

    ```yaml
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"
    ```

7. **Branch protection rules** — `Settings → Rules → Rulesets` — require a pull request before merging, require status
    checks to pass, require reviewer approval. Repository admins can be exempted via a bypass list.

8. Advanced/optional: pulling DVC-tracked data inside CI using a GitHub secret (`GDRIVE_CREDENTIALS_DATA`); a
    `codecheck.yaml` workflow running `ruff check`/`ruff format`/`mypy`; building and pushing a Docker image to Docker
    Hub from a workflow using repository secrets (`DOCKER_HUB_TOKEN`, `DOCKER_HUB_USERNAME`, `DOCKER_HUB_REPOSITORY`).

### Dependabot

`Dependabot` automatically opens PRs to keep dependencies (and GitHub Actions versions) up to date:

```yaml
# .github/dependabot.yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Knowledge check — core vocabulary

* **Workflow** — a YAML file defining what runs on which events, in `.github/workflows/`
* **Runner** — the environment executing the workflow (GitHub-hosted or self-hosted)
* **Job** — a series of steps run on the same runner
* **Action** — the smallest unit in a workflow; jobs consist of multiple actions run sequentially

---

## Part 3 — Pre-commit (`pre_commit.md`)

# Pre-commit

Pre-commit hooks let you automate quality checks (formatting, linting, large-file checks, etc.) every time you run
`git commit`, before the commit is even created — catching problems before they ever reach CI.

`pre-commit` works via a `.pre-commit-config.yaml` file:

```yaml
repos:
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v3.2.0
  hooks:
  - id: trailing-whitespace
  - id: end-of-file-fixer
  - id: check-yaml
  - id: check-added-large-files
```

### Exercises

1. `pip install pre-commit` (or `uv add --dev pre-commit`)
2. `pre-commit sample-config > .pre-commit-config.yaml`
3. `pre-commit install` — hooks it into `git commit`
4. `pre-commit run --all-files` — checks every file in the repo, not just staged ones
5. Add the `ruff` pre-commit hook:

    ```yaml
    - repo: https://github.com/astral-sh/ruff-pre-commit
      rev: v0.4.7
      hooks:
        - id: ruff
          args: ["--fix"]
        - id: ruff-format
        - id: ruff
    ```

6. Skip hooks in a hurry: `git commit -m <message> --no-verify`. Disable entirely: `pre-commit uninstall`.
7. Advanced/optional: a GitHub Actions workflow that runs `pre-commit` on every push and auto-commits any fixes
    (using the `pre-commit/action` + `stefanzweifel/git-auto-commit-action` combo), and a scheduled workflow that runs
    `pre-commit autoupdate` weekly and opens a PR with the config bump.

---

## Part 4 — Continuous Machine Learning / CML (`cml.md`)

# Continuous Machine Learning (CML)

Classical CI (tests + linting) has DevOps roots and applies to any software project. **Continuous Machine Learning**
(CML) is the ML-specific layer on top: automating checks that are unique to ML pipelines —
*Did I train on the correct data? Did the model converge? Did a tracked metric improve? Did I over/underfit?*

### MLOps maturity model

| Level | Characteristics |
|---|---|
| 0 | Ad-hoc ML: no standardization, no version control, no testing, no monitoring |
| 1 | Basic DevOps practices: version control, basic CI |
| 2 | Standardized, reproducible training; centralized model artifacts/metadata; model versioning/registry |
| 3 | CI + CD: automated model testing, production monitoring |
| 4 | Full CML: automated training, evaluation, deployment, automated retraining |

CML is the top of the maturity ladder — the automation covered in this part is some of the most advanced content in
the course.

### Exercises (from DTU's `cml` framework by iterative.ai, built on GitHub Actions)

1. **Data-triggered workflows** — a workflow (`cml_data.yaml`) that activates only when files under `data/` (or
    `.dvc` metafiles) change:

    ```yaml
    on:
      pull_request:
        branches: [main]
        paths:
          - '**/*.dvc'
          - '.dvc/**'
    ```

    The job then checks out code, sets up Python, authenticates to cloud storage, pulls the data (`dvc pull`), and runs
    a `dataset_statistics` function that reports sample counts, class distribution, and example images.

2. Use `cml comment create data_statistics.md` to have the bot post the generated statistics report directly on the
    pull request.

3. **Model-registry-triggered workflows** — using a webhook from a model registry (e.g. Weights & Biases) that fires
    a `repository_dispatch` event to GitHub whenever a model version is tagged `staging`:

    ```yaml
    on:
      repository_dispatch:
        types: staged_model
    ```

    The workflow then: identifies the staged model from the payload → runs performance tests against it (e.g. "100
    inferences in under 1 second") → if it passes, promotes the model by adding a `production` alias via the registry's
    API.

4. (Optional/advanced) Combine both: `cml pr create` instead of `cml comment create` so a human has to approve the PR
    before the production alias gets added — keeping a human in the loop before deployment.

### Knowledge check

* CI vs. CML: CI tests code; CML tests/automates the whole ML lifecycle (data, training, eval, deploy, monitor).
* Even at maturity level 4 (full automation), **human oversight should remain** in high-stakes domains (e.g. medical,
  safety-critical) — full auto-retraining isn't always the right target maturity level.

---

## Part 5 — Infrastructure as Code (`s10_extra/infrastructure_as_code.md`) — for the Azure DevOps "IaC" bullet

> DTU's own file opens with `!!! danger "Module is still under development"` — this is a skeleton, copied in full.

# Infrastructure as Code (IaC)

IaC manages/provisions infrastructure via machine-readable definition files instead of manual/interactive
configuration — infrastructure becomes versionable, testable, code.

**Terraform** (HashiCorp) — multi-cloud (AWS/Azure/GCP/others), configuration written in HCL (HashiCorp
Configuration Language) or JSON.

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
}
```

```bash
terraform init    # initialize the working directory
terraform apply   # provision/update infrastructure to match the config
```

DTU's draft stops here (install instructions + this one example). **This is the exact same topic Module 4's own
list calls out as "Infrastructure as Code (IaC) with Azure DevOps"** — the natural extension for this course is
showing the *Azure-specific* IaC path (ARM templates / Bicep, or Terraform's `azurerm` provider) integrated into an
Azure Pipelines YAML step, which has no DTU equivalent at all — write from scratch.

---

## Still to source for this module (not covered by any DTU page — write from scratch)

* **AWS DevOps**: CodePipeline, CodeBuild, CodeDeploy, CodeCommit + project pipeline
* **GCP DevOps**: Cloud Run, Cloud Build, Cloud Deploy, Artifact Registry, Cloud Source Repositories + project pipeline
  (DTU's `s6_the_cloud/using_the_cloud.md` covers GCP compute/storage/Vertex AI but not this Cloud Build/Deploy CI/CD
  angle specifically — cross-check that file when writing this section, see `week8_cloud_deep_dive.md`)
* **Azure DevOps**: Boards, Repos, Pipelines, Test Plans, Artifacts, YAML pipeline structure + project pipeline —
  entirely new content, no DTU equivalent (IaC-with-Azure-DevOps specifically is covered just above in Part 5)
* **GitHub Pages** — DTU covers deploying *their own* docs site via Pages/mkdocs (see `sprint_b_final_project.md`,
  sourced from `s10_extra/documentation.md`) — reusable as a simple example of a GitHub Actions → GitHub Pages
  deploy workflow
