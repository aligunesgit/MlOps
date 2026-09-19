# Reference material for Week 1 — Module 1: MLOps Introduction

> Source: [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) `pages/before.md`, Apache 2.0, copied in
> full/condensed. This is DTU's course-introduction page (not a numbered session module), but its core
> "what is MLOps + the 3-phase lifecycle" framing maps directly onto this course's Module 1 topics
> ("What is MLOps?", "MLOps Motivation", "Machine Learning Life Cycle"). The rest of Module 1's topic
> list (industrialisation challenges, DevOps/AIOps/ModelOps/LLMOps/FMOps/GitOps comparison, CI/CD case
> study) has no DTU equivalent — see "Still to source" below.

---

# Introduction to MLOps

*Machine Learning Operations* (MLOps) covers everything to do with managing the production ML lifecycle. It's the
compound of "machine learning" + "operations" — the structures and processes that take a model from "works once on
my laptop" to "a robust, scalable system many users can rely on."

!!! quote "Restaurant analogy (good one to open the first lecture with)"

    The difference between MLOps and doing ML without it is like the difference between cooking a meal for yourself
    at home versus running a restaurant. At home, you throw something together from whatever's in the fridge. A
    restaurant needs a well-defined process: sourcing ingredients, preparing food, serving customers, keeping
    everything running smoothly at scale. MLOps is building the "restaurant" for machine learning models.

## The three-phase ML lifecycle

1. **Design** — investigate the problem, prioritize requirements for what the model needs to do, investigate what
    data exists or needs to be sourced.

2. **Model development** — data analysis (is the model learning the right signal?), the ML engineering phase
    (choosing model architecture), validation/testing (does it generalize?).

3. **Operations** — build the automated pipeline that incorporates codebase changes into the model without slowing
    down production, and continuously **monitor** already-deployed models to confirm they keep behaving as
    specified.

**Critical framing**: these three phases form a *cycle*, not a pipeline with an end state. Deploying successfully
isn't "done" — requirements change (back to Design), new algorithms emerge (back to Model development), cost
pressure mounts (back to Operations, optimizing what's already running).

**This course (like DTU's) is specifically about the Operations phase** — the part of the lifecycle that most
data scientists' existing toolbox (data processing, model development skills) doesn't cover, and the actual gap
this course exists to fill.

## Course framing: "a toolbox, not a certification"

Worth setting this expectation explicitly on day one: the point of the course isn't to make every student an
expert in every tool covered — it's to fill their toolbox with enough breadth that they can *recognize* which tool
fits a given future problem, then go deep on that one tool as needed. Nobody leaves this course an expert in
Docker AND Kubernetes AND Terraform AND every cloud provider AND every experiment tracker — that's not the goal.

## Core vs. optional modules (a DTU convention worth adopting)

DTU visually marks certain modules "Core Module" vs. leaving others unmarked (optional/supplementary) — core
modules are required to pass the course, optional ones are recommended but not gating. Worth deciding early in this
course's own design which of the 10 modules (or sub-bullets within them) are "core" vs. "if time allows," especially
given several DTU source modules used as reference here (`s10_extra/*`) are themselves explicitly unfinished drafts
on DTU's side — a signal that even DTU treats that content as lower-priority/optional.

## Recommended local folder structure (adapt DTU's convention)

DTU recommends students keep the course repo, their cookiecutter template project, ad-hoc exercise folders, and
their exam project as **separate git repos with separate virtual environments**, to avoid dependency conflicts:

```txt
<course-folder>/
    ├── <this-course-repo>/       # this repo, cloned
    ├── <template-project>/       # cookiecutter-scaffolded running project (see sprint_a_project.md)
    ├── exercises/                 # one-off exercise folders, one git repo, per-module subfolders
    └── <exam-project>/            # the actual group project repo (see sprint_b_final_project.md)
```

Worth adapting and including in this course's own Module 1 "getting started" page — it's a small thing that
prevents a lot of early-course confusion about "which venv am I even in right now."

## Communication channel

DTU runs a course Slack with a `#general` channel plus one channel per session (`#s1`, `#s2`, ...) — a pattern
worth reusing regardless of platform (Slack/Discord/Teams), since "ask in the channel for this week's topic" scales
much better than DMs once the course population grows.

---

## Still to source for this module (no DTU equivalent — write from scratch)

* State of machine learning / ML industrialisation challenges / AI industrialization challenges — general framing,
  likely drawing on the same reference material already in this repo's `literature/` folder equivalent (Hidden
  Technical Debt in ML Systems paper, the Interview Study on Operationalizing ML — both cited in DTU's own root
  README as recommended reading, worth carrying over as recommended reading here too)
* "MLOps challenges similar to DevOps" — direct DevOps/MLOps comparison
* MLOps Components — likely overlaps with Module 2's "Detailed MLOps and stages" (see `week2_ml_mlops_stages.md`) —
  worth deciding the division of labor between Module 1 and Module 2 explicitly so the two don't duplicate content
* How MLOps relates to DevOps, AIOps, ModelOps, LLMOps, FMOps, and GitOps — a comparison table, likely the single
  most useful diagram for this module; LLMOps specifically gets its own full module later (Module 8, see
  `week9...` — not yet written, no DTU source at all for LLMOps)
* "Major Phases — what it takes to master MLOps" — likely this course's own synthesis/summary slide
* CI/CD in Production Case Study — a real (or realistic) worked example; DTU has nothing like this in their intro
  material, would need to be sourced from elsewhere (industry case study writeups, e.g. Google's MLOps continuous
  delivery paper already cited in this course's earlier planning conversation)
