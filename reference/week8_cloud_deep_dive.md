# Reference material for Week 8 — Module 7: Deep Dive into MLOps Cloud Services (AWS, Azure & GCP)

> Source: [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) `s6_the_cloud/cloud_setup.md` and
> `using_the_cloud.md`, Apache 2.0, copied in full. **Important scope note**: DTU's course is GCP-only
> (Compute Engine, Cloud Storage, Artifact Registry, Cloud Build, Vertex AI) — it has no AWS SageMaker
> or Azure ML content at all. This module's AWS SageMaker and Azure ML Studio sections (see the
> "Still to source" list at the end) need to be written entirely from scratch; only the GCP/Vertex AI
> third of this module can lean on DTU material. `s7_deployment/*` (FastAPI, cloud deployment, API
> testing, ML deployment, frontend) is also folded in below since DTU treats cloud deployment as a
> continuation of this same GCP thread.

---

## Part 1 — Cloud setup (`cloud_setup.md`)

# Cloud setup

!!! info "Core Module"

GCP is Google's cloud platform. The core selling point of any cloud provider is near-infinite scalable resources —
many modern deep learning workloads simply aren't feasible to run locally.

## Exercises — account & local setup

1. Claim cloud credits (institution-specific, or the provider's standard free-tier signup credit — note a credit
    card is typically required even for "free" credits, so credit usage should be monitored closely).

2. Log in to the cloud console; check the billing page to confirm credit balance, and watch the usage/reports tab
    throughout the course.

3. Create a dedicated project (DTU names theirs `dtumlops`) to keep resources organized.

    !!! warning "Create project under 'No organization' (GCP-specific, but the general lesson applies elsewhere too)"

        Organization-managed accounts (including university/Workspace accounts) often enforce policies that block
        creating service-account keys — needed later to authenticate services like GitHub Actions with the cloud.
        Creating the project under "No organization" avoids this while learning. (The equivalent gotcha exists on
        AWS/Azure too, under organization-level SCPs / management-group policies — worth flagging generically.)

4. Install the CLI (`gcloud` for GCP; `aws` CLI for AWS; `az` CLI for Azure) and authenticate:

    ```bash
    gcloud auth login
    gcloud auth application-default login
    gcloud config set project <project-id>
    ```

5. Install the provider's Python SDK (`google-api-python-client` for GCP; `boto3` for AWS; `azure-sdk-for-python`
    packages for Azure).

6. Enable the developer APIs/services you'll need (each provider requires explicit service enablement before use):

    ```bash
    gcloud services enable apigateway.googleapis.com
    gcloud services list   # check what's enabled
    ```

## IAM, quotas, and service accounts

* **IAM** (Identity and Access Management) governs who/what can do what. Sharing a project with teammates: grant
  `Viewer`/`Editor`/`Owner` access via email.
* **Quotas** limit resource consumption per project (e.g. GPU count) — free/education accounts typically default to
  0–1 GPUs; request an increase via the quotas page once the relevant service is enabled (5–10 min propagation delay,
  and requests may be rejected within 24h of account creation).
* **Service accounts** are non-human identities used for machine-to-machine auth (e.g. GitHub Actions authenticating
  to the cloud to trigger a build). Always grant the **lowest possible permission** needed
  ([principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege)) — e.g. `Storage Object
  Viewer` for read-only bucket access, not broader roles. Common roles used across this course:

  * `Storage Object Viewer` — list/download bucket objects
  * `Cloud Build Builder` — run Cloud Build jobs
  * `Secret Manager Secret Accessor` — read secrets
  * `Cloud Run Developer` — deploy Cloud Run services
  * `AI Platform Developer` — use Vertex AI
  * `Artifact Registry Writer` — push images

  A service account key is a downloadable JSON credential — treat it exactly like a password.

## Knowledge check — cross-cloud service name mapping (directly reusable for this course's AWS/Azure/GCP framing)

