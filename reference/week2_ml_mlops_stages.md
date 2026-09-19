# Reference material for Week 2 — Module 2: Overview of ML and MLOps Stages

> Source: [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) — `s2_organisation_and_version_control/dvc.md`
> (Versioning: Data) and `s3_reproducibility/config_files.md` (Reproducibility), Apache 2.0, copied in full.
> These map to two of Module 2's many bullets ("Versioning Data..." and "Reproducibility") — the rest of
> Module 2 (MLOps Maturity Model, stages, testing, automation, deployment, monitoring, architectures,
> open-source vs. cloud-native tooling, roles) has no DTU equivalent and needs to be written from scratch;
> DTU's course doesn't teach a maturity-model framing this early (their closest equivalent, the MLOps
> maturity model table, appears later in `s5_continuous_integration/cml.md` — see `week4_cicd_strategies.md`,
> Part 4 — worth reusing/cross-linking here).

---

## Part 1 — Data Version Control / DVC (`dvc.md`) — for the "Versioning: Data, Code, Model..." bullet

# Data Version Control

!!! info "Core Module"

Classic version control was built to track code files — simple text, even a 1000+ file codebase is usually under 1GB.
Data is drastically bigger; modern ML models train on petabytes. Frameworks like [DVC](https://dvc.org/),
[DAGsHub](https://dagshub.com/), [Hub](https://www.activeloop.ai/), and others solve this the same way: instead of
storing large artifact files directly, they store a small *pointer* file and version-control the pointer instead of
the artifact.

## DVC: What is it?

DVC is an extension of `git` that also versions data, models and experiments. It keeps a small *metafile* that points
to a remote location where the actual data lives (Google Drive, an S3 bucket, etc.). You get two remotes: one for code
(`git pull/push`) and one for data (`dvc pull/push`). The connection is between the large data file (e.g. `model.pkl`)
and its small metafile (`model.pkl.dvc`) — the large file lives in the data remote, the small metafile lives in the
code remote (and gets committed to git normally).

## Exercises

1. Set up a remote storage location (DTU uses Google Drive; equally valid: S3, GCS, Azure Blob, or an institution's
    own storage/HPC via SSH remote).

2. Install DVC and the relevant remote-storage extension:

    ```bash
    pip install dvc dvc-gdrive   # or dvc[s3], dvc[azure], dvc[gs], dvc[all], etc.
    ```

3. `dvc init` in your project repo — sets up DVC similarly to `git init`. Commit the resulting DVC files to git.

4. Add remote storage:

    ```bash
    dvc remote add -d storage gdrive://<your_identifier>
    git add .dvc/config
    ```

5. Track a data folder: `dvc add data/` — creates a human-readable `.dvc` metafile placeholder, and the `data/` folder
    gets added to `.gitignore` automatically.

6. Commit and tag the metafiles so you can restore this exact data state later:

    ```bash
    git add data.dvc .gitignore
    git commit -m "First dataset, containing N images"
    git tag -a "v1.0" -m "data v1.0"
    ```

7. Push data to remote storage: `dvc push` (first run requires authenticating). Confirm the raw data never ends up
    committed to the GitHub repo itself — only the pointer files do.

8. Others (or you, elsewhere) can now reproduce both code and data:

    ```bash
    git clone <repo>
    cd <repo>
    dvc pull
    ```

9. Versioning a new version of the data: add new files, `dvc add` → `git add` → `git commit` → `git tag` → `dvc push`
    → `git push`.

10. Roll back to an earlier data version:

    ```bash
    git checkout v1.0
    dvc checkout
    ```

11. (Optional) DVC isn't just for raw data — it's equally useful for versioning large model checkpoint files.

## Performance note

DVC handles a small number of large files well, but performs poorly with datasets made of *many small files*. If
that's the shape of your data, either zip it into a single archive (unzip at runtime) or convert to a single-file
tabular format (`.parquet`/`.csv`) before version-controlling it.

## Knowledge check

* A repo using DVC has a `.dvc` folder (parallel to `.git`), or check with `dvc status`.
* Adding a new `data/` folder to version control: `dvc add data/` → `git add .` → `git commit` → `git push` → `dvc push`.

---

## Part 2 — Config Files / Hydra (`config_files.md`) — for the "Reproducibility" bullet

# Config files

Docker (see Module 5) gives us environment-level reproducibility, but that alone doesn't make *experiments*
reproducible. A well-known study reproducing 255 papers found "hyperparameters specified" to be one of the significant
factors determining whether a result could be reproduced at all.

## Configuring experiments — the maturity ladder

1. **Hardcoded hyperparameters** in the script (`class my_hp: batch_size = 64 ...`) — easy to lose track of what
    config produced which result; requires editing the script for every new run.
2. **Argument parser** (`python train.py --batch_size 256 --learning_rate 1e-4`) — configurable, but still easy to
    lose the exact config used for a given experiment if you're not disciplined.
3. **Config files** (Hydra + OmegaConf) — hyperparameters live in versioned `.yaml` files, systematically saved
    alongside each experiment run.

```yaml
# config.yaml
hyperparameters:
  batch_size: 64
  learning_rate: 1e-4
```

```python
import hydra

@hydra.main(config_name="config.yaml")
def main(cfg):
    print(cfg.hyperparameters.batch_size, cfg.hyperparameters.learning_rate)

if __name__ == "__main__":
    main()
```

Separating hyperparameters into `.yaml` files disentangles configuration from the model code, making the
configuration itself independently version-controllable.

## Exercises

1. `pip install hydra-core` (or `uv add hydra-core`).
2. Identify all the hyperparameters hiding in an existing script (batch size, learning rate, hidden dims, epochs,
    and — easy to forget — the random seed, which is needed for full reproducibility: `torch.manual_seed(seed)`).
3. Extract them into a `config.yaml`.
4. Load the config in the script via `@hydra.main`.
5. Run it, and inspect Hydra's auto-generated `outputs/<date>/<time>/` folder — hyperparameters and logs are saved
    per run automatically.
6. Override parameters from the CLI without touching the config file:

    ```bash
    python train.py hyperparameters.seed=1234
    python train.py +experiment.new_param=42
    ```

7. Hydra defaults to capturing only Python's native `logging` output (not `print`) into its per-run log file —
    switch `print(...)` calls to `log.info(...)` (`log = logging.getLogger(__name__)`) so console output is preserved
    alongside the config.
8. Verify reproducibility across two runs with the same config, comparing saved weights + config.
9. Multiple named experiment configs (`conf/experiments/exp1.yaml`, `exp2.yaml`), selected via `python train.py
    experiment=exp2` — never hand-edit the "live" config file per run.
10. Hydra's `instantiate` feature lets a config directly construct Python objects (e.g. the optimizer):

    ```yaml
    optimizer:
      _target_: torch.optim.Adam
      lr: 1e-3
      betas: [0.9, 0.999]
    ```

    ```python
    optimizer = hydra.utils.instantiate(cfg.optimizer, params=model.parameters())
    ```

11. Best practice: split configs by concern — a `model_conf.yaml` for architecture hyperparameters, a
    `training_conf.yaml` for training-loop hyperparameters — rather than one monolithic file.

---

## Still to source for this module (no DTU equivalent — write from scratch)

* MLOps Maturity Model (5-level framework) — DTU's own version of this table lives in
  `s5_continuous_integration/cml.md` (see `week4_cicd_strategies.md`, Part 4) — reuse/adapt it here instead of
  duplicating, since it fits this module's opening topic well
* Detailed MLOps stages breakdown, Testing, Automation (CI/CD), Deployment, Monitoring as *stage* concepts (as
  opposed to the hands-on modules later in the course that teach *how*) — this module's job is the conceptual map,
  the later modules (4, 5, 7, 9) are the hands-on "how"
* Automated ML pipelines vs. CI/CD ML pipelines — distinction to define
* MLOps Architectures: Open Source tools (Kubeflow, MLflow, Metaflow, Kedro, ZenML, MLRun, CML) vs. Cloud Native
  tools (AWS/GCP/Azure) — comparative overview slide, cost-benefit framing
* Tool ecosystem list per stage + roles overview (ML Engineering vs. Operations) — a "who does what" / "what tool
  lives where" reference table, likely the best single visual to build for this module
