# Modern Original Model Smoke Tests

ComfyUI API smoke tests run on 2026-05-28 against `http://x399.lan:8188/`
using the Docker ComfyUI instance from `./run_comfyui.sh`.

The tests used small 512px prompts and `POST /prompt`; output images are under
`/mnt/data/comfyui/output`.

| Model | Result | Output / blocker |
| --- | --- | --- |
| FLUX.2 Dev | pass | `/mnt/data/comfyui/output/smoke_flux2_dev_00001_.png` |
| FLUX.2 Dev official text-to-image path | pass | `/mnt/data/comfyui/output/smoke_flux2_dev_text_to_image_00001_.png` |
| FLUX.2 Klein 9B | pass | `/mnt/data/comfyui/output/smoke_flux2_klein_9b_00001_.png`, `/mnt/data/comfyui/output/smoke_flux2_klein_9b_distilled_00001_.png` |
| Qwen-Image 2512 | pass | `/mnt/data/comfyui/output/smoke_qwen_image_2512_00001_.png` |
| Qwen-Image-Edit 2511 | pass | `/mnt/data/comfyui/output/smoke_qwen_image_edit_2511_00001_.png` |
| Z-Image Turbo | pass | `/mnt/data/comfyui/output/smoke_z_image_turbo_00001_.png` |
| Z-Image Base | pass | `/mnt/data/comfyui/output/smoke_z_image_base_00001_.png` |

## Notes

- Qwen-Image-Edit 2511 used an existing ComfyUI input image and a minimal edit
  prompt to exercise the official edit model path.
- FLUX.2 Dev official text-to-image smoke used
  `mistral_3_small_flux2_bf16.safetensors`,
  `full_encoder_small_decoder.safetensors`, and a 256px, 1-step API prompt. A
  512px BF16 text-encoder smoke hit CUDA OOM on the 24 GB 8188 instance.
- Optional Lightning/Turbo LoRAs from the official templates were not loaded;
  this pass validates the original base model files only.
- `/free` returned an empty HTTP response body after each call, but the server
  accepted prompts and completed all non-blocked jobs successfully.
