# Introduction

Welcome to **Machine Learning Operations (MLOps)**! Everything for this course — lecture notes,
exercises, and further reading — lives in this repository. I won't pretend you'll walk out an MLOps
expert twelve weeks from now, but I will promise something more useful: you'll leave knowing the core
concepts and a working set of tools the field actually runs on. Think of this course as a toolbox that
fills up module by module — not one you master cover to cover, but one you know well enough to reach
into whenever a real project calls for it.

![MLOps lifecycle: nine stages, three disciplines, one loop](../figures/mlops_diagram.png)

This course is a toolbox. You will not become an expert in every tool presented here, but you will get
an overview of many of the tools that are used in MLOps, and you will be able to pick up new tools as
needed in the future.

## What is MLOps?

*Machine Learning Operations* (MLOps) is the set of practices, tools, and processes that take a machine
learning model from a one-off experiment to a robust, scalable, monitored system running in production.
It borrows heavily from DevOps (version control, CI/CD, containerization, infrastructure automation) and
extends those ideas to the parts of the ML lifecycle that are unique to machine learning: data
versioning, experiment tracking, model registries, data/model drift monitoring, and — increasingly —
the operational concerns specific to large language models and feature stores.

The lifecycle a production ML system moves through is usually described in three phases:

1. **Design** — understand the problem, the requirements, and what data is available or needs sourcing.
2. **Model development** — data analysis, model architecture, training, validation.
3. **Operations** — the automated pipeline that takes code changes into production safely, and the
   ongoing monitoring that confirms the deployed system keeps behaving as expected.

These three phases are a *cycle*, not a line — a deployed model is never "done." New requirements, new
data, and new failure modes send you back through design, development, and operations again. This
course focuses on Operations because that's the part most ML curricula skip entirely.

## How this course is organized

The course runs across 12 weeks: 10 content modules (one per week) covering the tools and practices of
modern MLOps, plus two dedicated project sprints (Week 6 and Week 12) for applying everything to your
own group project. See the [time plan](timeplan.md) for the full week-by-week breakdown and the
[projects page](projects.md) for how the group project and grading work.

Think of this course as a toolbox, not a certification. You will not leave as an expert in every single
tool covered — Docker, Kubernetes, three different cloud platforms, half a dozen MLOps frameworks. The
goal is that you leave knowing *what exists* and *when to reach for it*, so that when a real project
calls for one of these tools you know where to start.

## Prerequisites

To get the most out of this course, you should have prior experience with:

* General understanding of machine learning (datasets, probability, classifiers, overfitting,
  underfitting, etc.)
* Basic knowledge of deep learning (backpropagation, convolutional neural networks, autoencoders,
  etc.)
* Coding in PyTorch. On the first day, we provide some exercises in PyTorch to get everyone's skills
  up to date as fast as possible.
* Docker and command line basics
* At least 1 year of general programming experience

## Setup

Everything below is worth installing and setting up **before Week 1**, even though some of it (Docker,
`kubectl`, the cloud CLIs) isn't touched until later modules — the goal is to remove "I couldn't
install X" as a reason to fall behind once the course actually needs it.

### Languages used in this course

* **Python 3.11+** — the primary language for essentially every exercise: training scripts, APIs,
  pipeline definitions, and every cloud SDK (`boto3`, `google-cloud-aiplatform`, `azure-ai-ml`).
* **YAML** — configuration and pipeline definitions: GitHub Actions workflows (Module 4), Kubernetes
  manifests (Module 5), Azure Pipelines (Module 4), and this site's own `mkdocs.yml`.
* **Bash/shell** — every CLI command in every module, plus `Dockerfile` `RUN` steps and CI scripts.
* **Dockerfile syntax** (Module 5) and **HCL** (Terraform, Module 4, for infrastructure as code) — not
  full programming languages, but you'll read and write both.

