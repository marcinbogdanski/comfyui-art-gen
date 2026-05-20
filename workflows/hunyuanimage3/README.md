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
- Instruct-Distil multi-fusion uses image 1 as the source face/identity and
  image 2 as the target pose/scene. It uses loader `blocks_to_swap=20` to leave
  enough VRAM for decode. Replace the two `LoadImage` inputs in the GUI before
  running.
- The `5090` multi-fusion variant is an aggressive low-VRAM experiment for
  the same two-reference Instruct-Distil NF4 use case. It keeps only one
  transformer block resident on GPU and swaps the rest from CPU. Quality should
  match the standard multi-fusion variant apart from normal execution-order floating point
  noise, but it is slower.
- On an RTX 5090, the `5090` workflow alone is not enough for two-reference
  Instruct-Distil multi-fusion. The current custom node still VAE-encodes
  reference images at native conditional `base_size=1024`, which OOMs before
  diffusion. Run `scripts/patch_hunyuanimage3_lowvram.sh` after installing
  `Comfy_HunyuanImage3`. The `5090` workflow sets the added multi-fusion node
  inputs `cond_vae_base_size=768`, `vae_tiling=on`, and `vae_offload=auto`.
  The repo startup scripts default `PYTORCH_CUDA_ALLOC_CONF` to
  `expandable_segments:True`; keep that allocator setting enabled for the 5090
  path.
- If Hunyuan errors appear after testing other large models, restart ComfyUI.
  The process can retain tens of GB of VRAM even when idle.
