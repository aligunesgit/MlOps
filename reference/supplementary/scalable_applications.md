# Supplementary — Scalable Applications: distributed data loading, distributed training, scalable inference

> Source: [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) `s9_scalable_applications/data_loading.md`,
> `distributed_training.md`, `inference.md` (Apache 2.0), copied in full/condensed. This whole DTU
> session has no equivalent in this course's 10-module list — filed here as optional/enrichment. The
> inference-optimization sub-topics (quantization, pruning) directly overlap with `week10_model_monitoring.md`'s
> "optimize and manage models at the edge" bullet — worth cross-referencing rather than duplicating if this
> content gets used.

---

## Part 1 — Distributed data loading (`data_loading.md`)

!!! info "Core Module (on DTU's side)"

Deep learning is unusual among ML approaches in that more data essentially always helps (traditional ML like
random forests/SVMs plateaus). This makes the data pipeline itself a potential bottleneck: if the GPU sits idle
waiting for data, that's wasted (and, in the cloud, billed) compute.

PyTorch parallelizes data loading across CPU worker threads via `DataLoader(num_workers=N)`:

```python
dataloader = DataLoader(dataset, batch_size=8, num_workers=4)
```

Mechanically: the main thread distributes the requested batch's indices across `N` worker threads, each calls
`__getitem__` for its share, then results are collected back on the main thread. Each of those hand-offs is a real
communication cost — **multiprocessing only pays off when `__getitem__` itself is expensive** (e.g. reading a file
from disk); for data that's already in memory, the parallelization overhead can exceed the savings.

Practical exercise DTU walks through: benchmark load time vs. `num_workers` on a dataset that loads raw JPEGs from
disk at runtime (rather than pre-loaded tensors) — the benefit of parallel workers only becomes visible once
per-item work (I/O + augmentation) is heavy enough to amortize the worker hand-off cost. `pin_memory=True` speeds
up the CPU→GPU transfer specifically when the whole dataset fits in GPU memory.

---

## Part 2 — Distributed training (`distributed_training.md`)

Training frontier models is fundamentally impossible on a single device within a reasonable timeframe (DTU's
example: AlphaFold trained on the equivalent of 100–200 modern GPUs for weeks — single-GPU would take years).
Three paradigms, in order of sophistication: **Data Parallel (DP)** → **Distributed Data Parallel (DDP)** →
**sharded training** (not covered in depth by DTU, but flagged as the newest approach, capable of ~60% memory
savings — worth a pointer to for a "what's next" close to this topic).

### Data Parallel (DP) — simplest, now considered obsolete, but instructive

Each forward pass: split the batch across `M` devices → replicate the model to each device → parallel forward →
gather outputs back to the primary device. Backward: compute loss on the primary device → scatter gradients →
parallel backward → reduce (sum) gradients back on the primary device.

```python
model = nn.DataParallel(model, device_ids=[0, 1])
preds = model(input)   # otherwise identical usage
```

Core problem: the model gets **re-replicated every single step** (destroyed after each backward pass), so DP pays
a large communication cost repeatedly — `3×M` communication calls per step. This is why it's considered obsolete.

### Distributed Data Parallel (DDP) — the practical default

Key difference: the model is replicated **once**, and the *gradient update* itself happens in parallel on each
device — no per-step re-replication. Steps: initialize a model copy per device → load non-overlapping data shards
into page-locked host memory per device → parallel forward → **all-reduce** the gradients (an all-to-all operation
— every process sends its gradient to every other process and receives theirs back) → each device updates its own
model copy using the reduced gradient (all copies stay in sync since they all received identical gradient info).

Only **one** communication call per step (the all-reduce) instead of DP's `3×M` — empirically 2-3x faster than DP,
though implementing raw DDP is significantly more involved than DP's one-line wrapper. In practice, **PyTorch
Lightning abstracts this almost entirely away** — flip two `Trainer` flags (`accelerator`, `devices`) and multi-GPU
training just works, no manual DDP wiring needed (see `supplementary/debugging_profiling_boilerplate.md`, Part 3).

