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
workflows/hunyuanimage3/hunyuanimage3_instruct_multifusion_nf4_5090.json
workflows/hunyuanimage3/hunyuanimage3_instruct_multifusion_nf4_5090.api.json
```

Important settings:

```text
Base NF4:              post_action=keep_loaded
Instruct-Distil NF4:   vae_tiling=on, vae_offload=on
Multi-fusion NF4:      blocks_to_swap=20, image 1 = source face/identity, image 2 = target pose/scene
Multi-fusion 5090:    RTX 5090 low-VRAM variant of the same two-reference use case, using blocks_to_swap=31
```

`post_action=full_unload` made second base runs fail because ComfyUI reused the
cached loader output after the model had been cleared. Keeping the model loaded
is the better default for interactive prompt/seed iteration.

`vae_tiling=auto` / `vae_offload=auto` on Instruct-Distil can return a 64x64
black fallback image after VAE decode OOM. Force both settings to `on`.

## Low-VRAM Measurements

Measured on Vast instance `37076366`, RTX PRO 6000 Blackwell 96 GB, clean
ComfyUI process, two-reference Instruct-Distil NF4 multi-fusion at 1024x1024.

| Workflow | blocks_to_swap | Comfy log allocation after load | Comfy log allocation before VAE decode | `nvidia-smi` peak | Post-run resident |
| --- | ---: | ---: | ---: | ---: | ---: |
| `hunyuanimage3_instruct_multifusion_nf4` | 20 | 21.6 GB | 25.3 GB | 83.5 GiB | 22.5 GiB |
| `hunyuanimage3_instruct_multifusion_nf4_5090` | 31 | 7.2 GB | 11.2 GB | 69.1 GiB | 8.2 GiB |

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
`Comfy_HunyuanImage3` node. The `5090` workflow solves weight residency, but the reference
VAE encode still needs the local node patch. The patch exposes
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

The current `5090` workflow defaults are `cond_vae_base_size=768`,
`vae_tiling=on`, `vae_offload=auto`, and seed `0`.

That run produced a real 1024x1024 PNG, not the 64x64 fallback, with sampled
peak VRAM `29308 MiB` and submit-to-success time `125.8 s`.

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
