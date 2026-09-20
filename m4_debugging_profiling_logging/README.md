# Module 4: Debugging, Profiling and Logging

Week 4

## Learning objectives

* Be able to debug a Python script with a real debugger instead of `print` statements
* Be able to profile a script to find out what it actually spends time on, not what you assume it does
* Be able to log experiments to Weights & Biases so a run's metrics, config, and environment are all
  recorded together
* Understand what a high-level training framework like PyTorch Lightning removes from a project

---

## 1. Debugging without print statements

`print()` works for a five-line script, but it stops scaling the moment a bug hides inside a training
loop that takes minutes to reach the failing line. Python's built-in debugger, `pdb`, drops you into an
interactive session at the exact point something goes wrong, so you can inspect variables live instead
of guessing which `print` to add next:

```python
import pdb
pdb.set_trace()   # execution pauses here; inspect variables interactively
```

```bash
python -m pdb my_script.py   # launches the whole script under the debugger
```

VS Code wraps the same mechanism behind a UI: press `F9` on a line to set a breakpoint, then run the
file in debug mode (the bug icon in the sidebar) instead of the normal run button. Either way, the
debugger can also auto-launch on an unhandled exception, dropping you exactly where the script died
rather than at the top.

A useful category of bug worth training your eye on, since each one produces a different kind of wrong
answer rather than a crash:

| Bug category | Symptom |
|---|---|
| Device mismatch | A tensor on CPU meets a tensor on GPU; PyTorch raises a runtime error naming both devices |
| Tensor shape mismatch | A matrix multiply or concatenation silently broadcasts wrong, or crashes with a shape error |
| A formula bug (e.g. confusing `log_var` with `var`) | The script runs to completion, but the loss or output is subtly, quietly wrong |
| Missing `optimizer.zero_grad()` | Gradients accumulate across batches instead of resetting; training slowly diverges rather than crashing |

The last two are the dangerous ones: nothing crashes, so the only sign is a model that trains worse than
it should. Stepping through the training loop with `pdb` and checking a tensor's actual values at each
line is how you catch what a stack trace never will.

## 2. Profiling: measure before you optimize

Profiling answers two questions: how many times is each function called, and how long does each call
take. The first tells you what to prioritize (a function called a thousand times more often than
another, at similar per-call cost, dominates total runtime); the second tells you which calls are
actually expensive. Guessing at either without measuring is how people optimize the wrong function.

```bash
python -m cProfile -s cumulative -o profile.txt myscript.py
```

```python
import pstats
p = pstats.Stats("profile.txt")
p.sort_stats("cumulative").print_stats(10)
```

