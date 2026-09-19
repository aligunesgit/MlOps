# Module 1 — MLOps Introduction

Week 1

## Learning objectives

* Understand what MLOps is and why it exists
* Understand the state of machine learning and the industrialisation challenges it faces
* Understand the machine learning life cycle
* Be able to place MLOps in relation to DevOps, AIOps, ModelOps, LLMOps, FMOps, and GitOps

---

## 1. What is MLOps?

**MLOps (Machine Learning Operations)** is the set of practices, culture, and tooling that lets a
team build, deploy, monitor, and continuously improve machine learning models as a reliable part of a
production system — rather than as a one-off artifact that lives in a notebook.

A useful way to think about it: training a model is like cooking a great dish once in your own
kitchen. Getting that model into production, keeping it running correctly for thousands of users, and
knowing the moment it starts producing bad predictions — that's like running a restaurant. The recipe
(the model) is necessary but nowhere near sufficient. You need supply chains for ingredients (data
pipelines), a kitchen that scales under load (infrastructure), staff trained to a consistent standard
(reproducible processes), and a way to know a dish went out wrong before the customer complains
(monitoring). MLOps is the discipline of building that "restaurant" around a model.

Concretely, MLOps borrows the automation and discipline of DevOps — version control, continuous
integration and delivery, infrastructure as code — and extends it to solve problems that are unique to
machine learning:

* **Data changes the behavior of the system**, not just the code. Two deployments with identical code
  can behave completely differently if the underlying data distribution shifted.
* **Models decay silently.** Software that isn't touched keeps working. A model that isn't touched
  quietly gets worse as the world it was trained on drifts away from the world it now sees.
* **Reproducibility is multidimensional.** Reproducing a result requires pinning code, data, model
  weights, hyperparameters, and the training environment simultaneously — any one of them changing can
  change the outcome.
* **The artifact is probabilistic, not deterministic.** You can't write a unit test that simply asserts
  "correct output" the way you can for a sorting function; you need statistical tests, drift
  detection, and human judgment about acceptable performance.

## 2. The state of machine learning

Machine learning has moved from a research activity practiced by a small number of specialists to a
default component of most software products. Deep learning in particular has gone from a niche
technique to the backbone of computer vision, natural language processing, recommendation systems, and
— most recently — large-scale generative and foundation models that power conversational assistants,
code generation, and content creation at a scale that didn't exist a few years ago.

This growth has outpaced the maturity of the tooling and practices needed to run these systems safely
and cost-effectively in production. Industry surveys over the last several years have repeatedly found
that a large majority of ML projects that start never reach production at all, and of the ones that do,
many fail to deliver sustained value because nobody built the operational muscle to keep them healthy.
Model training gets almost all of the attention in ML education; keeping a model alive, correct, and
cost-effective for the following two years gets almost none. That gap is precisely what this course
exists to close.

## 3. Machine learning industrialisation challenges

Moving from a prototype to an industrial-grade ML system surfaces challenges that a data science
notebook simply doesn't expose:

* **Data engineering at scale** — pipelines that reliably collect, clean, label, and version data,
  often from multiple upstream systems that were never designed with ML in mind.
* **Reproducibility** — being able to recreate a specific model's exact training conditions months
  later, for debugging, auditing, or compliance.
* **Testing a probabilistic system** — validating not just "does the code run" but "is the model's
  behavior still acceptable," which requires statistical thinking, not just assertions.
* **Serving at scale and within latency budgets** — a model that takes 30 seconds to run in a notebook
  may need to respond in 30 milliseconds in production.
* **Organizational silos** — data scientists, ML engineers, platform/DevOps teams, and business
  stakeholders often work with different tools, different vocabularies, and different incentives.
* **Governance and risk** — explainability, fairness, and compliance requirements that barely exist in
  a research setting become hard constraints in a regulated production one.

## 4. AI industrialization challenges

Zooming out from ML specifically to AI systems broadly, the same industrialisation problem shows up at
a larger scale: organizations need standardized platforms (rather than one-off pipelines built by every
team from scratch), a workforce that spans data science, ML/platform engineering, and increasingly
prompt/LLM engineering, and governance frameworks that can keep pace with systems whose behavior is
harder to fully specify in advance than traditional software. The rise of generative AI and foundation
models has intensified this: teams that had barely industrialized "classic" ML are now also expected to
operationalize LLM-based systems, which carry their own cost, latency, and evaluation challenges (a
theme this course returns to directly in Module 8, LLMOps).

## 5. MLOps motivation: high-level view

Put simply, MLOps exists because **training a good model is not the same as running a good ML
system.** The motivation for adopting MLOps practices comes down to a small number of recurring
business pressures:

* **Speed** — reducing the time from "we have an idea" to "it's safely serving real users."
* **Reliability** — making sure a deployed model keeps behaving the way it did when it was validated.
* **Scale** — supporting many models, many teams, and many environments without each one reinventing
  its own ad-hoc process.
