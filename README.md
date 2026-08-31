# ComfyUI Server

Minimal Docker-based ComfyUI server for this headless GPU box.

## Build

The image pins ComfyUI `v0.29.0`.

```bash
docker build -t local/comfyui:cu130 .
```

## Run

```bash
./run_comfyui.sh
```

Data is stored under `/mnt/data/comfyui`.
The wrapper starts a detached container named `comfyui` on watercooled GPU 1.

## Access

```text
http://x399.lan:8188/
```

The wrapper sets `PYTORCH_CUDA_ALLOC_CONF` to
`expandable_segments:True` to reduce CUDA allocator fragmentation on large
ComfyUI workflows and starts ComfyUI with `--disable-cuda-malloc` so PyTorch's
allocator controls CUDA allocations.

## Post-rebuild smoke tests

Run the fast direct-API dependency suite against one ComfyUI instance:

```bash
python3 scripts/api_smoke_post_rebuild_models.py
```

The suite retains older locally useful models and covers the model/LoRA assets
used by the current workflow matrix. Each test generates exactly one small PNG
and validates that it is at least 256px, readable, and not black or constant.
Use `--list`, `--group legacy`, `--group matrix`, or `--only NAME ...` to inspect
or narrow the inventory.

This is deliberately separate from canonical workflow validation. When a
session adds or changes workflows, models, dependencies, or related runtime
behavior, establish a drift baseline by validating all GUI workflows through
the actual frontend conversion path, unless that complete matrix has already
passed in the current session against the same environment. Do not run this
baseline merely for questions, research, read-only review, or documentation-only
work:

```bash
python3 scripts/workflow_queue.py --prompt prompts/prompt1.md --dry-run
```

After that baseline, reuse its results and validate later changes in proportion
to their behavioral impact. Isolated workflow changes need targeted workflow
checks; documentation or metadata-only changes do not justify repeating the
full matrix.