Two numbers matter per function: `tottime` (time spent in the function itself) and `cumtime` (time
spent in it plus everything it calls). `cumtime` is always at least `tottime`, and a large gap between
them means the real cost lives further down the call stack.
[snakeviz](https://jiffyclub.github.io/snakeviz/) turns a saved `.prof` file into a visual flame graph,
which makes spotting that gap much faster than reading a table.

A realistic example of what profiling actually catches: a dataset's `__getitem__` calling
`transforms.ToTensor()` on every access, converting a PIL image to a tensor each time, when the
underlying data was already tensor-backed. Wrapping it in a plain `TensorDataset` instead of
re-converting on every access eliminated that redundant work entirely, something no amount of staring
at the code would have surfaced as clearly as a profile did.

## 3. Profiling GPU-mixed workloads

`cProfile` only sees Python-level calls; it can't tell you how much of a `model(inputs)` call was
actual GPU compute versus time spent moving tensors between CPU and GPU. PyTorch's own profiler can:

```python
from torch.profiler import profile, ProfilerActivity

with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], record_shapes=True) as prof:
    model(inputs)

print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=10))
```

This distinguishes kernel time (actual compute) from transfer time (`memcpy` between CPU and GPU), and
a data-transfer bottleneck disguised as a "slow model" is a common enough finding that it's worth
checking for directly rather than assuming the model itself is the problem. `prof.export_chrome_trace
("trace.json")` produces a trace viewable at `chrome://tracing`; for multi-iteration profiling (a
single forward pass is a noisy sample on its own), calling `prof.step()` once per iteration inside the
context lets you view results in TensorBoard's profiler tab instead, which also supports diffing two
runs against each other.

Beyond function-level profiling, [line_profiler](https://github.com/pyutils/line_profiler) catches a
single expensive line inside an otherwise-fast function (an inefficient array index, say) that
`cProfile`'s function-level granularity can't see; `py-spy` is another solid standalone Python profiler
worth knowing exists.

## 4. Logging experiments with Weights & Biases

Once a script is debugged and profiled, the next problem is remembering what you actually ran. Writing
loss values to a text file works for one run; it stops working the moment you're comparing many runs,
or collaborating with teammates on the same project. **Weights & Biases (W&B)** is one standard answer
(Comet, Neptune, and the open-source MLflow are the same idea from different vendors):

```bash
pip install wandb
wandb login   # paste the API key from wandb.ai
```

```python
import wandb

wandb.init(project="my_project", entity="my_entity", job_type="train", config=hyperparams)
wandb.log({"train_loss": loss, "train_acc": acc})
wandb.log({"input_images": wandb.Image(batch)})  # images, histograms, and figures work too
```

* `project` groups every run from one experiment line together, shared across a team.
* `entity` is the owning user or team, shared across group members for a class project.
* `job_type` distinguishes different scripts logging to the same project (`"train"` versus
  `"evaluate"`) for dashboard filtering.

**The reproducibility payoff** is what makes this more than a nicer chart: every run's page
automatically records the exact git commit, the exact launch command, and a full dependency snapshot.
Reproducing a run becomes clone, checkout that commit, install from the snapshot, re-run the logged
command, exactly the problem Module 3's Hydra config output directories solve for hyperparameters,
applied here to the whole run.

**Model registry.** A trained model gets logged as a versioned, immutable **artifact**, then linked
into a **model registry** with an **alias** (`latest`, `staging`, `production`) marking where it sits
in the promotion path:

```python
run.link_artifact(artifact=artifact, target_path="model-registry/my-model", aliases=["staging"])
```

This alias mechanism is exactly what Module 5's Continuous Machine Learning material hooks into: a
webhook fires when an alias changes to `staging`, runs performance tests, and only flips it to
`production` once they pass. W&B also ships built-in hyperparameter sweeps as a lighter-weight
alternative to Optuna; Module 10 covers the more general-purpose hyperparameter optimization workflow
in depth.

Authenticating inside a training container (for a job running in CI or the cloud rather than on your
own machine) is one environment variable:

```bash
docker run -e WANDB_API_KEY=<your-api-key> my_training_image:latest
```

## 5. Minimizing boilerplate with PyTorch Lightning

Every ML project ends up with the same shape: the model itself (the part that actually differs between
projects), plus training-loop boilerplate and saving/logging utilities that look nearly identical
across all of them. High-level training frameworks (fast.ai, Ignite, **PyTorch Lightning** among
others) exist specifically to eliminate that repeated boilerplate:

```python
class MyModel(LightningModule):
    def training_step(self, batch, batch_idx):
        x, y = batch
        loss = self.criterion(self(x), y)
        self.log("train_loss", loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters())

trainer = Trainer(max_epochs=10)
trainer.fit(model)
```

* **Callbacks** are reusable, cross-cutting behavior attached to the `Trainer` rather than written into
  the training loop by hand: `ModelCheckpoint` saves on metric improvement, `EarlyStopping` halts
  training once a monitored metric plateaus.
* **Logging** integrates with W&B directly through `self.log(...)` inside `training_step`, plus
  `Trainer(logger=WandbLogger(project=...))`; non-scalar logging (images, histograms) still goes
  through the raw `wandb.log` API via `self.logger.experiment.log(...)`.
* **GPU handling is automatic.** `Trainer(accelerator="auto")` picks the best available device, no
  manual `.to("cuda")` calls scattered through the code.
* **Mixed-precision training** (`Trainer(precision="16-mixed")`) is a one-line flag that roughly halves
  memory usage with minimal accuracy impact, a genuinely free win worth turning on by default once a
  training loop already works, and directly relevant once Module 9 covers scaling training further.

Lightning's own CLI can replace a hand-rolled `typer`/`invoke` CLI (Module 2) and a Hydra config setup
(Module 3) at the same time, if a project is built Lightning-first from day one. That's a reason to
pick one path deliberately rather than stacking all three frameworks on top of each other for the same
job.

## 6. Project: profile and log a training run (required)

Take a training script from an earlier module's exercises. Profile it with `cProfile`, identify the
single largest `cumtime` contributor, and fix it (a redundant computation, an unnecessary data
conversion, a data-transfer bottleneck if it's GPU-bound). Then wire the same script to log to Weights
& Biases: at minimum, the hyperparameters as `config`, and training/validation loss per epoch. Confirm
the W&B run page shows the exact git commit the run was made from, and report the before/after runtime
change your profiling fix produced.

---

## Summary

A bug that doesn't crash is more dangerous than one that does, which is why stepping through a training
loop with a real debugger (§1) beats guessing with `print`. Profiling (§2-§3) replaces intuition about
what's slow with a measurement of what actually is, and logging (§4) is what turns "I think it worked
better this time" into a comparable, reproducible record. PyTorch Lightning (§5) is what all four of
those add up to once a project outgrows hand-rolled boilerplate: debugging, profiling, and logging
built into the training loop itself rather than bolted on separately.

## Further reading

* See the [Course books](../README.md#course-books) for deeper dives on applied ML engineering and
  production reliability.

## References

Foundational sources this module's content draws on:

* SkafteNicki, Nicki, et al. [`dtu_mlops`](https://github.com/SkafteNicki/dtu_mlops),
  `s4_debugging_and_logging/` (`debugging.md`, `profiling.md`, `boilerplate.md`) and
  `s4_debugging_and_logging/logging.md`. DTU course 02476, Apache 2.0 licensed. Primary source material
  this module's debugging, profiling, W&B logging, and Lightning content is adapted from.
* Python Software Foundation. [`pdb` documentation](https://docs.python.org/3/library/pdb.html) and
  [`cProfile` documentation](https://docs.python.org/3/library/profile.html). Source for the debugger
  and profiler mechanics in §1-§2.
* PyTorch Documentation. [PyTorch Profiler recipe](https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html).
  Source for the GPU/CPU activity profiling in §3.
* [Weights & Biases documentation](https://docs.wandb.ai/). Source for the experiment logging and
  model registry mechanics in §4.
* [PyTorch Lightning documentation](https://lightning.ai/docs/pytorch/stable/). Source for the
  `LightningModule`/`Trainer` API in §5.
