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
scripts/download_models/hunyuanimage3.sh
scripts/download_models/qwen3.5-35b-a3b.sh
```

The Civitai scripts require a token:

```bash
CIVITAI_API_KEY=... scripts/download_models/cyberrealistic-pony.sh
CIVITAI_API_KEY=... scripts/download_models/fluxed-up.sh
```
