# Moody Wild Mix V4 Base

Simplified local reference workflow for Civitai image 130509460 using Moody
Wild Mix (ZIB/ZID) V4.0 BASE 40STEPS CFG4.

## Sources

```text
Reference image:
https://civitai.red/images/130509460

Model page:
https://civitai.red/models/2384856/moody-wild-mix-zibzid?modelVersionId=2939920

Source workflow resource:
https://civitai.red/models/2612239/moody-zimage-base-simple-workflow?modelVersionId=2933293
```

Source version facts:

```text
Model:            Moody Wild Mix (ZIB/ZID)
Version:          V4.0 BASE 40STEPS CFG4
Model version ID: 2939920
Base model:       ZImageBase
Civitai filename: moodyWildMixZIBZID_v40BASE40STEPSCFG4.safetensors
Selected file:    full FP16, non-primary
Local filename:   moodyWildMixZIBZID_v40BASE40STEPSCFG4_fp16_full.safetensors
```

The source image workflow used this source-local UNet filename:

```text
ComfyUI\moody-wild-v4-undistilled-40steps-cfg4_00001__clean.safetensors
```

The local workflow maps that to the expected local full fp16 filename:

```text
moodyWildMixZIBZID_v40BASE40STEPSCFG4_fp16_full.safetensors
```

## Local Files

Required local ComfyUI files:

```text
diffusion_models/moodyWildMixZIBZID_v40BASE40STEPSCFG4_fp16_full.safetensors
text_encoders/qwen_3_4b.safetensors
vae/ae.safetensors
```

## Workflow

Repo workflow:

```text
workflows/z-image/base/nsfw/z_image_base_merge_moody_wild_v4.json
```

The workflow keeps the core source two-pass Z-Image Base generation path from
the embedded source image metadata. It intentionally omits unsupported or
non-core polish branches: UltimateSDUpscale, face/detailer/manual repaint,
skin contrast, SeedVR2, upscaler/detector weights, image comparers, preview
labels, group bypassers, and GUI clutter.

Important retained settings:

```text
UNETLoader:              moodyWildMixZIBZID_v40BASE40STEPSCFG4_fp16_full.safetensors, default
CLIPLoader:              qwen_3_4b.safetensors, lumina2, default
VAELoader:               ae.safetensors
Latent size:             640 x 960, batch 1
Seed:                    524
First sampler:           KSamplerAdvanced, 35 steps, CFG 4, res_multistep, simple
First step range:        start 0, end 30, return leftover noise enabled
Latent upscale:          bislerp, scale 1.7
ModelSamplingAuraFlow:   shift 3.0 before the second sampler
Second sampler:          KSamplerAdvanced, 30 steps, CFG 4, dpmpp_2m_sde, beta
Second step range:       start 15, end 999, return leftover noise disabled
Save prefix:             z-image-moody-wild-v4-base
```

Prompt:

```text
游戏厅抓娃娃机旁

视觉风格：抓娃娃机内部的彩色射灯+闪光灯，画面像游乐园万花筒。

少女侧靠在抓娃娃机的玻璃上，隔着玻璃能看到里面堆满的毛绒玩具。

她全身只穿一条蕾丝丁字裤（后边是一根细线），上身全裸。她故意把一侧乳房贴在冰凉的玻璃上，乳头被玻璃压扁，乳晕周围起了一层鸡皮疙瘩。另一侧乳房自由垂着。她岔开腿站着，丁字裤前面只有一小块倒三角蕾丝，根本挡不住，从侧面能看到光洁的阴阜隆起。她对着镜头微笑，眼睛又大又亮，嘴角带笑，像在说“你抓到我就跟我走”。
```

Negative prompt:

```text
泛黄，模糊，低分辨率，低质量图像，诡异的外观，多餘手臂, 多餘腿部，丑陋，躁点，网格感，JPEG压缩条纹，水印，乱码，意义不明的字符，Out of frame
```

No Civitai trainedWords or trigger words are listed for this version.

## Current Local Status

Created on 2026-05-30 from the source workflow-bearing Civitai image metadata.
API smoke test on 2026-05-30 with the full FP16 checkpoint and retained
two-pass source settings produced:

```text
/mnt/data/comfyui/output/smoke_z_image_moody_wild_v4_base_00001_.png
```
