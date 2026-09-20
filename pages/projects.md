# Project work

Roughly a sixth of the course's total time (2 of 12 weeks) is dedicated project work, but the group
project itself is meant to run in parallel with the content weeks: every module's tooling gets applied
to the same running project as soon as it's covered, starting in Sprint A (Week 6).

The project serves as the basis for the course's final grading. Groups are free to choose their own
problem; the point is not to build the most impressive model but to demonstrate that the group can
apply the tools taught in this course to a real (if modest) end-to-end system.

## Group size

Groups of 2, per the [course information](../README.md#course-information).

## Assessment

Pass/Fail, based on a midterm, a final, and the project report, per the
[course information](../README.md#course-information).

## Getting started

1. **Brainstorm and scope the project.** Pick a problem, a dataset, and a rough idea of what model
   you'll use. Start small: it's better to ship a small, fully-instrumented pipeline than an ambitious
   model with none of the MLOps tooling wired up.
2. **Write a short project description** (what's the goal, what data, what model) and commit it to the
   project repository's `README.md`.
3. **Scaffold the repository** from a cookiecutter template using Module 2's project-structure and Git
   workflow (see Sprint A).

## Project checklist

This checklist is *exhaustive*: it lists everything that could be done across the whole curriculum.
Nobody is expected to check every box. The module tag in parentheses shows which module the item ties
to.

### Weeks 1-6 (Modules 1-5, Sprint A)

* [ ] Scaffold the project from a cookiecutter template (M2)
* [ ] Create a Git repository; all team members have write access (M2)
* [ ] Adopt a branching strategy (dev/feature/bugfix/release) (M2)
* [ ] Keep the dependency file in sync with what the code actually imports (M2)
* [ ] Comply with good coding practices (linting, formatting, typing) while developing (M2)
* [ ] Containerize the application with a Dockerfile (M3)
* [ ] Move hardcoded hyperparameters into a Hydra config file (M3)
* [ ] Set up logging and use a debugger/profiler on at least one slow or broken piece of code (M4)
* [ ] Set up CI running unit tests and linting on push (M5)
* [ ] Add pre-commit hooks (M5)

### Weeks 7-11 (Modules 6-10)

* [ ] Set up a Google Cloud project and claim any available credits (M6)
* [ ] Train the model on Google Cloud, and store data/artifacts in Cloud Storage (M6)
* [ ] Wrap the model in a FastAPI service and write at least one API test (M7)
* [ ] Deploy the service to Cloud Functions or Cloud Run (M7)
* [ ] Instrument the deployed application with monitoring and data drift detection (M8)
* [ ] Set up at least one alert for the monitored application (M8)
* [ ] (If relevant to the project) parallelize data loading, or scale training across multiple devices (M9)
* [ ] Track experiments and/or run a hyperparameter sweep using an experiment tracker (M10)
* [ ] Publish API documentation for the project (M10)

### Extra

* [ ] Write documentation for the application and publish it
* [ ] Revisit the initial project description: did the project turn out as planned?
* [ ] Create an architectural diagram of the MLOps pipeline
* [ ] Make sure all group members understand every part of the project

## Submission

The report template lives at `reports/README.md` in this repository (excluded from the built docs
site since it's a template to copy, not a page to publish). Copy it into the group project's own
repository and fill it out. *Deadline TBD once the semester dates are fixed.*
