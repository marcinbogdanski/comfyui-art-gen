# Krea 2

Local Krea 2 RAW, Turbo, community-checkpoint, and LoRA references for ComfyUI.

## Official Sources

- ComfyUI tutorial and Turbo template:
  https://docs.comfy.org/tutorials/image/krea/krea-2
- Official Comfy-Org split files:
  https://huggingface.co/Comfy-Org/Krea-2/tree/952f49d49653cb42e7d6cf7cbfad74738073ec7d
- Krea 2 RAW upstream:
  https://huggingface.co/krea/Krea-2-Raw

The download script pins the Comfy-Org revision and verifies every file by
SHA-256:

```bash
CIVITAI_API_KEY=... \
  COMFYUI_MODELS_DIR=/mnt/data/comfyui/models \
  scripts/download_models/krea2.sh
```

## Local Inventory

Shared support files:

```text
text_encoders/qwen3vl_4b_fp8_scaled.safetensors
text_encoders/qwen3vl_4b_bf16.safetensors
vae/qwen_image_vae.safetensors
```

Official RAW-to-Turbo adapter:

```text
loras/krea2_turbo_lora_rank_64_bf16.safetensors
```

Official models:

```text
diffusion_models/krea2_raw_int8_convrot.safetensors
diffusion_models/krea2_turbo_int8_convrot.safetensors
```

Community checkpoints and LoRAs:

| Asset | Local file | Source version |
| --- | --- | --- |
| Krea 2 NSFW V4 | `loras/KNP_000003000.safetensors` | v4.3_EXP, 3147117 |
| RedCraft | `diffusion_models/redcraft23INT8INT4FP8_30Krea2.safetensors` | V3 INT8, 3139241 |
| Moody Krea 2 Mix | `diffusion_models/moodyKrea2Mix_v50.safetensors` | V5 INT8, 3151928 |
| SNOFS | `loras/snofs_krea_v1_2.safetensors` | Krea v1.2, 3172362 |
| Mystic XXX | `loras/MysticXXX_KREA2_v3.safetensors` | V3, 3116175 |
| Dark Beast | `diffusion_models/darkBeast30BF16INT8_darkBeast330.safetensors` | 3.0 INT8 ConvRot, 3173268 |
| TextFusion refusal reduction | `loras/Krea2_TextFusion_Refusal_Reduction.safetensors` | 3125118 |

The exact source URLs, file IDs, and hashes are preserved in the download
script and model-archive sidecars.

## Workflow Settings

Official RAW uses 52 steps, CFG 3.5, Euler/simple, resolution-aware
`ModelSamplingFlux`, and a separately encoded empty negative prompt. Zeroing the
positive conditioning for RAW produced a badly blown-out result and is not
equivalent to the classifier-free-guidance path.

Official Turbo and the Turbo-derived assets use CFG 1 with 8–12 steps. The
community workflows retain the source sampler, scheduler, LoRA strength, and
precision where practical:

- KNP uses model and text-encoder strength 1.0 and Euler/beta at 8 steps.
- RedCraft uses the selected V3 INT8 checkpoint. Its source image used V3 FP8.
- Moody uses the selected V5 INT8 checkpoint. Its source image used V5 NVFP4
  plus an upscale branch; the local workflow keeps the initial 832 x 1216
  generation path.
- SNOFS uses its current v1.2 two-stage source path: RAW INT8 plus SNOFS at
  strength 1.0 for the 52-step first stage, then the official rank-64 Turbo
  adapter at strength 1.0 for the 16-step second stage. The source uses the BF16
  text encoder and scales 2:3 from 1 MP to 3 MP with a 16% handoff. This graph
  requires `Krea-2-Two-Stage-Sampler` at commit
  `b201412a0178da17b9760faa897107283428a78a`, which is also pinned by the Vast
  setup script.
- Mystic uses model and text-encoder strength 1.0 with the official Qwen Image
  VAE. The source metadata named a Wan 2.1 VAE and did not include a complete
  GUI workflow.
- Dark Beast uses the selected V3 INT8 checkpoint and its source 12-step
  Euler/simple path.

## Unlock Selection

`Krea2_TextFusion_Refusal_Reduction` is the default standalone unlock. It
modifies only the TextFusion routing layer, has a source-recommended strength of
1.0, and stacks successfully with KNP. This makes it a more predictable default
than broad multi-vector bypass LoRAs whose effective strength varies by model
quantization.

The unlock is optional for the community checkpoints and task-specific LoRAs:
use it when prompt refusals remain, and avoid stacking it automatically where a
checkpoint or LoRA already gives the desired behavior.

## Validation

On 2026-07-31:

- the direct post-rebuild smoke group passed all 9 Krea dependency paths at
  512 x 512, including the TextFusion-plus-KNP stack;
- all 9 canonical Krea workflows passed actual ComfyUI frontend conversion,
  `/prompt` acceptance, and history success;
- all generated PNGs decoded successfully and had non-black, non-constant RGB
  signal.

On 2026-08-30, the edited SNOFS v1.2 canonical workflow passed actual frontend
conversion (12 API nodes from 13 workflow nodes and 16 links), `/prompt`
acceptance, and ComfyUI history success. The saved output was
`/mnt/data/comfyui/output/krea2_raw_lora_snofs_v12_reference_00002_.png`.
The required complete 34-workflow no-generation preflight also passed with its
prompt, batch, seed, and output-ID overrides; the SNOFS test copy used the
requested 832 x 1216 base and final dimensions without changing the canonical
1 MP to 3 MP reference graph.

Human reference review:

- On 2026-08-30, the KNP v4.3 workflow was reviewed at the source reference
  resolution of 1088 x 1448. Its local INT8 ConvRot output was judged extremely
  close to the archived FP8 source image despite the unavoidable precision
  difference.
- Dark Beast V3 was reviewed at its 1024 x 1536 source generation resolution
  and judged a good match before the source's upscale and grain postprocessing.
- RedCraft V3 was reviewed at its 1440 x 2160 source generation resolution and
  judged a good match despite the local INT8 checkpoint and FP8 text encoder.
- Moody Mix V5 was reviewed at its 1024 x 1536 source generation resolution and
  judged extremely close despite the local INT8 checkpoint and omitted upscale
  and detail-processing stages.
- SNOFS Krea v1.2 was reviewed at the current source image's 1456 x 2176 final
  resolution and judged a good match. The local non-save API graph matches the
  embedded source graph and parameters; the comparison measured SSIM `0.9301`
  and pixel correlation `0.9727`, with differences concentrated in fine detail.

Canonical workflows:

```text
workflows/krea-2/raw/original/krea2_raw_original.json
workflows/krea-2/raw/nsfw/krea2_raw_lora_snofs_v12.json
workflows/krea-2/turbo/original/krea2_turbo_original.json
workflows/krea-2/turbo/nsfw/krea2_turbo_lora_textfusion_unlock.json
workflows/krea-2/turbo/nsfw/krea2_turbo_lora_knp_v43.json
workflows/krea-2/turbo/nsfw/krea2_turbo_checkpoint_redcraft_v3_int8.json
workflows/krea-2/turbo/nsfw/krea2_turbo_checkpoint_moody_mix_v5_int8.json
workflows/krea-2/turbo/nsfw/krea2_turbo_lora_mystic_v3.json
workflows/krea-2/turbo/nsfw/krea2_turbo_checkpoint_darkbeast_v3_int8.json
```
