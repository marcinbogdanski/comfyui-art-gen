# PornMaster Z-Image Base V1

Simplified local text-to-image reference workflow for Civitai image 129616239
using PornMaster Z-Image Base_V1.

## Sources

```text
Reference image:
https://civitai.red/images/129616239

Model page:
https://civitai.red/models/2270401/pornmaster-z-image?modelVersionId=2918406
```

Source version facts:

```text
Model:            PornMaster Z-Image
Version:          Base_V1
Model version ID: 2918406
Base model:       ZImageBase
```

The source image URL has a `.jpeg` suffix, but the downloaded file header is
PNG and embeds ComfyUI `prompt` and `workflow` metadata.

The embedded source workflow used this source-local UNet filename:

```text
z image base\PornMaster_z-image_base_V1_fp8.safetensors
```

The local workflow intentionally maps that fp8 source-local filename to the
preferred local bf16 checkpoint:

```text
pornmasterZImage_baseV1_bf16.safetensors
```

This checkpoint precision/name substitution can change the output, so the local
image may drift from the exact Civitai reference even with the same seed and
prompt.

## Local Files

Required local ComfyUI files:

```text
diffusion_models/pornmasterZImage_baseV1_bf16.safetensors
text_encoders/qwen_3_4b.safetensors
vae/ae.safetensors
loras/Z-Image-Fun-Lora-Distill-8-Steps-2603-ComfyUI.safetensors
loras/Z-Image-Fun-Lora-Distill-4-Steps-2603-ComfyUI.safetensors
```

The source CLIP path contains a typo-like local filename:

```text
z image\qweb_3_4b.safetensors
```

The local workflow uses the available Z-Image text encoder filename:

```text
qwen_3_4b.safetensors
```

## Workflow

Repo workflow:

```text
workflows/z-image/base/nsfw/z_image_base_checkpoint_pornmaster_v1.json
```

The workflow keeps the source text-to-image generation path from the embedded
source image metadata. It omits source GUI/audio/cleanup clutter:
`easy cleanGpuUsed`, `PlaySound|pysssss`, and the source markdown model-link
note.

The source LoraManager node is replaced by two sequential core `LoraLoader`
nodes with the same activation strengths.

Important retained settings:

```text
UNETLoader:              pornmasterZImage_baseV1_bf16.safetensors, default
CLIPLoader:              qwen_3_4b.safetensors, lumina2, default
VAELoader:               ae.safetensors
LoRA 8-step distill:     model 0.5, clip 0.5
LoRA 4-step distill:     model 0.5, clip 0.5
Latent size:             1024 x 1936, batch 1
Seed:                    2562038239099
Sampler:                 KSamplerAdvanced, 8 steps, CFG 1, euler, simple
Step range:              start 0, end 9999, return leftover noise disabled
ModelSamplingAuraFlow:   shift 3
Save prefix:             z-image-pornmaster-base-v1
```

Prompt:

```text
這是一張採用 35mm 膠片拍攝的高分辨率超寫實電影劇照。鏡頭聚焦於一位擁有極致沙漏型身材的單人女性，她具備高挑的身軀、短腰且修長的雙腿，纖細的腰部線條與豐滿的胸部曲線形成強烈視覺對比。她身著一套淡青綠色的改良式漢服，服飾材質選用頂級的薄透蟬翼紗，呈現出半透明的質感，輕盈地覆蓋全身，其上鑲嵌著純銀絲線編織的通透花卉刺繡，在柔光下閃爍著細膩的銀光。

女性採取慵懶且婀娜的站姿，背對鏡頭，上半身帶著一種空靈而魅惑的氣息輕盈地向後回眸。她的黑色長髮梳理成規整的高盤發，完全露出額頭與小巧的耳朵，點綴著雕工精美的傳統銀質發飾。她的面部皮膚如陶瓷般細膩光滑，眉目清秀，展現出含蓄而羞澀的表情。她輕輕抿嘴含蓄微笑，雙唇微啟間隱約露出整齊潔白的牙齒，眼神中流露出慵懶與靈動。

她手中握著一把精緻的同色系圓形團扇，扇面上布滿半透明的花卉圖案。背景設置在充滿文化韻味的中式園林中，背景細節華麗且富有層次，包含雕花窗櫺與怪石盆景。環境中充斥著漫反射的柔和光影，無數粉色花瓣在空中隨風飛舞，營造出一種仙氣繚繞的氛圍。整張照片具有明顯的膠片顆粒感，色彩飽和度適中，背景簡約而不失格調，完美還原了古典電影鏡頭的質感。
```

Negative prompt:

```text
低质量，模糊，扭曲，丑陋，多余的手指，变形的脸，不对称的眼睛，错位的牙齿，重复的纹理，嗓点，压缩伪影，水印，文字，边框，网格线，3D渲染，CG，渲染感，过度曝光，阴影过重，色彩失真，平面化，缺乏细节，简笔画，动作僵硬，畸形，丑态，
```

No trigger words are listed in the embedded source workflow; the two distill
LoRAs are activated only by their loader strengths.

## Current Local Status

Created on 2026-05-30 from the source workflow-bearing Civitai image metadata.
A reduced-size ComfyUI API smoke test on 2026-05-30 used the local BF16
checkpoint, both 2603 distill LoRAs, and the retained source seed/settings at
512 x 960. It completed successfully and produced:

```text
/mnt/data/comfyui/output/smoke_z_image_pornmaster_base_v1_00001_.png
```

The smoke test verified model and LoRA loading plus sampling. It was not a
full-size 1024 x 1936 reproduction run.
