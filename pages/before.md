# Introduction

Welcome to **1413211011 — MLOps and AI Systems Engineering**. This course exists to fill a specific gap:
most students and practitioners coming out of a machine learning education know how to build a model,
but not how to take that model from a notebook to a system that other people can actually rely on. This
course is about that second half — the "Operations" in MLOps.

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

