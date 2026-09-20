# Project work

Roughly a sixth of the course's total time (2 of 12 weeks) is dedicated project work, but the group
project itself is meant to run in parallel with the content weeks: every module's tooling gets applied
to the same running project as soon as it's covered, starting in Sprint A (Week 6).

The project serves as the basis for the course's final grading. Groups are free to choose their own
problem; the point is not to build the most impressive model but to demonstrate that the group can
apply the tools taught in this course to a real (if modest) end-to-end system.

## Group size

*TBD: decide group size (DTU's comparable course uses 3–5 students per group).*

## Assessment

*TBD: decide whether assessment is the project report only (pass/fail), or report + presentation/exam.*

## Getting started

1. **Brainstorm and scope the project.** Pick a problem, a dataset, and a rough idea of what model
   you'll use. Start small: it's better to ship a small, fully-instrumented pipeline than an ambitious
   model with none of the MLOps tooling wired up.
2. **Write a short project description** (what's the goal, what data, what model) and commit it to the
   project repository's `README.md`.
3. **Scaffold the repository** using Module 3's Git workflow and a project template (see Sprint A).

## Project checklist

This checklist is *exhaustive*: it lists everything that could be done across the whole curriculum.
Nobody is expected to check every box. The module tag in parentheses shows which module the item ties
to.

### Weeks 1-6 (Modules 1-5, Sprint A)

* [ ] Create a Git repository; all team members have write access (M3)
* [ ] Adopt a branching strategy (dev/feature/bugfix/release) (M3)
* [ ] Scaffold the project from a template (cookiecutter or equivalent)
* [ ] Keep the dependency file in sync with what the code actually imports
* [ ] Comply with good coding practices (linting, formatting) while developing
* [ ] Set up CI running unit tests and linting on push (M4)
* [ ] Add pre-commit hooks
* [ ] Containerize the application with a Dockerfile (M5)
* [ ] Build and run the Docker image locally
* [ ] (If applicable) draft an initial Kubernetes/Compose setup (M5)

### Weeks 7-11 (Modules 6-10)

* [ ] Set up a feature store (online and/or offline) for the project's features (M6)
* [ ] Train/deploy a model end-to-end on at least one of AWS SageMaker, GCP Vertex AI, or Azure ML (M7)
* [ ] Create a CI/CD pipeline for the chosen cloud provider (M4/M7)
* [ ] (If relevant to the project) prototype an LLM-driven component and consider its LLMOps needs (M8)
* [ ] Instrument the deployed model/application with monitoring (M9)
* [ ] Set up at least one alert for the monitored application (M9)
* [ ] Track experiments and/or run a hyperparameter sweep using an experiment tracker (M10)

### Extra

* [ ] Write documentation for the application and publish it
* [ ] Revisit the initial project description: did the project turn out as planned?
* [ ] Create an architectural diagram of the MLOps pipeline
* [ ] Make sure all group members understand every part of the project

## Submission

The report template lives at `reports/README.md` in this repository (excluded from the built docs
site since it's a template to copy, not a page to publish). Copy it into the group project's own
repository and fill it out. *Deadline TBD once the semester dates are fixed.*