| GCP | AWS | Azure |
|---|---|---|
| Compute Engine | EC2 | Virtual Machines |
| Cloud Storage | S3 | Blob Storage |
| Cloud Functions | Lambda | Functions (Serverless Compute) |
| Cloud Run | App Runner, Fargate, Lambda | Container Apps, Container Instances |
| Cloud Build | CodeBuild | DevOps (Pipelines) |
| Vertex AI | SageMaker | Azure ML / AI Platform |

This table is exactly the kind of cross-provider mapping this module's whole premise depends on — worth
reproducing prominently, and extending with the Feature Store row (SageMaker Feature Store / Vertex AI Feature
Store / — no direct Azure equivalent, see Module 6) and the DevOps row (CodePipeline/CodeBuild/CodeDeploy /
Azure DevOps / Cloud Build+Deploy, see Module 4).

Region choice factors: service/resource availability (not all regions have all GPUs), latency (proximity to users),
compliance (e.g. EU data residency under GDPR), and pricing (varies by region).

---

## Part 2 — Using the cloud (`using_the_cloud.md`) — GCP compute, storage, build, training, secrets

# Using the cloud

## Compute (VMs)

Virtual machines let you scale horizontally (many machines), access hardware you don't own locally (e.g. specific
GPU configs), and run long background jobs without tying up your laptop.

* Create instances via console or CLI (`gcloud compute instances create ...`); price scales with CPU/GPU class,
  memory, disk, and region.
* A bare VM has no ML software pre-installed — GCP (and AWS/Azure) offer **ready-made deep-learning VM images**
  with Python/PyTorch/TensorFlow pre-baked (`--image-family=pytorch-latest-gpu --image-project=deeplearning-platform-release`
  + `--accelerator=type=nvidia-tesla-t4,count=1` for GPU).
* SSH in via CLI or browser-based terminal; remember to **stop VMs when not in use** — billed by the minute
  regardless of whether it's doing anything.

## Data storage

Cloud object storage (GCS/S3/Blob) is cheap (~$0.026/GB/month on GCS), durable (multi-location replication), and —
critically for DVC users — accessible via API without repeated interactive auth (unlike a personal Google Drive
remote).

* Create a bucket, enable object versioning.
* `gsutil`/`aws s3`/`az storage` CLI for basic object operations.
* Point DVC at the bucket instead of a personal Drive account:

    ```bash
    dvc remote add -d remote_storage <bucket-url>
    dvc remote modify remote_storage version_aware true
    dvc push --no-run-cache
    ```

* Accessing bucket data from a VM/container without repeated interactive auth: either make the bucket public (easy,
  insecure) or authenticate via a service account (`GOOGLE_APPLICATION_CREDENTIALS` env var pointing at the key file)
  — the AWS/Azure equivalents are IAM roles attached to compute, and managed identities, respectively.

## Building & storing containers in the cloud (Cloud Build + Artifact Registry)

Building Docker images locally is slow and images are large — move both the build and the storage to the cloud.

* **Artifact Registry** (GCP) / **ECR** (AWS) / **Azure Container Registry** — create a Docker-format repository,
  optionally with a cleanup policy (keep last N versions, to control storage cost).
* **Cloud Build** (GCP) / **CodeBuild** (AWS) / **Azure Pipelines / ACR Tasks** (Azure) — a YAML pipeline spec
  analogous to a GitHub Actions workflow file, but with provider-specific syntax:

    ```yaml
    # cloudbuild.yaml
    steps:
    - name: 'gcr.io/cloud-builders/docker'
      id: 'Build container image'
      args: ['build', '.', '-t', '<region>-docker.pkg.dev/$PROJECT_ID/<repo>/<image>', '-f', '<dockerfile>']
    - name: 'gcr.io/cloud-builders/docker'
      id: 'Push container image'
      args: ['push', '<region>-docker.pkg.dev/$PROJECT_ID/<repo>/<image>']
    ```

    Trigger manually (`gcloud builds submit . --config=cloudbuild.yaml`) or automatically on push via a connected
    repository trigger (GitHub ↔ Cloud Build integration).

* Steps can depend on each other (`waitFor: ['step_id']`) or run concurrently (`waitFor: ['-']`) — directly parallel
  to GitHub Actions' `needs:` keyword.