Note: a 2x speedup from 2 GPUs is not actually achievable in practice — communication overhead means real-world
scaling is always sub-linear, worth setting that expectation explicitly when teaching this.

---

## Part 3 — Scalable inference (`inference.md`)

Inference scaling is a fundamentally different problem from training scaling: usually one data point at a time,
often on edge devices or cheap/low-compute cloud tiers — you can't just throw more GPUs at it. The lever instead is
making the *model itself* smaller/faster.

### Architecture choice matters as much as parameter count

Different base architectures at the *same* parameter count have meaningfully different inference speed — DTU cites
benchmark data showing convolutional architectures are generally more throughput-efficient than transformer (ViT)
architectures at equal parameter budgets. **FLOPs** (floating point operations) is the standard way to quantify
this independent of hardware, measurable via the `ptflops` package. Practical exercise: benchmark
EfficientNet/ResNet/Swin-Transformer variants at similar parameter counts and correlate wall-clock inference time
with FLOP count and reported ImageNet accuracy — the actual "which model would you ship" decision is a genuine
three-way trade-off (accuracy vs. speed vs. FLOPs), not just "pick the most accurate one."

### Quantization

Convert `float32` computation to lower-precision integers (commonly `int8`). Why it helps: integer ops are faster
than float ops; modern hardware has specialized integer-op silicon; **many models are memory-bandwidth-bound, not
compute-bound** — 8-bit data moves ~4x faster than 32-bit; and quantized checkpoints are ~75% smaller on disk,
directly shrinking Docker image size for deployment (ties directly to the ONNX/BentoML deployment content in
`week8_deployment_fastapi_onnx.md` and the edge-optimization bullet in `week10_model_monitoring.md`).

Linear affine quantization: $x_{int} = \text{round}(x_{float}/s + z)$ where $s$ is a scale, $z$ a zero-point.
Rounding errors don't compound catastrophically in practice — DTU points at the central limit theorem as the
mathematical reason many small independent rounding errors tend to average out rather than accumulate.

```python
q = torch.quantize_per_tensor(tensor, scale=..., zero_point=..., dtype=torch.qint8)
q.dequantize()   # back to float, for sanity-checking how much was lost
```

### Pruning

Zero out weights below some importance threshold (commonly: magnitude — small weights contribute small activations
downstream). PyTorch's `torch.nn.utils.prune` module supports both **local** pruning (per-layer, independently —
risks over-pruning some layers relative to others) and **global** pruning (prune the smallest X% of weights across
the *whole* network at once — the more sensible default).

```python
prune.global_unstructured(parameters_to_prune, pruning_method=prune.L1Unstructured, amount=0.2)
```

**Important caveat worth teaching explicitly**: pruning alone does **not** guarantee a smaller file or faster
inference — PyTorch's dense tensor ops don't exploit sparsity by default. To actually realize savings, pruned
weights need explicit conversion to a sparse format (`.to_sparse()`) before saving, and even then, whether inference
speeds up depends on the sparsity *structure*, not just the sparsity *level*. This is a common student
misconception worth heading off directly.

### Knowledge distillation

Train a smaller "student" model to mimic a larger "teacher" model's *softmax output distribution* (not just its
hard labels) — the teacher's distribution encodes inter-class relationships the student doesn't need the same
capacity to learn from scratch. Canonical example: DistilBERT — 97% of BERT's performance at 40% of the parameters
and 60% faster inference.

```python
loss = cross_entropy(preds, target) + cross_entropy(preds, teacher_logits)
```

This module ends DTU's course content chain on model-size/speed optimization — natural closing note for this
course's own Module 9/10 material: architecture choice, quantization, pruning, and distillation are four
*independent, combinable* levers for the same underlying goal (cheaper/faster inference), not a menu to pick
exactly one from.
