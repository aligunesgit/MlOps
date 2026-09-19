# Reference material for Week 12 — Project Sprint B (final)

> Source: [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) `reports/README.md` (report template) and
> `s10_extra/documentation.md` (Apache 2.0), copied in full/condensed. This is DTU's exam/hand-in
> mechanism — highly reusable structurally (report template + validation script + module-tagged
> checklist), though the module numbers (M5, M8, M16, etc.) referenced throughout are DTU's own and
> need remapping to this course's Module 1–10 + Sprint A/B numbering before reuse.

---

## Part 1 — Project report template (`reports/README.md`)

DTU's exam consists **only** of this report (pass/fail grading) — no separate written exam. The report lives in a
`reports/` folder inside the student's own project repo (copied from this template at project start), with a
companion `report.py` script offering two utilities:

```bash
python report.py html    # renders the filled-in report to a standalone .html page (used for the final hand-in)
python report.py check   # validates each answer against length constraints, checks required images are present
```

`report.py` depends only on `typer` + `markdown`. Structural requirement for the auto-scraping to work: the report
**must** live at `<repo-root>/reports/README.md`, with any figures placed in `reports/figures/`.

### The report is a fixed set of ~31 numbered questions, grouped by topic

Rather than being open-ended, DTU forces every group through the exact same question set — this is what makes the
report scrapeable/gradeable at scale across many student groups. Section groupings (question numbers are DTU's own,
included for reference — this course would renumber based on its own module list):

* **Group information** (Q1–3) — group/member IDs, third-party frameworks used beyond the course
* **Coding environment** (Q4–6) — dependency management, cookiecutter template usage/deviation, code quality/typing/docs
* **Version control** (Q7–11) — test count/coverage, branches/PRs, DVC usage, CI setup detail
* **Running code & experiment tracking** (Q12–16) — config management, reproducibility guarantees, W&B screenshots,
  Docker usage, debugging/profiling
* **Working in the cloud** (Q17–22) — GCP services used, Compute Engine usage, bucket/registry/build-history
  screenshots, cloud training
* **Deployment** (Q23–26) — API implementation, deployment method + invocation, functional/load testing results,
  monitoring implementation
* **Overall discussion** (Q27–31) — cloud cost/credits spent, extras implemented beyond the checklist, architecture
  diagram + explanation, biggest struggles, individual contributions **+ explicit disclosure of generative AI tool
  usage** (this last point is worth keeping verbatim — DTU explicitly requires students to state how/if they used
  ChatGPT/Copilot/etc.)

Every question comes with: the exact question text, a recommended answer-length range (e.g. "100–200 words"), and
an example answer shape (never a real answer — just illustrating the expected tone/structure). Questions asking for
screenshots (bucket contents, artifact registry, cloud build history, architecture diagram, W&B dashboard) point at
placeholder figure paths (`figures/bucket.png` etc.) that the student must have actually created and referenced.

### The checklist embedded at the top of the report

The same module-tagged checklist that lives in `pages/projects.md` (already captured in the original
`CURRICULUM_DRAFT.md` conversation) is duplicated inside the report template itself, split into Week 1/2/3/Extra —
students check off what they actually did; **the checklist is explicitly "exhaustive," not a required 100% list**.
DTU is explicit that grading is based on the actual repository + code review, not just checked boxes — the honesty
framing ("please be honest in your answers, we will check the repositories and the code to verify your answers") is
worth keeping.

### Action items for this course's version of this file

1. Rewrite the ~31 questions' module-number references (M5, M8, M16, ... M31) to this course's own numbering
   (Module 1–10 + Sprint A/B).
2. Decide whether the assessment model matches DTU's (report-only, pass/fail) — flagged as an open decision in
   `CURRICULUM_DRAFT.md`'s Course Info table. If this course adds a presentation/exam component, the report
   template's question set would need a corresponding "presentation notes" or oral-defense section added.
3. Port `report.py`'s two utility commands (`html`, `check`) — these are small, self-contained, and worth reusing
   near-verbatim regardless of question-content changes.

---

## Part 2 — Documentation (`s10_extra/documentation.md`) — for the checklist's "write + publish documentation" items

# Documentation

Good documentation is often the difference between someone adopting a codebase and abandoning it. This module
teaches a minimal auto-generated **API documentation** system (not full narrative docs) — assumes the
docstring/typing conventions from Module 3's good-coding-practice content (see `supplementary/dev_tools_cli_and_style.md`).

Static-site generator options: MkDocs, Sphinx, GitBook, Docusaurus, Doxygen, Jekyll — DTU (and this course's own
website, per `CURRICULUM_DRAFT.md`'s planned repo structure) uses **MkDocs + Material for MkDocs theme**, chosen
for being markdown-based and Python-native (vs. Sphinx, which is more powerful but has a steeper learning curve —
worth mentioning as the "if you outgrow MkDocs" pointer).

### Minimal `mkdocs.yaml`

```yaml
site_name: Documentation of my project
docs_dir: source
theme:
  name: material
  features:
    - content.code.copy
    - content.code.annotate
plugins:
  - search
  - mkdocstrings   # auto-generates docs from docstrings
nav:
  - Home: index.md
```

### Auto-generating API docs from docstrings

```markdown
# My API

::: src.models.model.MyNeuralNet

::: src.predict_model.predict
```

The `:::` directive (via the `mkdocstrings` plugin) pulls in the docstring/signature of the named function/class
automatically — write good docstrings once (Module 3 content), get documentation for free.

```bash
mkdocs serve    # live-reloading local preview
mkdocs build    # produces a `site/` folder of static HTML
```

### Publishing to GitHub Pages

Requires GitHub Actions basics (Module 4). A `deploy_docs.yaml` workflow:

```yaml
name: Deploy docs
on:
  push:
    branches: [main]
permissions:
  contents: write   # needed because this workflow pushes to the gh-pages branch
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: mkdocs gh-deploy --force
```

Then in the repo's Settings → Pages: set source to "Deploy from a branch", branch `gh-pages`, folder `/(root)`. Site
publishes at `https://<username>.github.io/<reponame>/`.

**This is exactly the mechanism this course's own repo (per `CURRICULUM_DRAFT.md`'s planned `.github/workflows/`)
will use to publish its own course site** — a nice pedagogical hook: the same workflow pattern teaching students
how to publish *their* project's docs is the one the instructor used to publish the course material itself.

### Knowledge check takeaway

Documentation is best treated as an ongoing part of writing code, not a one-time end-of-project task — worth
stating explicitly since students otherwise treat this checklist item as an afterthought squeezed into Sprint B.
