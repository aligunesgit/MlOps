# Reference material for Week 11 — Module 10: Introduction to AutoML Tools

> Source: [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) `s4_debugging_and_logging/logging.md`
> (Weights & Biases half) and `s10_extra/hyperparameters.md` (Optuna), Apache 2.0, copied in full.
> DTU doesn't teach H2O MLOps, Valohai, Domino Data Lab, neptune.ai, or Iguazio at all — its
> experiment-tracking content is entirely W&B-centric, and its hyperparameter-optimization content is
> Optuna-centric (with a note that W&B's built-in sweep feature is the more actively maintained path).
> Both fit this module's "AutoML/experiment platform" theme well; the other 5 named tools need to be
> covered from scratch (short comparative overview, not full hands-on modules, given DTU has no
> equivalent depth for any of them).

---

## Part 1 — Experiment logging with Weights & Biases (`logging.md`, experiment-logging half)

# Experiment logging

Basic experiment logging (writing loss/accuracy to a file, plotting with matplotlib) works alone or on tiny
projects, but breaks down once collaborating or running many experiments — comparing runs needs a proper tracker.
Options: Tensorboard, Comet, MLflow, Neptune, **Weights & Biases (W&B)** — DTU picks W&B for its course (proprietary
but free for personal use; MLflow is the open-source-first alternative worth mentioning for this module's AutoML
platform survey).

### Setup

```bash
pip install wandb    # or: uv add wandb
wandb login           # paste the 40-character API key from wandb.ai
```

Store the API key in a `.env` file (gitignored), loaded via `python-dotenv`:

```txt
WANDB_API_KEY=your-api-key
WANDB_PROJECT=my_project
WANDB_ENTITY=my_entity
```

### Core logging

```python
import wandb
wandb.init(project="my_project", entity="my_entity", job_type="train", config=hyperparams)
wandb.log({"train_loss": loss, "train_acc": acc})
wandb.log({"input_images": wandb.Image(batch)})   # images, histograms, matplotlib figures also supported
```

* `project` — groups all runs from one experiment line together (shared across a team).
* `entity` — the owning user/team (shared across group members for a class project).
* `job_type` — distinguishes different scripts logging to the same project (e.g. "train" vs. "evaluate") for
  easy dashboard filtering.

### Reproducibility payoff

Every W&B run page's `Overview` tab automatically records: the git repo URL + exact commit hash, the exact launch
command, the full system environment (OS, Python version, installed packages), and a `requirements.txt` snapshot —
reproducing a run is: clone → checkout that commit → install from the snapshot → re-run the logged command.

### Model registry

Trained models get logged as **artifacts** (versioned, immutable file bundles with metadata), then **linked** into a
**model registry** — a centralized, versioned store of "candidate for production" models:

```python
run.link_artifact(artifact=artifact, target_path="model-registry/<registry_name>", aliases=["latest"])
```

Aliases (`latest`, `staging`, `production`, ...) track where in the workflow a given model version sits — this is
exactly the mechanism the CML material (`week4_cicd_strategies.md`, Part 4) hooks into for triggering automated
staged-model tests via webhooks.

### Hyperparameter sweeps (W&B's built-in AutoML feature)

```yaml
# sweep.yaml
program: train.py
method: bayes   # or random, grid
metric:
  goal: minimize
  name: validation_loss
parameters:
  learning_rate: {min: 0.0001, max: 0.1, distribution: log_uniform}
  batch_size: {values: [16, 32, 64]}
run_cap: 10
```

```bash
wandb sweep configs/sweep.yaml   # prints a sweep_id
wandb agent <sweep_id>           # run in multiple terminals to parallelize the search
```

The sweep dashboard supports sorting by metric, parallel-coordinates plots (spotting hyperparameter tendencies),
and importance/correlation plots (which hyperparameters actually matter) — this is W&B's own answer to the
"AutoML tool" pitch of this module, alongside Optuna below.

### Authenticating inside Docker (for training jobs running in CI/cloud)

```bash
docker run -e WANDB_API_KEY=<your-api-key> my_training_image:latest
```

---

## Part 2 — Hyperparameter optimization with Optuna (`hyperparameters.md`)

# Hyperparameter optimization

!!! note "DTU flags this module as outdated in their own material — recommends W&B sweeps instead where possible"

Deep learning models are often not robust to hyperparameter choice, but a full grid search is infeasible when a
single training run takes days. [Optuna](https://optuna.readthedocs.io/) provides smarter search strategies.

### Core concepts

* **Trial** — one experiment (one hyperparameter combination)
* **Study** — a collection of trials
* **Objective** — the function that scores a trial (what's being optimized)

```python
import optuna

def objective(trial):
    lr = trial.suggest_float("lr", 1e-6, 1e0, log=True)
    batch_size = trial.suggest_categorical("batch_size", [16, 32, 64])
    # ...train and evaluate...
    return validation_loss  # optuna minimizes by default

study = optuna.create_study()
study.optimize(objective, n_trials=100)
```

* Default direction is **minimize** — if the metric should be maximized (e.g. accuracy), either negate it or set
  `direction="maximize"` on `create_study`.
* Optuna defaults to **Bayesian optimization** (a more sample-efficient search than grid search), but exhaustive
  grid search is also available via `optuna.samplers.GridSampler` if the search space is small enough.

### Pruning — cutting unpromising trials early

For expensive models (e.g. neural nets with 1000+ combinations to search), **pruning** stops clearly-bad trials
early rather than letting them run to completion:

```python
study = optuna.create_study(pruner=optuna.pruners.MedianPruner())
```

Trade-off: pruning saves compute, but risks discarding a trial that would have improved later (e.g. one with a
temporarily-worse-looking learning curve due to a learning rate warmup) — worth flagging which hyperparameter
choices make pruning riskier (anything affecting training dynamics' shape over time, like learning-rate schedules).

### Distributed/parallel search

Optuna supports running many trials in parallel against a shared database (DTU uses MySQL):

```bash
optuna create-study --study-name "distributed-example" --storage "mysql://root@localhost/example"
```

```python
study = optuna.load_study(study_name="distributed-example", storage="mysql://root@localhost/example")
```

Multiple worker processes each call `study.optimize(...)` against the same storage, parallelizing the search
across however many machines/processes are available.

### Visualization

Optuna's [visualization module](https://optuna.readthedocs.io/en/latest/tutorial/10_key_features/005_visualization.html)
produces parameter-importance plots and optimization-history plots directly from a completed study — useful for
explaining *which* hyperparameters actually mattered, not just which combination won.

---

## Still to source for this module (no DTU equivalent — write from scratch, comparative overview only)

DTU has zero coverage of any of these — a short comparative table (what each platform is for, open-source vs.
managed, standout feature) is more appropriate than a full hands-on module for each, given the time budget:

* **H2O MLOps** — AutoML model training + a full MLOps deployment/monitoring platform (H2O Driverless AI + H2O MLOps)
* **Valohai** — MLOps orchestration platform with a strong pipeline/versioning focus, deployable on any cloud
* **Domino Data Lab** — enterprise data science platform, strong on governance/compliance for regulated industries
* **neptune.ai** — experiment tracker positioned as a lighter-weight, cheaper W&B alternative
* **Iguazio** — full MLOps platform built around the open-source MLRun project (real-time feature store + serving)

A natural framing for this module, given the above: **W&B and Optuna (from DTU) are point solutions** (experiment
tracking, hyperparameter search) that a team bolts onto their own pipeline, whereas **H2O MLOps/Valohai/Domino/
Iguazio are platform plays** that try to own the whole lifecycle — same distinction as the "Open Source tools vs.
Cloud Native tools" comparison already flagged for Module 2 (`week2_ml_mlops_stages.md`), worth cross-referencing.
