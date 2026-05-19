# Model Download Scripts

These scripts are intentionally simple command references for the model files
used by the checked-in workflows. They assume ComfyUI lives at
`/workspace/ComfyUI` on the Vast instance.

Run one script at a time:

```bash
scripts/download_models/z-image-turbo.sh
scripts/download_models/hunyuanimage3.sh
```

The Civitai scripts require a token:

```bash
CIVITAI_API_KEY=... scripts/download_models/cyberrealistic-pony.sh
CIVITAI_API_KEY=... scripts/download_models/fluxed-up.sh
```