* **Integrating the cloud build step into GitHub Actions itself** (rather than a native repo trigger) — lets the
  build depend on other CI steps (e.g. only build if tests pass on all OSes):

    ```yaml
    jobs:
      test: ...
      build:
        needs: test
        if: ${{ github.event_name == 'push' && github.ref == 'refs/heads/main' }}
        steps:
          - uses: actions/checkout@v5
          - uses: google-github-actions/auth@v2
            with:
              credentials_json: ${{ secrets.GCLOUD_SERVICE_KEY }}
          - uses: google-github-actions/setup-gcloud@v2
          - run: gcloud builds submit . --config cloudbuild_containers.yaml
    ```

    (This is the exact pattern that carries over — with different action names — for AWS CodeBuild and Azure
    Pipelines triggered from GitHub Actions; worth writing parallel snippets for both when building this section.)

* **Substitutions** — parametrize a single `cloudbuild.yaml` for multiple image names/tags via `substitutions:` and
  `--substitutions=` on the CLI.

## Training

Two escalating approaches to running training jobs in the cloud:

1. **Compute Engine (manual VM)** — create a VM with an ML-ready image, SSH in, clone repo, install deps, run
    training. Simple but doesn't scale — one VM per experiment, managed by hand.

2. **Vertex AI custom jobs** (GCP) / **SageMaker Training Jobs** (AWS) / **Azure ML compute + jobs** (Azure) — an
    abstraction layer that provisions the VM, pulls a specified container, runs the job, and tears the VM down
    automatically:

    ```bash
    gcloud ai custom-jobs create \
        --region=europe-west1 \
        --display-name=test-run \
        --config=config.yaml \
        --command 'python src/my_project/train.py' \
        --args=--epochs=10 --args=--batch-size=128
    ```

    with a `config.yaml` specifying machine type, (optional) accelerator type/count, and container image URI. GPU
    quota approval is required and separate from CPU quota.

    Training jobs can mount cloud storage as a filesystem (`/gcs/<bucket>/...` on GCP) instead of downloading data
    first — often faster than a DVC pull inside the job.

    Environment variables (e.g. a W&B API key) can be injected via the job config's `env` field — but a raw API key
    in a config file is itself a secret-management problem, which leads to:

## Secrets management

Cloud-native secret stores (**Secret Manager** on GCP, **Secrets Manager** on AWS, **Key Vault** on Azure) let you
avoid hardcoding credentials into config files. A common pattern: use the build pipeline to substitute the secret
into a config template right before submitting the training job (`envsubst` + `availableSecrets`/`secretEnv` in
Cloud Build; equivalent secret-injection steps exist in CodeBuild buildspecs and Azure Pipelines variable groups).

## Knowledge check

* **Stopped vs. suspended VM**: a suspended VM preserves memory/device/application state (charged for storage of
  that state, not compute); a stopped VM discards all state (charged only for attached disk storage). Attached
  static IPs/persistent disks are billed regardless until explicitly deleted.

---

## Cross-reference — `s7_deployment/` (folded into this module's cloud-deployment coverage)

DTU's Session 7 (Deployment: `apis.md` [FastAPI], `cloud_deployment.md`, `testing_apis.md`, `ml_deployment.md`
[ONNX/BentoML], `frontend.md`) is fully copied into **`week8_deployment_fastapi_onnx.md`** — read that file
alongside this one for the complete GCP-deployment third of this module (requests/APIs → Cloud Functions/Cloud Run →
API testing → ONNX/BentoML serving → Streamlit frontend).

## Still to source for this module (no DTU equivalent — write from scratch)

* **AWS SageMaker** section in full: SageMaker Notebooks, IAM role/VPC setup, build/train/deploy via SageMaker,
  endpoints, SageMaker Pipelines, SageMaker Studio/domain/Projects, model groups — DTU has zero AWS content
* **Azure ML** section in full: Azure ML Studio, ML components, Azure MLOps + DevOps integration, fully automated
  CI/CD ML pipelines (Azure MLOps v2) — DTU has zero Azure content
