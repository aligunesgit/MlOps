# 1413211011 — MLOps and AI Systems Engineering
### 12-Week Curriculum Draft (own module list, DTU-inspired repo/format)

> Status: DRAFT for review. All content modules have been provided by the instructor and are final
> (10 modules, renumbered 1–10 in teaching order, no gaps). 2 Project Sprint weeks are inserted
> between them, for a **12-week total**. The **repository structure and tooling conventions** (mkdocs
> site, one folder per week, CI workflows, project checklist model, report template) are still
> adapted from [SkafteNicki/dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) (DTU course 02476) —
> only the *content topics* are this course's own.

---

## Course Info

| | |
|---|---|
| Course code | 1413211011 |
| Course name | MLOps and AI Systems Engineering |
| Duration | 12 weeks (semester) — 10 content modules + 2 Project Sprint weeks |
| Prerequisites | None required |
| Assessment | TBD — DTU uses project report only (pass/fail). Needs a decision: report only, or report + exam/presentation + individual component? |
| ECTS / credit weight | TBD — not specified yet |
| Group size | TBD — DTU uses 3–5 students per project group |

**Open decisions flagged above (ECTS, exact assessment breakdown, group size) — fill in before finalizing.**

---

## Learning Objectives

* Understand MLOps fundamentals and how it relates to DevOps/AIOps/ModelOps/LLMOps/FMOps/GitOps
* Master Git and CI/CD across GitHub Actions, AWS, Azure and GCP
* Containerize and orchestrate ML workloads with Docker and Kubernetes
* Use feature stores for online/offline feature management
* Build and deploy end-to-end ML pipelines on AWS SageMaker, GCP Vertex AI and Azure ML
* Understand LLMOps: operationalizing generative AI / foundation models
* Monitor deployed models and infrastructure across the major clouds
* Get oriented in the AutoML / MLOps platform tooling ecosystem
* Apply all of the above to a self-directed group project, end-to-end

---

## Weekly Breakdown

| Week | Module | Topic |
|------|--------|-------|
| 1  | Module 1  | MLOps Introduction |
| 2  | Module 2  | Overview of ML and MLOps Stages |
| 3  | Module 3  | Git Essentials for MLOps Practitioners |
| 4  | Module 4  | CI/CD Strategies for AWS, Azure, GCP, and GitHub Actions |
| 5  | Module 5  | Docker & Kubernetes Overview |
| 6  | —         | **Project Sprint A** — apply Modules 1–5 to the group project (repo setup, Git workflow, CI/CD pipeline, containerize) |
| 7  | Module 6  | Feature Store |
| 8  | Module 7  | Deep Dive into MLOps Cloud Services (AWS SageMaker, GCP Vertex AI, Azure ML) |
| 9  | Module 8  | MLOps for LLMs (LLMOps) |
| 10 | Module 9  | Understanding Model Monitoring (AWS, Azure & GCP) |
| 11 | Module 10 | Introduction to AutoML Tools |
| 12 | —         | **Project Sprint B (final)** — integration, monitoring hookup, report + submission |

*Sprint placement rationale: Sprint A sits right after the foundational/DevOps block (Intro → Stages
→ Git → CI/CD → Docker/K8s) so groups have a working, containerized, CI-wired repo before moving into
the more specialized cloud/LLMOps/monitoring/AutoML modules. Sprint B is the final integration +
submission week. Say the word if you'd rather move either sprint.*

*(Exact calendar dates intentionally left out — fill in once the semester start date is fixed.)*

---

## Module Details

### Module 1 — MLOps Introduction

* What is MLOps?
* State of machine learning
* Machine learning industrialisation challenges
* AI Industrialization Challenges
* MLOps Motivation: High-level view
* MLOps challenges
* MLOps challenges similar to DevOps
* MLOps Components
* Machine Learning Life Cycle
* How does it relate to DevOps, AIOps, ModelOps, LLMOps, FMOps, and GitOps?
* Major Phases — what it takes to master MLOps
* CI/CD in Production Case Study

