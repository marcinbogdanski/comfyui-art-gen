# Model Download Scripts

These scripts are intentionally simple command references for the model files
used by the checked-in workflows. They default to a Vast-style ComfyUI path at
`/workspace/ComfyUI`. Override `COMFYUI_MODELS_DIR` for local x399 downloads:

```bash
COMFYUI_MODELS_DIR=/mnt/data/comfyui/models scripts/download_models/z-image-turbo.sh
```

Run one script at a time:

```bash
scripts/download_models/z-image-turbo.sh
scripts/download_models/z-image-base.sh
scripts/download_models/qwen-image-2512.sh
scripts/download_models/qwen-image-edit-2511.sh
scripts/download_models/hunyuanimage3.sh
scripts/download_models/qwen3.5-35b-a3b.sh
scripts/download_models/flux2-klein-nsfw.sh
```

The FLUX.2 Klein 9B script requires an accepted Black Forest Labs Hugging Face
agreement and an HF token:

```bash
HF_TOKEN=... scripts/download_models/flux2-klein-9b.sh
```

The Civitai scripts require a token:

```bash
CIVITAI_API_KEY=... scripts/download_models/cyberrealistic-pony.sh
CIVITAI_API_KEY=... scripts/download_models/fluxed-up.sh
CIVITAI_API_KEY=... scripts/download_models/flux2-klein-nsfw.sh
```
