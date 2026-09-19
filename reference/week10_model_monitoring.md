# Reference material for Week 10 — Module 9: Understanding Model Monitoring (AWS, Azure & GCP)

> Source: [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) `s8_monitoring/data_drifting.md` and
> `monitoring.md`, Apache 2.0, copied in full. DTU's monitoring content is GCP-only (Cloud Run sidecar
> containers, GCP Monitoring/Alerting) — the AWS and Azure model-monitoring sections, and the
> edge-optimization bullet, have no DTU equivalent (see "Still to source" below).

---

## Part 1 — Data drifting (`data_drifting.md`)

# Data drifting

!!! info "Core Module"

Data drift — the change in model input data over time that leads to degraded performance — is one of the core
reasons production model accuracy decays. The model receives inputs outside the distribution it was trained on. The
usual remedy: retrain on newly received data and redeploy — a cycle that repeats over the application's lifetime.
The remaining question: **when** should retraining actually trigger? We need tooling that detects drift, rather
than waiting for performance to visibly degrade.

## Exercises (using [Evidently](https://github.com/evidentlyai/evidently))

Alternative frameworks worth knowing about: [NannyML](https://github.com/NannyML/nannyml),
[WhyLogs](https://github.com/whylabs/whylogs), [deepcheck](https://github.com/deepchecks/deepchecks).

1. `pip install evidently scikit-learn pandas` (or `uv add evidently scikit-learn pandas`).

2. Starting point: an already-deployed classification API (DTU uses an iris classifier FastAPI app, itself
    converted from a GCP Cloud Function). Add a **background task** (FastAPI's `BackgroundTasks`) that logs every
    request's input + prediction + timestamp to a simple CSV "database", without slowing down the response:

    ```csv
    time, sepal_length, sepal_width, petal_length, petal_width, prediction
    2022-12-28 17:24:34.045649, 1.0, 1.0, 1.0, 1.0, 1
    ```

3. Build a `data_drift.py` script comparing **reference data** (the original training distribution) against
    **current data** (the logged production requests):

    ```python
    import pandas as pd
    from sklearn import datasets
    from evidently.legacy.report import Report
    from evidently.legacy.metric_preset import DataDriftPreset

    reference_data = datasets.load_iris(as_frame=True).frame
    current_data = pd.read_csv('prediction_database.csv')

    report = Report(metrics=[DataDriftPreset()])
    snapshot = report.run(reference_data=reference_data, current_data=current_data)
    snapshot.save_html('report.html')
    ```

    This generates a browsable HTML report showing per-feature drift.

4. Beyond `DataDriftPreset`, Evidently offers:
    * `DataQualityPreset` — flags missing values, data quality issues
    * `TargetDriftPreset` — detects when the *predicted label distribution* itself has shifted (e.g. a previously
      balanced classifier suddenly predicting one class far more often — a strong signal something upstream changed)

5. For programmatic (non-HTML) integration into a pipeline or CI workflow, use `TestSuite`/`Test` classes instead of
    `Report`:

    ```python
    from evidently.legacy.test_suite import TestSuite
    from evidently.legacy.tests import TestNumberOfMissingValues

    data_test = TestSuite(tests=[TestNumberOfMissingValues()])
    data_test.run(reference_data=reference_data, current_data=current_data)
    result = data_test.as_dict()
    print("All tests passed:", result['summary']['all_passed'])
    ```

6. (Optional) Filtering monitored data to a recent window (last N entries, or last T hours) before running drift
    checks — monitoring rarely wants to run over *all* historical data every time.

7. **Unstructured data (images/text)**: Evidently (like most drift frameworks) only natively supports tabular data.
    For images/text, first extract structured features (e.g. brightness/contrast/sharpness for images, or use a
    pretrained embedding model like [CLIP](https://arxiv.org/abs/2103.00020) to get abstract feature vectors for
    both images and text), then run drift detection on those extracted features instead of raw pixels/tokens.

8. (Optional) Exposing monitoring as its own deployed `/monitoring` endpoint alongside the main `/predict` endpoint
    of a service — returning an Evidently report/test-suite result as HTML or JSON on demand.

## Data drift in the cloud (GCP walkthrough — sentiment analysis example)

DTU walks through a full worked example: a BERT sentiment classifier deployed as a FastAPI app on Cloud Run, with
request/response data logged to a GCS bucket, and a second, separately-deployed FastAPI "monitoring" service that
runs Evidently's `TextOverviewPreset` + `TargetDriftPreset` against the logged data on demand. A companion client
script simulates production traffic that becomes progressively more "negative-skewed" over iterations, to
demonstrate drift actually being detected.

Key structural takeaway independent of which cloud provider: **(1)** the inference service logs input/output data
somewhere durable (bucket/database), **(2)** a separate monitoring service/job periodically compares that logged
data against the original training distribution, **(3)** the monitoring output should ideally be a structured
result (JSON/metrics) that feeds a dashboard, not just a one-off HTML report — see Part 2 below.

## Caveats (worth keeping in the lesson, not just the exercises)

* Monitoring ML systems is genuinely hard — there's no universal rule for *when* drift is "bad enough" to act on;
  it's application-specific.
* The tooling shown only tests **marginal** (per-feature) distributions — data can drift in ways that preserve each
  feature's marginal distribution while the *joint* distribution has shifted. Multivariate tests exist (e.g.
  [Maximum Mean Discrepancy](https://jmlr.org/papers/v13/gretton12a.html)) — the practical takeaway for students is
  to always look at multiple features together, not one at a time in isolation.

---

## Part 2 — Monitoring / telemetry (`monitoring.md`)

# Monitoring

## Telemetry — three kinds

| Kind | What it is | Example | Purpose |
|---|---|---|---|
| **Metrics** | Quantitative, aggregated numbers | Requests/minute | Dashboards, overview |
| **Logs** | Textual/structured event records | Error logs | Debugging, auditing, root-cause tracing |
| **Traces** | Per-transaction flow across components | Distributed tracing in microservices | Bottleneck/latency diagnosis |

This module focuses on **metrics** — the first telemetry type most teams instrument.

## Prometheus metric types

* **Counter** — monotonically increasing (or reset-to-zero-on-restart); e.g. total error count
* **Gauge** — arbitrary up/down value; e.g. current memory usage
* **Histogram** — bucketed observation counts + sum; e.g. request duration distribution
* **Summary** — like a histogram, but computes sliding-window quantiles instead of fixed buckets

## Instrumenting an application

```bash
pip install prometheus-client
```

```python
from prometheus_client import Counter, Histogram, Summary, CollectorRegistry, make_asgi_app

MY_REGISTRY = CollectorRegistry()
error_counter = Counter('errors_total', 'Total errors', registry=MY_REGISTRY)
request_counter = Counter('requests_total', 'Total requests', registry=MY_REGISTRY)
inference_time = Histogram('inference_seconds', 'Time to classify a review', registry=MY_REGISTRY)
review_size = Summary('review_size_chars', 'Size of reviews classified', registry=MY_REGISTRY)

app.mount("/metrics", make_asgi_app(registry=MY_REGISTRY))
```

Using a custom `CollectorRegistry` (rather than the implicit default one) matters — the default registry already
contains many metrics injected by the `prometheus-client` package itself, which clutters the `/metrics` endpoint if
you're trying to show only your own application metrics.

## Cloud monitoring (GCP walkthrough — generalizes to AWS/Azure equivalents)

A cloud-native monitoring service (GCP **Cloud Monitoring**; AWS **CloudWatch**; Azure **Monitor**) instruments
services out-of-the-box with default metrics, but custom application metrics (like the Prometheus ones above)
typically need a **sidecar container** pattern: one container runs the app and exposes `/metrics`, a second
collects from it and forwards to the monitoring backend. This is exactly the problem full container orchestration
(Kubernetes — see Module 5) solves natively; simpler managed services (GCP Cloud Run, AWS App Runner/Fargate, Azure
Container Apps) offer a lighter-weight sidecar feature to achieve the same without a full cluster.

**Service Level Objectives (SLOs)** — a defined target for how well the application should perform (e.g. 99% of
requests under 200ms) — set up per service in the monitoring console.

## Alert systems

The core tension in alerting is the **Goldilocks problem**: too many alerts causes alert fatigue (important ones get
ignored); too few means real problems go unnoticed. Setting up good alerting is often as hard as setting up the
metrics themselves.

Typical setup: notification channel (e.g. email) → alerting policy/condition (e.g. "cloud function invoked >N times
in period X") → attach the notification channel + human-readable documentation to the alert → trigger and confirm
delivery.

## Optimize and manage models at the edge (bullet from Module 9's own topic list)

> Both DTU source files below open with `!!! danger "Module is still under development"` — skeletons, copied in
> full, not condensed.

### Quantization (`s10_extra/quantization.md`)

Two strategies: **quantization-aware training** (model is trained knowing it will be quantized — generally yields
a better-performing quantized model, use when the deployment target has a hard size/speed constraint) vs.
**post-training quantization** (train normally, quantize after — simpler, use when raw performance matters most
and quantization is just a "nice to have" size/speed win).

```bash
pip install neural-compressor   # Intel's quantization toolkit
```

Core exercise DTU sketches: load a `float32` model checkpoint (ONNX or PyTorch Lightning), quantize it, then
compare file sizes — an `int4` quantized model should be close to **4x smaller** than `float32`, since it uses a
quarter of the bits per weight.

### Calibration (`s10_extra/calibration.md`)

An even thinner skeleton on DTU's side — just exercise stubs, no explanatory prose:

* Temperature scaling
* Label smoothing:

    ```python
    alpha = 0.1
    for i in range(len(y_true)):
        y_true[i] = (1 - alpha) * y_true[i] + alpha / num_classes
    ```

* Mixup, CutMix, Focal Loss
* Wiring calibration checks into a CI pipeline

Calibration (making a model's confidence scores match its actual accuracy) is conceptually adjacent to monitoring:
a well-calibrated model's confidence score is itself a useful signal for when to flag a prediction for human
review — worth drawing that connection explicitly when writing this section, since it's the "why does this belong
in a monitoring module" hook DTU's skeleton doesn't spell out.

**For this course's Module 9**: both quantization and calibration tie into "optimize and manage models at the edge"
— a smaller/faster/better-calibrated model is cheaper to keep redeploying through frequent retrain cycles, and its
confidence scores are more trustworthy as a monitoring signal in their own right.

## Common issues in ML model deployment / Feedback loop role (bullets from Module 9's topic list — no DTU coverage)

Write from scratch — likely candidates: training/serving skew, silent data pipeline failures upstream of the model,
missing rollback strategy when a new model version underperforms, and the feedback loop concept itself (production
outcomes feeding back into future training data — closely related to the CML material in
`week4_cicd_strategies.md`, Part 4, which is worth cross-linking here).

---

## Still to source for this module (no DTU equivalent — write from scratch)

* **AWS model monitoring** — SageMaker Model Monitor (data quality, model quality, bias drift, feature attribution
  drift monitors) — entirely new content
* **Azure model monitoring** — Azure ML's model monitoring / data collection + Application Insights — entirely new
  content
* Cross-cloud architecture comparison diagram for "the monitoring ecosystem in AWS/Azure/GCP" (this module's own
  stated topic) — a genuinely new deliverable, not adapted from DTU, best built as a single comparison table/diagram
  once the AWS/Azure sections above are written
* "Optimize and manage models at the edge" — see note above; would benefit from incorporating
  `s10_extra/quantization.md` and `calibration.md` once read (flagged in Supplementary)
