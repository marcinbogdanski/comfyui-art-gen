# Flux.1 Schnell FP8

Working first-test model for this ComfyUI server.

Docs:

```text
https://docs.comfy.org/tutorials/flux/flux-1-text-to-image
```

Download the single-file FP8 checkpoint:

```bash
mkdir -p /mnt/data/comfyui/models/checkpoints

wget -c \
  -O /mnt/data/comfyui/models/checkpoints/flux1-schnell-fp8.safetensors \
  https://huggingface.co/Comfy-Org/flux1-schnell/resolve/main/flux1-schnell-fp8.safetensors
```

Workflow image used:

```text
https://raw.githubusercontent.com/Comfy-Org/example_workflows/main/flux/text-to-image/flux_schnell_fp8.png
```

Notes:

- Drag the workflow PNG onto the empty ComfyUI canvas.
- The workflow should load `flux1-schnell-fp8.safetensors` via `Load Checkpoint`.
- If ComfyUI asks for `v1-5-pruned-emaonly-fp16.safetensors`, the Flux workflow did not load and the default SD1.5 workflow is still active.
- Repeated runs vary unless the sampler seed behavior is set to fixed.
