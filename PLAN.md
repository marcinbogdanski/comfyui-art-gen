# Modern Original ComfyUI Model Set Plan

## Goal

Build a complete local baseline set of six modern original ComfyUI image model
families, all using official/recommended `.safetensors` files where available
and official ComfyUI workflows.

Target set:

- FLUX.2 Dev
- FLUX.2 Klein 9B
- Qwen-Image 2512
- Qwen-Image-Edit 2511
- Z-Image Turbo
- Z-Image Base

Current known local coverage:

- FLUX.2 Dev: model and official ComfyUI workflow already present.
- Z-Image Turbo: model and official ComfyUI workflow already present.
- FLUX.2 Klein 9B: missing official/original model and official workflow.
- Qwen-Image 2512: missing model and official workflow.
- Qwen-Image-Edit 2511: missing model and official workflow.
- Z-Image Base: local GGUF quant exists, but canonical original safetensors
  model and official workflow are missing.

## Required Sources

Use official ComfyUI documentation/templates as the workflow source of truth.
Use Comfy-Org Hugging Face split/repack repositories when the ComfyUI docs
recommend them, and document upstream official model repositories too.

Expected ComfyUI docs:

- `https://docs.comfy.org/tutorials/flux/flux-2-dev`
- `https://docs.comfy.org/tutorials/flux/flux-2-klein`
- `https://docs.comfy.org/tutorials/image/qwen/qwen-image-2512`
- `https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit-2511`
- `https://docs.comfy.org/tutorials/image/z-image/z-image-turbo`
- `https://docs.comfy.org/tutorials/image/z-image/z-image`

Expected upstream official model repositories:

- `https://huggingface.co/black-forest-labs/FLUX.2-dev`
- `https://huggingface.co/black-forest-labs/FLUX.2-klein-9B`
- `https://huggingface.co/Qwen/Qwen-Image-2512`
- `https://huggingface.co/Qwen/Qwen-Image-Edit-2511`
- `https://huggingface.co/Tongyi-MAI/Z-Image-Turbo`
- `https://huggingface.co/Tongyi-MAI/Z-Image`

The Hugging Face API token should be available from the user's shell startup
files. The FLUX.2 Klein 9B BFL agreement has been accepted by the user.

## Repository Layout

Use the existing family/variant/source layout.

Models docs:

- `models/flux-2/dev/original/`
- `models/flux-2/klein/original/`
- `models/qwen-image/2512/original/`
- `models/qwen-image/2511-edit/original/`
- `models/z-image/turbo/original/`
- `models/z-image/base/original/`

Workflows:

- `workflows/flux-2/dev/original/`
- `workflows/flux-2/klein/original/`
- `workflows/qwen-image/2512/original/`
- `workflows/qwen-image/2511-edit/original/`
- `workflows/z-image/turbo/original/`
- `workflows/z-image/base/original/`

Do not count local `.my.json`, `.my.work.json`, or `.work.json` files as
official/original workflows. They can be ignored for this goal.

## Model Archive Requirements

Before creating, renaming, or cleaning sidecar/reference files under
`/mnt/data/comfyui/models`, read:

```text
/mnt/data/comfyui/models/MODEL_SUMMARY_RULES.md
```

Then maintain the external model archive consistently:

- Keep actual weights out of git.
- Add/update Markdown sidecars and raw source captures as required by the
  model archive rules.
- Update `/mnt/data/comfyui/models/MODEL_SUMMARY.md` if the high-level coverage
  changes.
- Preserve source URLs, hashes, file sizes, workflow source links, and local
  filenames.

## Download And Documentation Work

For each missing original model:

1. Confirm the current ComfyUI docs page and recommended filenames.
2. Download the recommended `.safetensors` files into
   `/mnt/data/comfyui/models/...`.
3. Download or save the official ComfyUI workflow/template into the matching
   `workflows/.../original/` folder.
4. Add or update the matching repo model doc under `models/.../original/`.
5. Add or update any `scripts/download_models/*.sh` script needed for repeatable
   setup.
6. Add or update model-archive sidecars under `/mnt/data/comfyui/models`
   according to `MODEL_SUMMARY_RULES.md`.

For already-present FLUX.2 Dev and Z-Image Turbo:

1. Verify the model files still match the official ComfyUI docs.
2. Verify repo docs and model archive sidecars point at current source URLs.
3. Verify the official workflow files are still in the right `original/`
   folders.

## Runtime And Validation

All six original models must be API smoke tested in local ComfyUI.

Smoke-test requirements:

- Use the local Docker ComfyUI wrapper and existing operational preferences.
- Start/restart ComfyUI if needed. This machine is available for the task.
- The default URL is `http://x399.lan:8188/`.
- It is acceptable to restart the `comfyui` container when models leave stale
  VRAM state or when a clean process is useful.
- Keep tests small and practical for a 24 GB GPU where possible.
- Record whether each smoke test produced a real image and where the output was
  saved.
- If a model cannot fit locally, record the exact failure and whether the model
  was still downloaded and documented.

ComfyUI operational constraints:

- Use `./run_comfyui.sh`; do not introduce Docker Compose.
- Do not install CUDA Toolkit, PyTorch, ComfyUI, or model dependencies on the
  host.
- Persistent ComfyUI data lives under `/mnt/data/comfyui`.
- Do not expose ComfyUI directly to the public internet.
- Start with one GPU per ComfyUI instance. The local wrapper uses watercooled
  GPU 1 for ComfyUI.

## Git And Commit Policy

Do not commit as you go.

Work in checkpoints and keep the working tree reviewable. Stage only when a
coherent set of files is ready for review, and ask before committing unless the
user explicitly requests a commit.

Expected final staged/committable areas may include:

- `PLAN.md` if it is still useful to keep.
- `models/...`
- `workflows/...`
- `scripts/download_models/...`
- `/mnt/data/comfyui/models` model-archive docs/sidecars in its separate git
  repository.

## Stopping Condition

Stop when all six target model families have:

- recommended original `.safetensors` files present locally, or a documented
  blocker;
- official ComfyUI workflow present locally, or a documented blocker;
- repo model/download documentation updated;
- model-archive sidecars and high-level summary updated where needed;
- an API smoke-test result recorded.

If blocked, stop with concrete file/model/source names, the command that failed,
the exact error, and the next recommended action.