### Module 2 — Overview of ML and MLOps Stages

* MLOps Maturity Model
* Detailed MLOps and stages
* Versioning: Data, Code, Model, Features & Containers
* Testing
* Automation (CI/CD)
* Reproducibility
* Deployment
* Monitoring
* Automated ML pipelines vs CI/CD ML pipelines
* MLOps Architectures
* Architectures — Open Source tools: Kubeflow, MLflow, Metaflow, Kedro, ZenML, MLRun, CML
* Architectures — Cloud Native tools: AWS, GCP and Azure
* The cost-benefit approach of each architecture and MLOps maturity
* List of tools involved in each stage (MLOps tool ecosystem)
* Different roles involved in MLOps (ML Engineering + Operations)

### Module 3 — Git Essentials for MLOps Practitioners

* Overview of Git
* Understanding branching strategies and repo
* Standard Git branching strategies (development, feature, bug, release, UAT)
* Practising important Git commands
* GitHub Actions overview and working
* GitHub remote repository
* Project: Mastering Git — Commands, Branching, and Collaboration

### Module 4 — CI/CD Strategies for AWS, Azure, GCP, and GitHub Actions

* Introduction to CI and CD
* CI/CD challenges in Machine Learning
* Steps involved in CI/CD implementation in the ML lifecycle and workflow
* A glimpse of popular tools used in the DevOps ecosystem on the cloud

**AWS DevOps**
* AWS CodePipeline
* AWS CodeBuild
* AWS CodeDeploy
* AWS CodeCommit
* Project: AWS DevOps Pipeline

**GCP DevOps**
* Cloud Run
* Cloud Build
* Cloud Deploy
* Artifact Registry
* Cloud Source Repositories
* Project: GCP DevOps Pipeline

**Azure DevOps**
* Azure Boards
* Azure Repos
* Azure Pipelines
* Azure Test Plans
* Azure Artifacts
* Infrastructure as Code (IaC) with Azure DevOps
* YAML pipeline structure
* Project: Azure DevOps Pipeline

**GitHub Actions**
* Introduction to GitHub Actions
* GitHub Actions YAML pipeline structure
* GitHub Actions automation & custom workflows
* GitHub Pages
* Project: GitHub Actions DevOps Pipeline

### Module 5 — Docker & Kubernetes Overview

**Docker Foundation**
* Installing Docker on Windows, macOS & Linux
* Managing containers with Docker commands
* How does it work? Docker registry — Docker Hub
* Building your own Docker images
* Docker network types
* Docker volumes
* Docker Compose
* Docker Swarm
* Project: Deploy a Node.js app in a Docker container
* Project: Deploy an ML model in a Docker container
* Project: Deploy a complete end-to-end ML model with Docker Compose

**Kubernetes Overview**
* Kubernetes architecture
* Worker nodes
* Control plane
* Virtual network
* API server
* Command line tool — `kubectl`

**Kubernetes Resources**
* Pod
* ConfigMap
* Service
* Secret
* Ingress
* Deployment
* StatefulSet
* DaemonSet
* Volumes (PVC)
* Minikube
* Project: Deploy an ML model in a Kubernetes cluster

### Module 6 — Feature Store

* Introduction to Feature Stores: SageMaker Feature Store, Vertex AI Feature Store, Databricks, Tecton, Feast, Hopsworks, etc.
* Feast — open source feature store
* Feature store: online vs. offline
* Project: Deploy Feast online/offline feature store
* Online & offline feature store options
* Feast feature store on the cloud
* Monitor features programmatically
* Visualizing feature drift over time

### Module 7 — Deep Dive into MLOps Cloud Services (AWS, Azure & GCP)

