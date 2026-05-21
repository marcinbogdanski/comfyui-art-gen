# HunyuanImage 3

HunyuanImage 3 setup notes for `EricRollei/Comfy_HunyuanImage3` on the Vast RTX
PRO 6000 Blackwell instance.

## Custom Node

Installed by:

```text
scripts/setup_vast_extras.sh
```

The tested runtime pins are:

```text
transformers==4.57.1
huggingface-hub==0.36.0
bitsandbytes==0.48.2
```

The newer `transformers` / `bitsandbytes` combination initially installed on
the Vast image produced quantized-model failures.

## Model Files

Downloaded by:

```text
scripts/download_models/hunyuanimage3.sh
```

Tested workflow models:

```text
/workspace/ComfyUI/models/HunyuanImage-3-NF4-v2
/workspace/ComfyUI/models/HunyuanImage-3.0-Instruct-Distil-NF4-v2
```

The INT8 model folders are downloaded too, but they were not reliable in this
runtime and are not used by the checked-in workflows.

## Workflows

Repo copies:

```text
workflows/hunyuanimage3/hunyuanimage3_base_nf4.json
workflows/hunyuanimage3/hunyuanimage3_base_nf4.api.json
workflows/hunyuanimage3/hunyuanimage3_instruct_distil_nf4.json
workflows/hunyuanimage3/hunyuanimage3_instruct_distil_nf4.api.json
workflows/hunyuanimage3/hunyuanimage3_instruct_multifusion_nf4.json
workflows/hunyuanimage3/hunyuanimage3_instruct_multifusion_nf4.api.json
```

Important settings:

```text
Base NF4:              post_action=keep_loaded
Instruct-Distil NF4:   vae_tiling=on, vae_offload=on
Multi-fusion NF4:      blocks_to_swap=20, image 1 = source face/identity, image 2 = target pose/scene
Multi-fusion low VRAM: use the workflow note presets for 5090 / 3090 settings
```

`post_action=full_unload` made second base runs fail because ComfyUI reused the
cached loader output after the model had been cleared. Keeping the model loaded
is the better default for interactive prompt/seed iteration.

`vae_tiling=auto` / `vae_offload=auto` on Instruct-Distil can return a 64x64
black fallback image after VAE decode OOM. Force both settings to `on`.

## Low-VRAM Measurements

Measured on Vast instance `37076366`, RTX PRO 6000 Blackwell 96 GB, clean
ComfyUI process, two-reference Instruct-Distil NF4 multi-fusion at 1024x1024.

| Settings | blocks_to_swap | Comfy log allocation after load | Comfy log allocation before VAE decode | `nvidia-smi` peak | Post-run resident |
| --- | ---: | ---: | ---: | ---: | ---: |
| Default / RTX 6000 Pro Blackwell | 20 | 21.6 GB | 25.3 GB | 83.5 GiB | 22.5 GiB |
| Low-VRAM block swap | 31 | 7.2 GB | 11.2 GB | 69.1 GiB | 8.2 GiB |

The `nvidia-smi` peak is a conservative driver-level number with
`cudaMallocAsync`; it appears to include CUDA allocator pool reservation and is
much higher than the tensor allocation reported by the Hunyuan node logs. Use
the Comfy log allocation as the better first-pass signal for whether a smaller
GPU might fit, then verify on the actual target GPU.

Cropping/resizing both reference images to 1024x1024 before multi-fusion did not
materially reduce memory in this test (`nvidia-smi` peak about 69.7 GiB,
pre-VAE log allocation about 11.0 GB). It can still be useful for controlling
input semantics, but it is not a meaningful VRAM lever here.

### RTX 5090 Findings

Measured on Vast instance `37146497`, RTX 5090 32 GB, driver `570.211.01`,
PyTorch `2.9.1+cu128`, native allocator (`--disable-cuda-malloc`).

The `5090` workflow loaded successfully on the RTX 5090, but the unmodified
multi-fusion node failed before diffusion while VAE-encoding the conditional
reference images:

```text
CUDA OOM in autoencoder_kl_3d.py conv3d
Tried to allocate 27.00 GiB
```

Pre-resizing the ComfyUI input images to 1024, 768, or 512 did not help because
the upstream image processor snaps conditional VAE images back to native
`base_size=1024` buckets before encoding.

A remote-only custom-node experiment made 5090 generation work by forcing only
the conditional/reference VAE preprocessing to a smaller base size while leaving
the output resolution at 1024x1024:

```text
HUNYUAN_COND_VAE_BASE_SIZE=512
HUNYUAN_COND_VAE_BASE_SIZE=768 HUNYUAN_VAE_TILING=on PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
```

Results with two reference images, Instruct-Distil NF4, `blocks_to_swap=31`,
`bot_task=image`, output `1024x1024`:

| Conditional VAE base | Result | `nvidia-smi` peak | Runtime | Host RAM peak |
| ---: | --- | ---: | ---: | ---: |
| 1024 | OOM in ref VAE encode | 13.1 GiB sampled before failure | 5.7 s | 4.3 GiB |
| 512 | Success | 23.6 GiB | 85.9 s | 50.3 GiB |
| 768 + expandable segments + VAE tiling on | Success | 28.6 GiB | 93.0 s | 49.6 GiB |
| 768 + expandable segments + VAE tiling auto | Final VAE decode OOM; 64x64 fallback | 28.6 GiB | 87.0 s | 49.7 GiB |
| 768 without expandable segments | OOM in second ref VAE encode | 25.0 GiB sampled before failure | 8.3 s | 3.9 GiB |
| 832 + expandable segments | Failed tokenizer path | 7.8 GiB sampled before failure | 7.9 s | 3.8 GiB |

