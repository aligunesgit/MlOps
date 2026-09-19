# Supplementary — Orchestration, MLOps design, HPC, and course-admin precedents from DTU

> Source: [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) `s10_extra/orchestration.md`,
> `s10_extra/design.md`, `s10_extra/high_performance_clusters.md`, `pages/overview.md`, `pages/faq.md`
> (Apache 2.0). The first two are explicitly unfinished stubs on DTU's side; HPC content is DTU-specific
> (their own university cluster) but structurally reusable; `overview.md`'s tool-stack table and
> `faq.md`'s course-admin answers are useful precedents for this course's own still-open decisions
> (see `CURRICULUM_DRAFT.md`'s Course Info table).

---

## Part 1 — Workflow orchestration (`orchestration.md`) — skeleton only

> `!!! danger "Module is still under development"` on DTU's side. Genuinely just a pitch + install step.

# Workflow orchestration

The pitch for orchestration tools (DTU frames it as "things an MLOps engineer gets asked for"): set up a training
pipeline → add logging → run it daily → retry on failure → notify on success → visualize dependencies → add
caching → let non-coding collaborators trigger it via a UI.

```bash
pip install prefect   # or: uv add prefect
prefect server start
```

DTU's draft stops immediately after this — no actual worked example. **This is a genuine gap in DTU's material**
relative to what this course's own Module 2 topic list implies ("Automated ML pipelines vs CI/CD ML pipelines" —
see `week2_ml_mlops_stages.md`) — if this course wants a real orchestration exercise (Prefect, or an alternative
like Airflow/Dagster/Kedro), it needs to be built from scratch; there's no DTU exercise to adapt.

## Part 2 — Designing MLOps pipelines (`design.md`) — skeleton only

> Also flagged `!!! danger "Module is still under development"` — one quote, one book recommendation, one
> unlabeled image reference, nothing else.

Opens with: *"Machine learning engineering is 10% machine learning and 90% engineering."* — Chip Huyen, whose book
*Designing Machine Learning Systems: An Iterative Process for Production-Ready Applications* DTU recommends as
required-adjacent reading for this topic. The rest of the file is an unfinished pointer toward a "tool landscape"
diagram and "visualizing the design" section that never got written.

Worth noting: this course's Module 2 already has strong overlap with what this stub was clearly *trying* to be
(MLOps architectures, tool ecosystem, roles — see `week2_ml_mlops_stages.md`'s "Still to source" list) — likely
not worth treating as a separate module, just a citation (the Chip Huyen book) to fold into Module 2's reading list.

---

## Part 3 — High Performance Clusters (`high_performance_clusters.md`)

Positions HPC as the alternative to cloud compute when cost matters more than infinite scale — most university
students already have institutional HPC access (DTU points at EuroHPC as the EU-wide public alternative for anyone
without institutional access).

**Tiering** (Europe-specific but the concept generalizes): Tier-0 = petaflop-scale national/European centers,
Tier-1 = national supercomputing centers, Tier-2 = regional centers — lower tier number = bigger jobs supported.

**Architecture**: two broad shapes — a true supercomputer (front-end login node + backend compute/GPU/RAM/storage
modules, all network-linked) vs. a Load Sharing Facility / LSF (a network of independent machines, each with its
own full CPU/GPU/RAM). Rule of thumb: LSF is fine for single-node jobs; a real supercomputer matters once a job
needs many devices communicating with each other (i.e., matches the DDP content in
`supplementary/scalable_applications.md`).

**Scheduler** is the actual software layer that matters day-to-day — without one, a shared cluster is just
resource contention chaos. Major schedulers: SLURM, MOAB HPC Suite, PBS Works (DTU's own cluster uses PBS/LSF-style
`bsub`/`qstat`/`bstat` commands).

Typical exercise flow (DTU's own, adaptable to any institution's HPC): SSH/ThinLinc into the cluster → set up
`(mini)conda` for a dependency environment → write a job submission bash script specifying the queue, resource
request (GPU count), and the actual command to run → `module load cuda/X.Y` to pull in the right CUDA version →
submit with `bsub < jobscript.sh` → poll status with `bstat`/`qstat` → inspect the `.out`/`.err` output files.

**Relevance to this course**: worth a single slide/pointer rather than a full module — the concept ("HPC as a
cost-effective compute alternative to the cloud, gated by institutional access") is more important than any
specific scheduler's command syntax, especially since this course leans cloud-first (AWS/Azure/GCP) rather than
DTU's cloud-vs-HPC dual framing.

---

## Part 4 — Course tool-stack overview (`pages/overview.md`)

DTU's own "summary of everything" page is a single table mapping each tool taught in the course to a one-line role
description (PyTorch → computational engine, Lightning → high-level training interface, uv/Conda → dependency
management, Hydra → config management, Typer → CLI, W&B → experiment tracking, profiler/debugger → performance/bug
tooling, Cookiecutter → project templating, Docker → containerization, DVC → data versioning, Git → code
versioning, Pytest → testing, Ruff → linting, GitHub Actions → CI, Cloud Build → image build automation, Artifact
Registry → image storage, Cloud Storage → data/model storage, Compute Engine → general compute, Vertex AI →
managed training, FastAPI → serving API, ONNX → portable model format, Streamlit → frontend, Cloud Functions/Run →
deployment targets, Locust → load testing, Cloud Monitoring/Evidently/OpenTelemetry → observability).

**Directly actionable for this course**: build the equivalent single-page tool-map once all 10 modules' content is
finalized — it's the single highest-value "how does everything fit together" artifact for students, and every tool
in it should trace back to a specific module (this course's own version would additionally need rows for AWS/Azure
tools, Feast, LLMOps tooling, and the AutoML platforms — none of which are in DTU's table since DTU doesn't teach
them).

---

## Part 5 — Course-admin precedents from the FAQ (`pages/faq.md`)

Directly relevant to this course's own still-open decisions (see `CURRICULUM_DRAFT.md` Course Info table):

* **Group size**: DTU uses 3–5 students per project group, explicitly sized so the project is "intentionally too
  big for one person" but still parallelizable.
* **Assessment**: DTU's exam is the project report only (as of their 2025+ policy) — no separate written/oral exam
  for most students. Exception: non-DTU foreign students needing a numeric grade (rather than pass/fail) get an
  additional short oral exam specifically to validate their individually contributed work.
* **Generative AI policy**: explicitly permitted for exercises, project code, and even the report itself — but
  students are asked to write report answers in their own words since the report is meant to describe *their own*
  work process, not an AI's summary of it. Quote worth keeping verbatim for this course's own academic-integrity
  section: *"The I in LLM stands for intelligence."*
* **Prerequisites framing**: DTU recommends (not requires) prior deep learning + PyTorch exposure, and explicitly
  builds a PyTorch refresher into the very first module to level the class — directly consistent with this course's
  own "no prerequisites required" decision (see `week1_mlops_introduction.md`), just worth deciding whether this
  course's Module 1 should carry the same kind of PyTorch-refresher safety net DTU's Module 1 (Development
  Environment) does, since this course's own Module 1 topic list doesn't currently include one.
* **Attendance/online policy** and **remote/PhD-student access rules** — DTU-specific administrative content, not
  worth porting unless this course has a similar remote-attendance or cross-institution enrollment situation.