**AWS SageMaker**
* Introduction to Amazon SageMaker
* Using Amazon S3 along with SageMaker
* Amazon SageMaker notebooks
* Notebook instance type, IAM role & VPC
* Build, train & deploy an ML model using SageMaker
* Endpoint & endpoint configurations
* Generate inference from a deployed model
* AWS SageMaker Pipelines
* SageMaker Studio & SageMaker domain
* SageMaker Projects
* Repositories
* Pipelines & graphs
* Experiments
* Model groups
* Endpoints
* Project: Deploy an end-to-end MLOps pipeline using SageMaker Studio

**GCP Vertex AI**
* Introduction to Vertex AI
* Gather, import & label datasets
* Build, train & deploy ML solutions
* Manage your models with confidence
* Using pipelines throughout your ML workflow
* Adapting to changes in data
* Creating models with Vertex AI and deploying ML models using `aiplatform` pipelines
* Project: Deploy an end-to-end MLOps pipeline using Vertex AI

**Azure MLOps**
* Azure Machine Learning Studio
* Azure MLOps
* Azure ML components
* Azure MLOps + DevOps
* Fully automated end-to-end CI/CD ML pipelines
* Project: Deploy an end-to-end MLOps v2 pipeline using Azure Machine Learning

### Module 8 — MLOps for LLMs (LLMOps)

* What is an LLM?
* MLOps for LLMs
* FMOps/LLMOps: operationalize generative AI
* LLM system design
* High-level view of an LLM-driven application
* LLMOps pipeline

### Module 9 — Understanding Model Monitoring (AWS, Azure & GCP)

* Importance of model monitoring
* Various types of monitoring related to the model
* The architecture of the monitoring ecosystem in AWS/Azure/GCP
* AWS model monitoring
* Azure model monitoring
* GCP model monitoring
* Optimize and manage models at the edge
* Common issues in ML model deployment
* Feedback loop role
* Project: Model & infrastructure monitoring using cloud tools

### Module 10 — Introduction to AutoML Tools

* H2O MLOps
* Valohai
* Domino Data Lab
* neptune.ai
* Iguazio
* Weights & Biases (W&B)

---

## Repository Structure (planned — DTU layout pattern, this course's own modules)

```
MlOps/
├── README.md                              course landing page
├── mkdocs.yml                             site nav (Material for MkDocs)
├── pages/                                 before.md, timeplan.md, projects.md, faq.md, overview.md
├── m1_mlops_introduction/                 README.md + module content + exercise_files/
├── m2_ml_and_mlops_stages/
├── m3_git_essentials/
├── m4_cicd_strategies/
├── m5_docker_and_kubernetes/
├── sprint_a_project/                      Project Sprint A guidance + checklist
├── m6_feature_store/
├── m7_cloud_mlops_deep_dive/
├── m8_llmops/
├── m9_model_monitoring/
├── m10_automl_tools/
├── sprint_b_final_project/                Project Sprint B guidance + checklist + submission info
├── figures/                               shared images/icons
├── slides/                                one PDF per lecture
├── literature/                            supporting papers
├── canvas/                                MLOps canvas (project design template)
├── reports/                                project report template + report.py validator
├── tools/                                 course-management scripts (grading, repo scraping)
├── .github/workflows/                     docs build+deploy, pre-commit update, link-check, formatting
├── .devcontainer/                         Codespaces support
├── tasks.py                               invoke tasks (install, docs, lint, deploy)
└── pyproject.toml                         deps (mkdocs stack + exercises group)
```

