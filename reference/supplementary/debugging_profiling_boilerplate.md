# Supplementary — Debugging, Profiling, PyTorch Lightning boilerplate (not mapped to a specific week)

> Source: [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops) `s4_debugging_and_logging/debugging.md`,
> `profiling.md`, `boilerplate.md` (Apache 2.0), copied in full/condensed. None of this course's 10
> named modules mention debugging, profiling, or high-level training frameworks explicitly — filed here
> as optional/enrichment material. If time allows, the profiling content pairs naturally with Module 9
> (Monitoring/optimization) and the PyTorch Lightning content pairs naturally with Module 10 (AutoML/
> experiment tooling, alongside W&B — see `week11_automl_tools.md`).

---

## Part 1 — Debugging (`debugging.md`)

Debugging is hard to teach — it's a skill built through experience. `print()` statements work for small scripts but
don't scale. The Python built-in debugger (`pdb`) is worth knowing:

```python
import pdb
pdb.set_trace()   # drop into an interactive debugger at this line
```

Or via editor breakpoints (VS Code: `F9` for an inline breakpoint, then run in debug mode), or auto-launching the
debugger on an unhandled exception:

```bash
python -m pdb my_script.py
```

DTU's exercise: a buggy VAE script with four planted bugs (device mismatch, tensor shape mismatch, a math bug
around `log_var` vs. `var`, and a missing `optimizer.zero_grad()` causing gradient accumulation) — a good template
for a "find the bugs using a real debugger, not print statements" in-class exercise, regardless of what specific
model this course's own exercises end up using.

---

## Part 2 — Profiling (`profiling.md`)

!!! info "Core Module (on DTU's side)"

Profiling answers two questions: *how many times is each function called?* and *how long does each call take?* — the
first tells you what to prioritize optimizing (a function called 1000x more often than another, at similar per-call
cost, dominates total runtime); the second tells you which calls are expensive.

### `cProfile` (Python's built-in profiler)

```bash
python -m cProfile -s cumulative -o profile.txt myscript.py
```

```python
import pstats
p = pstats.Stats('profile.txt')
p.sort_stats('cumulative').print_stats(10)
```

`tottime` (time in the function itself) vs. `cumtime` (time including everything it calls) — `cumtime` ≥ `tottime`
always. [snakeviz](https://jiffyclub.github.io/snakeviz/) gives a visual flame-graph view of a `.prof` file.

A real optimization case DTU walks through: an MNIST dataset returning PIL images (converted via a `transforms.ToTensor()`
call on every `__getitem__`) turned out to already be tensor-backed internally — wrapping it in a plain
`TensorDataset` instead of re-converting per access eliminated redundant work entirely.

### PyTorch's built-in profiler (for GPU-mixed workloads)

```python
from torch.profiler import profile, ProfilerActivity

with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], record_shapes=True) as prof:
    model(inputs)

print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=10))
```

* Distinguishes kernel time (actual compute) from transfer time (`memcpy` between CPU/GPU) — a common
  "bottleneck" in ML code is data transfer, not compute.
* `prof.export_chrome_trace("trace.json")` → visualize at `chrome://tracing`.
* For multi-iteration profiling (a single forward pass is a noisy sample): call `prof.step()` per iteration inside
  the context, and view results in TensorBoard's profiler tab (`tensorboard --logdir=./log`), which supports diffing
  two runs against each other (e.g. comparing ResNet18 vs. ResNet34).

Beyond function-level profiling, [line_profiler/kernprof](https://github.com/pyutils/line_profiler) catches
single-line hotspots (e.g. an expensive non-sequential array index) that `cProfile` can't see; `py-spy` is another
solid open-source profiler for Python.

---

## Part 3 — Minimizing boilerplate with PyTorch Lightning (`boilerplate.md`)

Every ML project ends up with the same shape: model implementation (the actual research/dev focus) + training loop
boilerplate + saving/logging utilities (also boilerplate). High-level training frameworks
(fast.ai, Ignite, skorch, Catalyst, Composer, **PyTorch Lightning**) exist to eliminate the repeated boilerplate so
the model is the only thing that changes between projects.

### Core API: `LightningModule` + `Trainer`

```python
class MyModel(LightningModule):
    def training_step(self, batch, batch_idx):
        x, y = batch
        loss = self.criterion(self(x), y)
        self.log('train_loss', loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters())

trainer = Trainer(max_epochs=10)
trainer.fit(model)
```

* Data: either implement `train_dataloader`/`val_dataloader`/`test_dataloader` on the module, pass dataloaders
  directly to `trainer.fit(model, train_dl, val_dl)`, or (best for reuse across projects) package everything into a
  `LightningDataModule`.
* Callbacks — reusable cross-cutting behavior, e.g. `ModelCheckpoint` (save on metric improvement / keep best K) and
  `EarlyStopping` (stop training when a monitored metric plateaus):

    ```python
    trainer = Trainer(callbacks=[
        ModelCheckpoint(dirpath="./models", monitor="val_loss", mode="min"),
        EarlyStopping(monitor="val_loss", patience=3, mode="min"),
    ])
    ```

* Logging integrates directly with W&B (and many other trackers — see `week11_automl_tools.md`) via `self.log(...)`
  in the training step, plus `trainer = Trainer(logger=WandbLogger(project=...))` — non-scalar logging (images,
  histograms) still goes through `self.logger.experiment.log(...)`, i.e. the raw `wandb.log` API.
* GPU handling is automatic — no more manual `.to('cuda')` calls: `Trainer(accelerator="auto")` picks the best
  available device.
* Mixed-precision training (`float16`/`bfloat16` instead of `float32`) is a one-line flag
  (`Trainer(precision="16-mixed")`) — roughly halves memory usage with minimal accuracy impact, a good
  "free win" to teach alongside the ONNX/quantization content in `week8_deployment_fastapi_onnx.md` and
  `supplementary/scalable_applications.md`.
* Lightning CLI can replace both a hand-rolled CLI (Module 3's typer/invoke content) and a Hydra config setup
  (Module 2's reproducibility content) *if* a project is built Lightning-first — worth flagging as "pick one path,
  don't stack all three" rather than presenting them as always-complementary.

Adjacent Lightning-ecosystem packages worth a mention: `torchmetrics` (metrics library), `lightning-bolts`
(pretrained models/components for fast prototyping).
