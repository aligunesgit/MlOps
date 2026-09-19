# Reference material for Week 8 — Module 7 (continued): Deployment content from DTU's Session 7

> Source: [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) `s7_deployment/apis.md`, `cloud_deployment.md`,
> `testing_apis.md`, `ml_deployment.md`, `frontend.md` (Apache 2.0), copied in full/condensed. This is
> the largest chunk of DTU material directly reusable for Module 7's GCP third (deployment via
> Cloud Functions/Cloud Run, testing deployed APIs, ONNX/BentoML packaging, frontend). See
> `week8_cloud_deep_dive.md` for the compute/storage/build/training/secrets half of this module.

---

## Part 1 — Requests and APIs (`apis.md`)

# Requests and APIs

Before deployment, two prerequisite concepts: **requests** (client-side: how a user talks to a server) and **APIs**
(server-side: how you expose your application to be talked to).

### HTTP requests

An HTTP request has a **URL** (where) and a **method** (what action): `GET` (retrieve), `POST`/`PUT` (send data),
`DELETE` (remove). Responses carry a **status code** (200 = success, 404 = not found, etc.) and a **payload** (raw
bytes, usually parsed as JSON).

```python
import requests
response = requests.get('https://api.github.com')
print(response.status_code)
print(response.json())          # JSON payload as a nested dict
```

Query parameters via `params=`; POST payloads via `data=`. Unauthenticated API calls are often rate-limited (e.g.
GitHub: 60/hour per IP unauthenticated vs. 5,000/hour authenticated via a personal access token passed as an
`Authorization` header) — worth teaching students to check `response.status_code` and rate-limit headers before
assuming a failure is their own bug. `curl` can send the same requests from the terminal directly.

### Building APIs — REST and FastAPI

An API is the abstraction layer letting others use your application without reading your code. **REST** APIs must be
**stateless**: every request is self-contained; the server never relies on memory of previous requests.