Interpretation: 5090 support is not settings-only with the upstream
`Comfy_HunyuanImage3` node. `blocks_to_swap=31` solves weight residency, but the
reference VAE encode still needs the local node patch. The patch exposes
`cond_vae_base_size`, `vae_tiling`, and `vae_offload` on the multi-fusion node.
`cond_vae_base_size=768` is the best 5090 result from this pass; it should
preserve more reference detail than 512, but it does change information flow
because fewer conditional VAE tokens are given to the network.

Node patch behavior:

- `cond_vae_base_size`: reference/conditional VAE preprocessing base size;
  default `1024` matches the native conditioning path; `0` disables the wrapper.
- `vae_tiling`: VAE decode tiling mode, `auto` / `on` / `off`.
- `vae_offload`: VAE decode offload mode, `auto` / `on` / `off`.
- Multi-fusion applies the memory-efficient MoE forward patch before generation.
- If `cond_vae_base_size > 0`, reference images use that VAE base size instead
  of the native VAE resolution group.

The low-VRAM node patch is captured in:

```bash
scripts/patch_hunyuanimage3_lowvram.sh
```

It has also been validated on replacement Vast RTX 5090 instance `37152517`
with driver `595.45.04`, PyTorch `2.9.1+cu130`, the same two-reference
workflow, and low-VRAM node inputs:

```text
cond_vae_base_size=768
vae_tiling=on
vae_offload=auto
```

The repo ComfyUI startup scripts now default `PYTORCH_CUDA_ALLOC_CONF` to
`expandable_segments:True`. Keep that allocator setting enabled for this 5090
path unless explicitly testing allocator behavior. Pair it with
`--disable-cuda-malloc` so ComfyUI uses PyTorch's allocator.

The tested 5090 low-VRAM preset is `cond_vae_base_size=768`, `vae_tiling=on`,
`vae_offload=auto`, and `blocks_to_swap=31`.

That preset produced a real 1024x1024 PNG, not the 64x64 fallback, with sampled
peak VRAM `29308 MiB` and submit-to-success time `125.8 s`.

### RTX 3090 Findings

Measured locally on `x399`, GPU 1, RTX 3090 24 GB, driver `580.126.09`,
Docker image `local/comfyui:cu130`, PyTorch `2.9.1+cu130`, ComfyUI `v0.20.1`,
with `--disable-cuda-malloc` and `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`.

The local Hunyuan custom node was installed under
`/mnt/data/comfyui/custom_nodes/Comfy_HunyuanImage3` at the pinned
`bf738dba3f542e6744c49bc29c29a20dd14d079d` ref and patched with:

```bash
COMFYUI_PATH=/mnt/data/comfyui scripts/patch_hunyuanimage3_lowvram.sh
```

Instruct-Distil NF4 multi-fusion works on the 3090 with:

```text
blocks_to_swap=31
cond_vae_base_size=512
vae_tiling=on
vae_offload=auto
```

Run results, `bot_task=image`, output `1024x1024`, 8
Distil steps:

| References | Conditional VAE base | Result | Sampled `nvidia-smi` peak | Submit-to-history time | Notes |
| ---: | ---: | --- | ---: | ---: | --- |
| 1 | 768 | Failed; 64x64 fallback | 9794 MiB | 19.2 s | OOM during conditional VAE encode, tried to allocate 14.65 GiB with 13.19 GiB free. |
| 1 | 640 | Failed; 64x64 fallback | 7696 MiB | 10.8 s | Tokenizer/template path failed with `'NoneType' object cannot be interpreted as an integer`. |
| 1 | 512 | Success; real 1024x1024 PNG | 16874 MiB | 272.8 s | Completed all 8 diffusion steps and tiled VAE decode. |
| 2 | 512 | Success; real 1024x1024 PNG | 16874 MiB | 241.0 s | Completed after reboot to driver `580.159.03`; all 8 diffusion steps and tiled VAE decode succeeded. |

Successful outputs:

```text
/mnt/data/comfyui/output/hunyuanimage3/instruct_single_reference_nf4_3090_cond512_00001_.png
/mnt/data/comfyui/output/hunyuanimage3/instruct_multifusion_nf4_3090_tworef_cond512_00001_.png
```

This establishes that local CUDA compatibility is good enough for the patched
single- and two-reference 3090 path at `cond_vae_base_size=512`. The next
quality frontier is testing whether a higher valid base such as `576` can
improve reference detail without triggering the tokenizer failure or
conditional VAE OOM.

## Operational Notes

HunyuanImage can leave large model state in VRAM after failed runs or after
switching between other big models. If errors are fixed by restart, that is the
expected current recovery path:

```bash
/workspace/art-gen-ctrl/scripts/start_vast_comfyui.sh
```

If ComfyUI is already running, stop it first with the PID in
`/workspace/comfyui.pid`, then start it again. A clean idle server should show
roughly `560 MiB` VRAM used.