You don't need to know all of these on day one — Python is the only one you should already be
comfortable with (see Prerequisites above). The rest are taught as they come up.

### Accounts to create

| Account | Needed from | Notes |
|---|---|---|
| **GitHub** | Module 3 | Free. Used for every module's exercises and the group project repo. |
| **Azure ([Azure for Students](https://azure.microsoft.com/en-us/free/students))** | Module 4, 7, 9 | No credit card required — verified with your academic email. $100 credit for 12 months plus 65+ always-free services, renewable every year you're still a student. This is the only cloud account this course requires; see the note below on why. |
| **Weights & Biases** | Module 10 | Free for personal/academic use. |

If you're signing up for Azure with a university-managed account, create your course
subscription under "no organization" where possible — organization-managed accounts sometimes block
creating the service-account keys/credentials you'll need later (e.g. for GitHub Actions to
authenticate to the cloud).

**Why Azure only, and not AWS/GCP too:** AWS's no-credit-card option (AWS Educate's Starter Account) is
a heavily restricted sandbox (one region, no IAM/billing dashboard, session timeouts), and GCP's
standard student credit still requires entering a card at signup. Azure for Students is the one option
that's genuinely free, uncapped-in-scope within its credit, and requires no card — so this course
standardizes on it for every cloud exercise. Module 4, 7, and 9 still *cover* AWS and GCP conceptually
(so you recognize the equivalent service on either), but every hands-on project in those modules should
be done on Azure.

### Tools to install locally

| Tool | Needed from | Install |
|---|---|---|
| **Python 3.11+** | Module 1 | [python.org/downloads](https://www.python.org/downloads/) or a version manager like `pyenv` |
| **uv** | Module 1 | [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) — this repo's dependency manager; `uv sync` installs everything in `pyproject.toml` |
| **Git** | Module 3 | [git-scm.com/downloads](https://git-scm.com/downloads/) |
| **A code editor** | Module 1 | [VS Code](https://code.visualstudio.com/) is recommended — this repo ships a `.devcontainer/`, so opening it in VS Code (or GitHub Codespaces) can set up Python + `uv` for you automatically |
| **Docker Desktop** (or OrbStack on macOS) | Module 5 | [docs.docker.com/get-docker](https://docs.docker.com/get-docker/) |
| **kubectl** | Module 5 | [kubernetes.io/docs/tasks/tools](https://kubernetes.io/docs/tasks/tools/) |
| **Minikube** | Module 5 | [minikube.sigs.k8s.io/docs/start](https://minikube.sigs.k8s.io/docs/start/) |
| **Azure CLI** (`az`) | Module 4, 7, 9 | [learn.microsoft.com/cli/azure/install-azure-cli](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) |

Once Python, `uv`, and Git are installed, clone the course repository and run:

```bash
git clone https://github.com/aligunesgit/MlOps.git
cd MlOps
uv sync
```

This installs every dependency listed in `pyproject.toml`, including the per-module exercise
dependencies (Feast, FastAPI, the cloud SDKs, Evidently, Optuna, W&B, and the rest) tracked under
`[dependency-groups.exercises]` — check that file if you want to see exactly which package a given
module's exercises will need.

## Prescribed books

The following books are suggested reading for the course:

* Emmanuel Ameisen — *Building Machine Learning Powered Applications: Going from Idea to Product*
  (O'Reilly)
* Todd M. Chen, Niall Richard Murphy, and Kasey Parisa — *Reliable Machine Learning: Applying SRE
  Principles to ML in Production* (O'Reilly)
* Ben Wilson — *Machine Learning Engineering in Action* (O'Reilly)
* Martin Kleppmann — *Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable,
  and Maintainable Systems* (O'Reilly)

None are required to follow the course, but each is a good deeper dive on a theme that recurs across
several modules: applied ML product-building, production reliability practices for ML, hands-on ML
engineering, and the distributed-systems foundations underneath most cloud MLOps tooling.
