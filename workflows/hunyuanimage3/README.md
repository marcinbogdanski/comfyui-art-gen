# HunyuanImage 3 Examples

These workflows target the `EricRollei/Comfy_HunyuanImage3` custom nodes and
the pre-quantized NF4 checkpoints downloaded by
`scripts/download_models/hunyuanimage3.sh`.

The no-suffix `.json` files are GUI-loadable workflow examples. Matching
`.api.json` files are executable prompt graphs for `POST /prompt`.

Tested on the Vast RTX PRO 6000 Blackwell instance with:

- `transformers==4.57.1`
- `huggingface-hub==0.36.0`
- `bitsandbytes==0.48.2`

Operational notes:

- Base NF4 uses `post_action=keep_loaded`; `full_unload` can make second runs
  fail because ComfyUI reuses a cached loader output after the model was cleared.
- Instruct-Distil NF4 needs `vae_tiling=on` and `vae_offload=on`; `auto` can
  return a 64x64 black fallback image after VAE decode OOM.
- If Hunyuan errors appear after testing other large models, restart ComfyUI.
  The process can retain tens of GB of VRAM even when idle.
