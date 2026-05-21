# Model Summary

## Introduction

If model/LoRA page gets taken down we want enough to be able to load the model.
This repo is "what works for us", files in external "comfyui" folder are 
downloaded models/LoRAs but also our metadata.

For each model/LoRA in "comfyui" external folder we try to have three pieces:
- model/LoRA files, large binaries with actual weights
- a Markdown file describing where the file came from and how to use it,
  this is usually curated info from original source, like LoRA trigger words etc
- workflow image, or just workflow - raw source reference workflow

In this repo we track:
- our working workflow, where possible a minimally modified source workflow

## Downloaded Models

**FLUX.2 Klein 9B**
Main models:
- `diffusion_models/bigLove_klein2_bf16_pruned.safetensors` - 17 GB - ok
- `diffusion_models/bigLove_klein2_fp8_pruned.safetensors` - 8.5 GB - not used

LoRAs:
- `loras/FLUX2_KLEIN_UNLOCKED_V1.safetensors` - 317 MB - image w/o workflow
- `loras/klein_snofs_v1_4.safetensors` - 1.1 GB - ok

**FLUX.2 Dev**
Main models:
- `diffusion_models/flux2_dev_fp8mixed.safetensors` - 34 GB - ok

**FLUX.1**
Main models:
- `checkpoints/flux1-schnell-fp8.safetensors` - 17 GB - ok
- `checkpoints/fluxedUpFluxNSFW_100BF16.safetensors` - 23 GB - ok

**Z-Image Turbo**
Main models:
- `diffusion_models/z_image_turbo_bf16.safetensors` - 12 GB - json workflow

LoRAs:
- `loras/Civit_Art_V1T1_E11.safetensors` - 163 MB - workflow from image not tested
- `loras/Shizuka_E10.safetensors` - 163 MB - workflow from image not tested

**Wan 2.2 / WanVideo**
Main models:
- `diffusion_models/WanVideo/2_2/Wan2_2-I2V-A14B-HIGH_fp8_e4m3fn_scaled_KJ.safetensors` - 14 GB - json workflow
- `diffusion_models/WanVideo/2_2/Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors` - 14 GB - use HIGH workflow
- `diffusion_models/WanVideo/2_2/wan2.2_ti2v_5B_fp16.safetensors` - 9.4 GB - workflow not tested

LoRAs:
- `loras/WanVideo/Lightx2v/lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors` - 704 MB - use HIGH workflow
- `loras/Pronebone_high_noise.safetensors` - 293 MB - use HIGH workflow

**HunyuanImage 3.0**
Main models:
- `HunyuanImage-3.0-Instruct-Distil-NF4-v2/` - 48 GB sharded model directory - see HunyuanImage-3.0-Instruct-Distil-NF4-v2.md

**Pony / SDXL**
Main models:
- `checkpoints/ponyDiffusionV6XL_v6StartWithThisOne.safetensors` - 6.5 GB
- `checkpoints/cyberrealisticPony_v180Coreshift.safetensors` - 6.5 GB - md, image w/o workflow, repo workflow
- `checkpoints/cyberrealisticPony_v180Coreshift_fp32.safetensors` - 13 GB - same md

**Qwen3.5 LLM**
Main models:
- `LLM/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf` - 20 GB - md, our workflow