[FastAPI](https://fastapi.tiangolo.com/) — "a modern, high-performance web framework... based on standard Python
type hints" — is the framework of choice here (vs. Flask/Django) for its balance of flexibility without excess
boilerplate.

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

```bash
uvicorn --reload --port 8000 main:app
```

* `/docs` and `/redoc` — auto-generated interactive API documentation (try-it-out UI, generates the `curl` command
  for you); `/openapi.json` — the machine-readable schema.
* Type hints drive automatic request **validation** via [pydantic](https://docs.pydantic.dev/) — a malformed request
  (e.g. a string where an `int` is expected) is rejected before your function body ever runs. Always type your
  endpoints.
* **Path parameters** (`{item_id}` in the URL) vs. **query parameters** (anything else) vs. **body** (JSON payloads
  for POST, via a pydantic model).
* Restricting a string path parameter to specific allowed values: use an `Enum`.
* File upload/response: `UploadFile`/`File` for input, `FileResponse` for output; `async`/`await` needed for
  file I/O endpoints.
* **Lifespan events** — code that runs on startup/shutdown (e.g. loading a model once at startup rather than per
  request):

    ```python
    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("Hello")   # startup
        yield
        print("Goodbye") # shutdown

    app = FastAPI(lifespan=lifespan)
    ```

* An ML-serving example: wrapping a HuggingFace image-captioning model (`VisionEncoderDecoderModel`) behind a
  FastAPI endpoint that takes an image and returns a caption.
* Containerizing a FastAPI app:

    ```dockerfile
    FROM python:3.11-slim
    WORKDIR /code
    COPY ./requirements.txt /code/requirements.txt
    RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
    COPY ./app /code/app
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
    ```

    ```bash
    docker build -t my_fastapi_app .
    docker run --name mycontainer -p 80:80 myimage
    ```

Worth pointing students at [BentoML](https://github.com/bentoml/BentoML) (see Part 4 below) and
[Postman](https://www.postman.com/) for API design/testing beyond what's covered here.

---

## Part 2 — Cloud deployment (`cloud_deployment.md`) — GCP Cloud Functions & Cloud Run

# Cloud deployment

GCP offers several deployment targets; this module focuses on the two **serverless** ones (no infrastructure to
manage): **Cloud Functions** and **Cloud Run**. The non-serverless alternatives (Kubernetes Engine, Compute Engine)
require managing the underlying infrastructure yourself.

### Cloud Functions — for single-script applications

Simplest deployment target: write one Python function decorated with `@functions_framework.http`, and GCP handles
everything else. Good for small, single-file applications (e.g. a trained `sklearn` model loaded from a bucket,
taking a list of numbers, returning a prediction). Deployable via console UI or:

```bash
gcloud functions deploy <func-name> \
    --gen2 --runtime python311 --trigger-http --source <folder> --entry-point <function_name>
```

Cloud Functions' built-in metrics/logs tabs show invocations/sec, execution time, memory usage, instance count —
worth a quick tour when teaching this, since it previews the same telemetry concepts covered later in Module 9
(Monitoring).

### Cloud Run — for containerized applications

Scales beyond Cloud Functions' single-script limitation: deploy **any Docker container** as a scalable, serverless
service. Steps: build image locally → push to Artifact Registry → create a Cloud Run service pointing at the image →
set port + auth policy (`--allow-unauthenticated` while learning) → deploy.

```bash
gcloud run deploy <service-name> \
    --image <image-name>:<image-tag> --platform managed --region <region> --allow-unauthenticated
```

Common gotcha: the container must listen on the `$PORT` env var Cloud Run injects (default 8080), and must `EXPOSE`
that port in the Dockerfile — a container that ignores this and hardcodes a different port fails to start.

**Continuous deployment**: extend the `cloudbuild.yaml` from Module 4's CI/CD content with a third step that calls
`gcloud run deploy` after build+push — so every push to `main` automatically rebuilds and redeploys.

**Mounted storage volumes** — a Cloud Run service can mount a storage bucket directly as a filesystem path, useful
for reading a model checkpoint on startup or writing runtime statistics without wiring up a database.

**Secrets in Cloud Run** — inject via `--update-secrets=<env-var>=<secret-name>:latest`, backed by the same Secret
Manager covered in Module 4/`week8_cloud_deep_dive.md`.

For teams that outgrow serverless (need full control of the orchestration layer), the natural next step is
**Kubernetes** — covered in Module 5 (`week5_docker_kubernetes.md`).

---

## Part 3 — API testing (`testing_apis.md`)

# API testing

Two distinct concerns, both worth teaching as separate exercises:

1. **Functional testing** — does the API return the expected output for a given input? (Not quite the same as
    integration testing — a simple inference API with no external DB/service dependency is functionally tested,
    not integration tested.)
2. **Load/performance testing** — does the API survive realistic concurrent traffic?

### Functional testing (via `httpx` + FastAPI's `TestClient`)

Recommended test-folder layout, extending the unit-test structure from Module 4:

```plaintext
tests/
├── unittests/
│   ├── test_train.py
│   └── test_data.py
├── apitests/
│   └── test_apis.py
```

```python
from fastapi.testclient import TestClient
from my_project.api import app
client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome!"}
```

(If the app has `lifespan` events, wrap the client in a `with TestClient(app) as client:` block so startup/shutdown
hooks actually run.)

### Load testing (via [Locust](https://locust.io/))

```bash
pip install locust
```

```python
# tests/performancetests/locustfile.py
from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def predict(self):
        self.client.get("/predict?x=1.0")
```

```bash
locust -f tests/performancetests/locustfile.py --headless --users 10 --spawn-rate 1 --run-time 1m --host $MYENDPOINT
```

Key metrics: average response time, 99th-percentile response time (catches the "small number of very slow users"
problem the average hides), requests/second (capacity ceiling).

**Post-deployment load test in CI/CD** — a good pattern: after a deploy step succeeds, extract the deployed
service's URL, then run Locust against it automatically as a CI step, uploading results as a build artifact. Ties
directly into the CI/CD material from Module 4.

---

## Part 4 — ML-specific serving: ONNX & BentoML (`ml_deployment.md`)

# Deployment of Machine Learning Models

FastAPI is a *general* web framework — it wasn't built with ML serving in mind, so it lacks: **dynamic batching**
(processing requests in batches to amortize model-load/GPU overhead), **native async inference**, and **native GPU
scheduling**. ML-specific serving frameworks fill this gap: BentoML, Ray Serve, Triton, OpenVINO, Seldon-core,
LitServe (backend- and model-agnostic); TorchServe, TF Serving (backend-specific); vLLM (LLM-specific). Choice
criteria: ease of use, raw performance, and community size.

### ONNX — a portable model-packaging format

[ONNX](https://onnx.ai/) standardizes the computation graph + weights so a model trained in one framework
(PyTorch) can run on a different backend/hardware without re-implementing it.

```python
import torch, torchvision
model = torchvision.models.resnet18(weights=None)
model.eval()
dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(
    model=model, args=(dummy_input,), f="resnet18.onnx",
    input_names=["input"], output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}}
)
```

`dynamic_axes` marks which input dimensions can vary at inference time (e.g. batch size) — marking *every* axis
dynamic hurts the runtime's ability to optimize the graph, so mark only what actually needs to vary.

* Only a model's `forward`/`predict` method gets exported — make sure that method alone is sufficient for inference.
* [Netron](https://netron.app/) visualizes the exported graph.
* **ONNX Runtime** can apply graph optimizations (operator fusion) that reduce memory-load round-trips, and can
  target different execution providers (`CUDAExecutionProvider`, `CPUExecutionProvider`, ...), prioritized in a list.
* **Concrete size/speed payoff** (DTU's own measured numbers, illustrative for teaching): a PyTorch inference Docker
  image was 5.54GB (CUDA)/1.25GB (CPU-only) vs. an equivalent ONNX image at 647MB either way — roughly 8.5x/1.9x
  smaller — and built ~7x/1.3x faster. This kind of concrete before/after number is a good in-class demo.
* Always **numerically verify** an exported model against the original (`np.allclose` between ONNX Runtime output
  and native framework output, within a tolerance) — opset mismatches can silently change results.
* `scikit-learn` models export via the separate `sklearn-onnx` package; the exported method there is `predict`.

### BentoML — backend-/model-agnostic ML serving

```python
import bentoml
from transformers import pipeline

@bentoml.service(resources={"cpu": "2"}, traffic={"timeout": 10})
class Summarization:
    def __init__(self) -> None:
        self.pipeline = pipeline('summarization')

    @bentoml.api
    def summarize(self, text: str) -> str:
        return self.pipeline(text)[0]['summary_text']
```

```bash
bentoml serve service:Summarization
```

Features BentoML adds beyond FastAPI:

* **Adaptive batching** — define a max batch size + timeout; whichever triggers first, the collected batch gets
  sent to the model together, balancing latency vs. throughput.
* **GPU inference** — `@bentoml.service(resources={"gpu": 1})`.
* **Multiple workers** — `@bentoml.service(workers=4)` (or `workers="cpu_count"`) for multi-core scaling, parallel
  to `uvicorn --workers`.
* **Model composition** — sequential (pipeline of services) or concurrent (ensemble, outputs combined downstream)
  multi-model serving graphs.
* **`bentofile`** — a declarative alternative to hand-writing a Dockerfile (`bentoml build` → `bentoml containerize`).

### Knowledge check

* Computational graph = nodes (operations) + edges (data flow); the forward-pass graph is what enables
  backpropagation (it captures everything needed to compute gradients).
* Operator fusion improves performance mainly by reducing memory load/store round-trips between operations.

---

## Part 5 — Frontend (`frontend.md`)

# Frontend

The deployed model API is the **backend** — functional but not user-friendly. A **frontend** gives end users a
proper interface, and splitting frontend/backend also enables independently scaling the (usually heavier) backend —
a basic instance of [microservice architecture](https://martinfowler.com/articles/microservices.html).

Python-native frontend frameworks: Django, Reflex, Streamlit, Bokeh, Gradio. This module uses **Streamlit** — easy to
learn, easy to wire to a Python backend, though far less powerful/flexible than Django for a "real" production
frontend.

### Backend (FastAPI, e.g. an image classifier)

```python
# backend.py — single POST endpoint taking an image, returning a predicted class
```

Containerize, test locally with `curl -F 'file=@my_cat.jpg'`, then deploy to Cloud Run exactly as in Part 2 above.

### Frontend (Streamlit)

```python
import streamlit as st
# file uploader -> display image -> button -> call backend -> display result
```

```bash
streamlit run frontend.py
```

**Auto-discovering the backend URL** (instead of hardcoding it) via the Cloud Run Python SDK:

```python
from google.cloud import run_v2
import streamlit as st

@st.cache_resource
def get_backend_url():
    client = run_v2.ServicesClient()
    for service in client.list_services(parent="projects/<project>/locations/<region>"):
        if service.name.split("/")[-1] == "production-model":
            return service.uri
    return os.environ.get("BACKEND")
```

Deploy both frontend and backend as **separate** Cloud Run services, each with its own Dockerfile and its own
`requirements_*.txt` — keeping requirement files separate matters because the frontend doesn't need heavy backend
dependencies like `torch`, which keeps the frontend image dramatically smaller.

DTU's own worked example of this whole pattern lives in their repo root at `samples/frontend_backend/`
(`backend.py`, `frontend.py`, two Dockerfiles, a `requirements_backend.txt`/`requirements_frontend.txt`, and a
`Makefile`) — a good structural reference for this course's own Docker-Compose-style Module 5 project
("Deploy a complete end-to-end ML model with Docker Compose", see `week5_docker_kubernetes.md`).

### Knowledge check

* Separate requirement files per service (frontend vs. backend) → smaller, more independently deployable images;
  the frontend shouldn't need to bundle heavy ML libraries it never imports.