* **Cost** — avoiding wasted compute, redundant infrastructure, and the very expensive failure mode of
  a silently degrading model nobody notices until a business metric drops.
* **Trust and governance** — being able to explain, audit, and roll back model behavior when it matters
  most — regulators, customers, or leadership asking "why did the model do that?"

## 6. MLOps challenges

Adopting MLOps is not just "buy some tools." The practical obstacles teams run into again and again
include:

* Fragmented tooling across the data → training → deployment → monitoring pipeline, often owned by
  different teams with little shared context.
* A shortage of people who are fluent in *both* the ML side and the production-engineering side.
* Cultural resistance — data science teams optimizing for model accuracy in isolation, without
  ownership of what happens after a model ships.
* Monitoring blind spots — most organizations instrument their infrastructure (CPU, memory, latency)
  far more thoroughly than they instrument the *statistical health* of their models (drift, skew,
  fairness).
* Cost sprawl — GPUs, managed cloud ML services, and duplicated environments across teams add up
  quickly without centralized visibility.

## 7. MLOps challenges similar to DevOps

Many of MLOps' hardest problems are not new — they're the same problems DevOps solved for traditional
software, just harder:

| DevOps problem | MLOps equivalent, and why it's harder |
|---|---|
| Version control for code | Version control for code **and** data **and** models **and** hyperparameters, which are much larger and change independently |
| CI (does the code work?) | CI **and** CT — continuous *training* (does the model still learn something good on current data?) |
| CD (ship the new binary) | CD **and** continuous *evaluation* (a new model version needs a quality gate, not just "it compiles") |
| Infrastructure monitoring | Infrastructure monitoring **and** model/data monitoring (drift, skew, fairness — signals that have no equivalent in traditional software) |
| Rollback a bad deploy | Rollback a bad deploy **and** detect a model that is technically running fine but has quietly become wrong |

This is why MLOps is often described as "DevOps plus the parts of the lifecycle that are unique to
data and models" rather than a wholesale replacement for DevOps thinking.

## 8. MLOps components

A working MLOps setup is made up of a small number of recurring building blocks, most of which get
their own dedicated module later in this course:

* **Version control** for code, data, and models (Module 3)
* **CI/CD pipelines** that build, test, and deploy automatically (Module 4)
* **Containerization and orchestration** for reproducible, scalable execution (Module 5)
* **Feature management** so training and serving use consistent, versioned features (Module 6)
* **Managed training/serving infrastructure** on one or more cloud platforms (Module 7)
* **Model-specific operational concerns for LLMs and generative AI** (Module 8)
* **Monitoring and observability** for both infrastructure and model behavior (Module 9)
* **Experiment tracking and hyperparameter optimization** (Module 10)

Seeing the whole map now is the point of this module — every later module is a deep dive into one of
these boxes.

## 9. The machine learning life cycle

A production ML system moves through three broad phases, and — critically — moves through them
repeatedly, not once:

1. **Design** — understand the problem, define success metrics, and figure out what data exists or
   needs to be sourced. Getting this phase wrong (solving the wrong problem, or on the wrong data)
   dooms everything downstream, no matter how good the engineering is later.
2. **Model development** — exploratory data analysis, feature engineering, model selection, training,
   and offline validation against held-out data.
3. **Operations** — packaging, deploying, and — the phase most ML curricula skip — continuously
   monitoring the deployed model, detecting when it degrades, and feeding that signal back into the
   next iteration of design and development.

<figure markdown>
The three phases form a loop, not a line: production monitoring signals (drift, failures, new labeled
data) are exactly what triggers the next round of model development, which may in turn surface new
requirements that send the team back to the design phase.
</figure>

This course is deliberately weighted toward phase 3 — Operations — because that is the phase most
people arrive at this course *without* a toolbox for.

## 10. How MLOps relates to DevOps, AIOps, ModelOps, LLMOps, FMOps, and GitOps

These terms overlap heavily and the industry is not fully consistent about their boundaries, but a
useful working distinction is:

| Term | Primary focus |
|---|---|
| **DevOps** | Software delivery in general — CI/CD, infrastructure automation, culture of shared ownership between development and operations |
| **MLOps** | DevOps principles extended to the ML-specific lifecycle: data versioning, experiment tracking, model training pipelines, model deployment, and model monitoring |
| **AIOps** | Using AI/ML *to run IT operations* — anomaly detection, automated incident response, log analysis. (Note the direction is reversed from MLOps: AIOps uses ML to operate systems; MLOps operates ML systems.) |
| **ModelOps** | Often used interchangeably with MLOps, but sometimes scoped narrower — specifically governance, versioning, and lifecycle management of models already in production, less focused on the training side |
| **LLMOps** | MLOps specialized for large language models: prompt/version management, retrieval pipelines, evaluation of open-ended text output, cost and latency management at inference time (covered in depth in Module 8) |
| **FMOps** | "Foundation Model Ops" — a broader frame than LLMOps, covering the operational concerns of any large pre-trained foundation model (text, vision, multimodal) that gets adapted/fine-tuned for downstream tasks |
| **GitOps** | A specific implementation pattern (mostly from the Kubernetes/infrastructure world) where Git is the single source of truth and all changes to a system happen through Git commits + automated reconciliation. MLOps pipelines frequently *use* GitOps as their deployment mechanism, but GitOps itself is not ML-specific |

