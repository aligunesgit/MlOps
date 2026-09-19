# Reference material for Week 5 — Module 5: Docker & Kubernetes Overview

> Source: [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) `s3_reproducibility/docker.md`
> (Apache 2.0), copied in full for the Docker half of this module. The Kubernetes half will be
> appended below once sourced from `s10_extra/kubernetes.md` (that file exists in DTU's repo but is
> excluded from their *published* mkdocs site — likely an unfinished/experimental module on their end —
> so treat it as a rougher starting draft, not polished lesson content).

---

## Part 1 — Docker (`docker.md`)

# Docker

!!! info "Core Module"

A big part of creating an MLOps pipeline is being able to **reproduce** it. Reproducibility goes beyond versioning our
code with `git` and using `conda`/`uv` environments to keep track of our Python installations. To truly achieve
reproducibility, we need to capture system-level components such as:

* Operating system
* Software dependencies (other than Python packages)

Docker provides this kind of system-level reproducibility by creating isolated program dependencies. In addition to
reproducibility, one of Docker's key features is scalability — because Docker ensures system-level reproducibility, it
doesn't matter (conceptually) whether we start our program on one machine or 1,000 machines at once.

## Docker Overview

Docker has three main concepts: **Dockerfile**, **Docker image**, and **Docker container**:

* A **Dockerfile** is a text document containing all the commands a user could call on the command line to run an
    application — installing dependencies, pulling data, setting up code, specifying run commands (e.g. `python train.py`).
* *Building* a Dockerfile creates a **Docker image** — a lightweight, standalone, executable package including
    everything (code, libraries, tools, dependencies) needed to run the application.
* *Running* an image creates a **Docker container**. The same image can be launched multiple times, creating multiple
    containers.

## Docker Sharing

Two ways to share a containerized application:

* Commit the `Dockerfile` to GitHub (it's just a text file) and ask others to build the image themselves.
* Push the built image to a registry such as [Docker Hub](https://hub.docker.com/), so others can `docker pull` it and
    run it instantly as a container.

## Exercises

1. [Install Docker](https://docs.docker.com/get-docker/) (macOS: OrbStack or Docker Desktop; Windows: Docker Desktop +
    WSL2 backend). Restart after installing. This course uses Docker's CLI only, not the GUI.

2. Confirm the install: `docker run hello-world`.

3. Pull a tiny test image: `docker pull busybox`.

4. `docker images` — list locally available images; confirm `busybox` shows up.

5. `docker run busybox` does nothing visible (no command was given to run). Try:
    `docker run busybox echo "hello from busybox"` — note how fast Docker starts a VM, runs a command, and kills it.

6. `docker ps` (running containers) vs. `docker ps -a` (all containers, including stopped ones).

7. Interactive mode for exploring a container's filesystem: `docker run -it busybox`.

8. Stray stopped containers pile up disk space — clean up with `docker rm <container_id>`, or use `--rm` on `docker run`
    to auto-remove after exit.

9. Constructing an actual project Dockerfile (e.g. `train.dockerfile`):

    ```dockerfile
    # Base image (pip)
    FROM python:3.12-slim
    # or (uv, faster dependency installs)
    FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

    RUN apt update && \
        apt install --no-install-recommends -y build-essential gcc && \
        apt clean && rm -rf /var/lib/apt/lists/*

    # --- pip variant ---
    COPY requirements.txt requirements.txt
    COPY pyproject.toml pyproject.toml
    COPY src/ src/
    COPY data/ data/
    WORKDIR /
    RUN pip install -r requirements.txt --no-cache-dir
    RUN pip install . --no-deps --no-cache-dir
    ENTRYPOINT ["python", "-u", "src/<project-name>/train.py"]

    # --- uv variant ---
    COPY uv.lock uv.lock
    COPY pyproject.toml pyproject.toml
    COPY README.md README.md
    COPY src/ src/
    COPY data/ data/
    WORKDIR /
    RUN uv sync --locked --no-cache --no-install-project
    ENTRYPOINT ["uv", "run", "src/<project-name>/train.py"]
    ```

    Splitting dependency install from code copy lets Docker cache the (slow) dependency layer separately from the
    (frequently changing) application code layer.

10. Build: `docker build -f train.dockerfile . -t train:latest` (note the `-t` tag and the trailing `.` build context).
    On Apple Silicon, cross-platform builds may need `--platform linux/amd64` (slower, emulated).

11. Run: `docker run --name experiment1 train:latest`. Multiple containers from the same image can run concurrently
    under different `--name`s.

12. Speed up rebuilds with BuildKit cache mounts:

    ```dockerfile
    # pip
    RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt --no-cache-dir
    # uv
    ENV UV_LINK_MODE=copy
    RUN --mount=type=cache,target=/root/.cache/uv uv sync
    ```

13. Explore a container's filesystem interactively: `docker run --rm -it --entrypoint sh {image}:{tag}`.

14. Getting files *out* of a container: `docker cp {container}:{path} {local_path}` for one-off copies, or mount a
    volume for ongoing sync: `docker run --name c -v %cd%/models:/models/ train:latest`.

15. A second Dockerfile for prediction/evaluation (`evaluate.dockerfile`), mounting the trained model + test data as
    volumes at run time.

16. (Optional, GPU) Building a GPU-enabled image needs the Nvidia Container Toolkit installed on the host, and
    swapping the base image to an Nvidia/PyTorch NGC image:

    ```dockerfile
    FROM nvcr.io/nvidia/pytorch:22.07-py3
    ```

    Verify with `docker run --gpus all ... python -c "import torch; print(torch.cuda.is_available())"`.

17. (Optional) **Dev Containers** — developing *inside* a container via VS Code's Remote-Containers extension, using
    a `.devcontainer/Dockerfile` + `.devcontainer/devcontainer.json` (`postCreateCommand` running `uv sync --locked`
    or `pip install -r requirements.txt`).

18. (Optional) Incorporating `dvc` (data version control) into a Docker image — `dvc init --no-scm`, copying the
    `.dvc/config` + metafiles, and pulling data credentials into the image at build time (`dvc pull`).

## Knowledge check

* **Image vs. container**: an image is a static template; a container is a running instance of that image.
* **Three steps to containerize**: write Dockerfile → build image → run container.
* **Why containers over bare-metal**: consistent, portable, isolated runtime environment across machines.
* **Layer caching**: images are built from stacked layers; only changed layers need to be rebuilt/re-downloaded,
  which is why splitting "install deps" from "copy app code" into separate layers matters.

If actively using Docker going forward, image size becomes a real concern (multi-GB images with PyTorch are common) —
worth a pointer to image-size-reduction techniques and tools like `dive` for inspecting image layers.

---

## Part 2 — Kubernetes (`s10_extra/kubernetes.md`)

> DTU's own file opens with `!!! danger "Module is still under development"` and is **excluded from their
> published mkdocs site** — the content below is genuinely just a skeleton on their end, copied in full, not
> condensed. Treat as a starting outline to flesh out, not finished lesson material.

# Kubernetes

Kubernetes (K8s) automates deployment, scaling, and operation of containerized applications across a cluster of
hosts — resilient distributed systems, scaling, failover, deployment patterns. Originally built by Google, now
maintained by the Cloud Native Computing Foundation.

**Architecture** — client-server: a **Control Plane** (master) and **Nodes** (workers).

* Control plane components: **API Server** (Kubernetes' frontend), **etcd** (consistent key-value store), plus
  others DTU's draft leaves as "..." (scheduler, controller-manager — standard K8s components to fill in)
* Node components: **Kubelet** (per-node agent), **Container Runtime** (runs the containers), plus others left as
  "..." (kube-proxy — standard to fill in)

**Minikube** — run a single-node K8s cluster locally in a VM, for learning/dev without a real cluster:

```bash
minikube start
minikube        # validate install
kubectl         # validate the K8s CLI is installed
```

**Yatai** — a [BentoML-adjacent](https://github.com/bentoml/Yatai) model-serving platform for Kubernetes,
simplifying ML model deployment/management/scaling on K8s specifically (ties back to Module 7's BentoML content in
`week8_deployment_fastapi_onnx.md`).

DTU's own module stops here with pointers to the official K8s docs, tutorials, and community forum — this is the
weakest-covered topic in DTU's entire repo. Given this course's Module 5 explicitly lists Pod/ConfigMap/Service/
Secret/Ingress/Deployment/StatefulSet/DaemonSet/Volumes(PVC) as required content, **this whole resource list needs
to be written from scratch** — DTU's draft doesn't even name most of them.

## Still to source for this module

* Docker Network Types, Docker Volumes (as a dedicated topic — DTU's docker.md above touches volumes only via `-v`
  mount examples, not network types)
* Docker Compose, Docker Swarm — not covered by DTU's docker.md at all; write from scratch
* Projects: "Deploy a Node.js app in a Docker container", "Deploy a complete end-to-end ML model with Docker
  Compose" — DTU's `samples/frontend_backend/` folder (FastAPI backend + Streamlit-style frontend, each with its own
  Dockerfile + a `docker-compose`-style Makefile) is a good structural reference for the Compose project — see
  `week8_cloud_deep_dive.md` where the same sample is referenced for the S7 deployment/frontend modules
* Kubernetes resources and Minikube exercise — see placeholder above