Content will be in **English**. Folder-per-week naming follows `mN_slug/` (module) or
`sprint_x_*` (project sprint), each with its own `README.md`, following the same mkdocs conventions
DTU uses (admonitions, `--8<--` code-snippet includes, content tabs — see DTU's `AGENTS.md` for the
exact syntax we'll replicate).

---

## Reference Material Index

Full/condensed source content pulled from [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) (Apache 2.0),
organized by which week/module it's raw material for. Located in `reference/`. Use these as source material when
actually writing each module's lesson page — none of this is finished, publishable content yet, it's the research
layer underneath the curriculum.

| File | Maps to | Source DTU pages |
|---|---|---|
| `reference/week1_mlops_introduction.md` | Module 1 | `pages/before.md` |
| `reference/week2_ml_mlops_stages.md` | Module 2 | `s2.../dvc.md`, `s3.../config_files.md` |
| `reference/week3_git_essentials.md` | Module 3 | `s2.../git.md` |
| `reference/week4_cicd_strategies.md` | Module 4 | `s5_continuous_integration/*.md`, `s10_extra/infrastructure_as_code.md` |
| `reference/week5_docker_kubernetes.md` | Module 5 | `s3.../docker.md`, `s10_extra/kubernetes.md` |
| `reference/sprint_a_project.md` | Sprint A (Week 6) | `s2.../code_structure.md` |
| `reference/week8_cloud_deep_dive.md` + `week8_deployment_fastapi_onnx.md` | Module 7 | `s6_the_cloud/*.md`, `s7_deployment/*.md` |
| `reference/week10_model_monitoring.md` | Module 9 | `s8_monitoring/*.md`, `s10_extra/{quantization,calibration}.md` |
| `reference/week11_automl_tools.md` | Module 10 | `s4.../logging.md` (W&B half), `s10_extra/hyperparameters.md` |
| `reference/sprint_b_final_project.md` | Sprint B (Week 12) | `reports/README.md`, `s10_extra/documentation.md` |
| `reference/supplementary/dev_tools_cli_and_style.md` | *(enrichment, unmapped)* | `s2.../cli.md`, `good_coding_practice.md` |
| `reference/supplementary/debugging_profiling_boilerplate.md` | *(enrichment, unmapped)* | `s4.../{debugging,profiling,boilerplate}.md` |
| `reference/supplementary/scalable_applications.md` | *(enrichment, unmapped)* | `s9_scalable_applications/*.md` |
| `reference/supplementary/misc_stubs_and_course_admin.md` | *(enrichment, unmapped)* | `s10_extra/{orchestration,design,high_performance_clusters}.md`, `pages/{overview,faq}.md` |

**No content sourced for**: Module 6 (Feature Store), Module 8 (LLMOps) — DTU has zero coverage of either topic;
these two modules need to be written entirely from scratch, no DTU reference material exists to draw on.

**Intentionally not pulled**: `s1_development_environment/*.md` (terminal/conda/editor/PyTorch-refresher basics) —
generic dev-environment setup content with low novelty value for this course's own Module 1, which doesn't cover
that ground the same way DTU's does. Say the word if you want it pulled in anyway (e.g. if this course decides its
own Module 1 *should* include a PyTorch refresher — see the note on this in `misc_stubs_and_course_admin.md`, Part 5).

## Next steps (pending your review)

1. Confirm the Sprint A (Week 6) / Sprint B (Week 12) placement, or move them.
2. Resolve the open decisions: ECTS/credit weight, assessment breakdown (report only vs. report +
   presentation/exam), group size. DTU's own precedents (3–5 per group, report-only pass/fail assessment) are
   documented in `reference/supplementary/misc_stubs_and_course_admin.md`, Part 5, as a starting reference.
3. Decide what to do about Module 6 (Feature Store) and Module 8 (LLMOps) — zero DTU source material exists for
   either, so these need original content from the start rather than adapted DTU material.
4. Once confirmed, scaffold the full repo structure (mkdocs.yml, module folders, CI workflows,
   devcontainer, tasks.py) mirroring DTU's tooling, with each module's `README.md` populated from
   the bullet lists above plus the corresponding `reference/` file.
5. Decide content authorship approach for turning each module's bullet list into full lesson pages:
   I draft and you review, or you draft and I polish/format into mkdocs conventions.