The practical takeaway: MLOps is the umbrella most relevant to this course, but you will encounter all
of these terms in the wild, often used loosely — knowing the distinctions helps you read a job posting,
a vendor's marketing page, or a conference talk correctly.

## 11. Major phases — what it takes to master MLOps

Organizations don't adopt MLOps all at once — they move through recognizable levels of maturity:

| Level | What it looks like |
|---|---|
| 0 | Ad hoc: manual, notebook-driven, no version control discipline, no monitoring |
| 1 | Basic DevOps hygiene applied: code is versioned, a simple CI pipeline exists |
| 2 | Reproducible training pipelines; models and data are versioned and tracked in a registry |
| 3 | Full CI/CD/CT: automated testing, automated deployment, and production monitoring are all in place |
| 4 | Continuous training and retraining pipelines trigger automatically based on monitored signals, with human oversight retained at the decision points that matter |

Mastering MLOps doesn't mean reaching Level 4 for every project — a small internal tool and a
customer-facing fraud model warrant very different levels of investment. Part of the skill this course
builds is judgment: knowing which level of rigor a given project actually needs.

## 12. CI/CD in production: a worked scenario

To make all of the above concrete, walk through a composite, illustrative scenario (not a specific
real company — a generic pattern that recurs across many production ML systems):

An e-commerce team ships a model that ranks search results. Every time an engineer merges a change to
the ranking code, code, or to the training data pipeline:

1. A CI pipeline automatically runs unit tests on the code and a smaller-scale training run to confirm
   the model still trains without errors.
2. If those pass, a CD pipeline builds a new container image and deploys it to a staging environment.
3. A held-out evaluation set (not seen during training) is scored, and the new model's metrics are
   compared against the currently deployed model's — this is the "continuous evaluation" gate; if the
   new model doesn't beat a minimum bar, the pipeline stops here automatically.
4. If it passes, the new model is rolled out gradually (e.g. to 5% of traffic first), while a
   monitoring system compares live business metrics and model-quality metrics between the old and new
   model.
5. If the new model's live metrics hold up, traffic is ramped to 100%. If they don't, the pipeline
   automatically rolls back to the previous model version — no human had to notice the regression
   manually at 2 a.m.
6. Ongoing production monitoring keeps watching the now-fully-rolled-out model for drift; when it
   detects the input data distribution has shifted meaningfully, it flags the model for retraining,
   closing the loop back to step 1.

Every step in that scenario maps directly onto a module later in this course: step 1-2 is Module 4
(CI/CD), step 2 is also Module 5 (containerization), step 3 uses tooling from Module 10 (experiment
tracking), steps 4-5 draw on Module 7 (cloud deployment), and step 6 is Module 9 (monitoring). This
scenario is worth revisiting after each of those modules — you'll be able to say precisely how you'd
implement each step yourself.

---

## Summary

MLOps is what turns a trained model into a system other people can actually depend on. It exists
because production ML has failure modes that classical software testing was never designed to catch,
and because the gap between "it worked in the notebook" and "it's reliably serving real users" is where
most ML projects quietly die. The rest of this course is a tour of the concrete tools and practices that
close that gap — one module, one component of the MLOps stack, at a time.

## Further reading

* See the [Course books](../README.md#course-books) for deeper dives on applied ML engineering and
  production reliability.

## References

Foundational industry/academic sources this module's content draws on:

* Sculley, D., et al. ["Hidden Technical Debt in Machine Learning Systems."](https://papers.nips.cc/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf)
  NeurIPS, 2015. — the original, widely-cited paper on the industrialisation challenges unique to ML
  systems (§3, §4).
* Google Cloud. ["MLOps: Continuous Delivery and Automation Pipelines in Machine Learning."](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
  Architecture guide. — source for the MLOps components and CI/CD/CT framing (§5, §8, §12).
* Microsoft. ["MLOps Maturity Model."](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/mlops-maturity-model)
  Azure Architecture Center. — source for the 5-level maturity framework (§11).
* ["Operationalizing Machine Learning: An Interview Study."](https://arxiv.org/abs/2209.09125)
  arXiv, 2022. — source for the practitioner-reported MLOps challenges discussed in §6.
