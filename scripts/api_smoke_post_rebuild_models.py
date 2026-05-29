#!/usr/bin/env python3
import argparse
import json
import sys
import time
import urllib.error
import urllib.request
import uuid


PROMPT = "a small red cube on a wooden table, studio light"
NEGATIVE = "low quality, blurry, distorted"


def post_json(base_url, path, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
    return json.loads(body) if body else {}


def get_json(base_url, path):
    with urllib.request.urlopen(f"{base_url}{path}", timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def free_memory(base_url):
    try:
        post_json(base_url, "/free", {"unload_models": True, "free_memory": True})
    except Exception as exc:
        print(f"warn: /free failed: {exc}", flush=True)


def wait_for_prompt(base_url, prompt_id, timeout_s):
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        history = get_json(base_url, f"/history/{prompt_id}")
        if prompt_id in history:
            entry = history[prompt_id]
            status = entry.get("status", {})
            if status.get("status_str") == "error":
                messages = status.get("messages", [])
                raise RuntimeError(f"ComfyUI error: {messages}")
            return entry
        time.sleep(2)
    raise TimeoutError(f"timed out waiting for prompt {prompt_id}")


def outputs_from_history(entry):
    files = []
    for node in entry.get("outputs", {}).values():
        for item in node.get("images", []):
            files.append(item.get("filename"))
        for item in node.get("gifs", []):
            files.append(item.get("filename"))
    return [f for f in files if f]


def run_prompt(base_url, name, prompt, timeout_s):
    print(f"RUN {name}", flush=True)
    response = post_json(base_url, "/prompt", {"prompt": prompt, "client_id": str(uuid.uuid4())})
    prompt_id = response["prompt_id"]
    entry = wait_for_prompt(base_url, prompt_id, timeout_s)
    files = outputs_from_history(entry)
    if not files:
        raise RuntimeError("prompt completed but produced no saved output")
    print(f"PASS {name}: {', '.join(files)}", flush=True)
    return files


def checkpoint_prompt(ckpt, prefix, width=320, height=320, steps=1, cfg=3.5):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": ckpt}},
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": PROMPT, "clip": ["1", 1]},
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": NEGATIVE, "clip": ["1", 1]},
        },
        "4": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": width, "height": height, "batch_size": 1},
        },
        "5": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["1", 0],
                "positive": ["2", 0],
                "negative": ["3", 0],
                "latent_image": ["4", 0],
                "seed": 101,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0,
            },
        },
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": prefix}},
    }


def flux_checkpoint_prompt(ckpt, prefix, width=320, height=320):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": ckpt}},
        "2": {
            "class_type": "TripleCLIPLoader",
            "inputs": {
                "clip_name1": "t5xxl_fp16.safetensors",
                "clip_name2": "clip_l.safetensors",
                "clip_name3": "clip_g.safetensors",
            },
        },
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "Flux/flux_vae.safetensors"}},
        "4": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": PROMPT, "clip": ["2", 0]},
        },
        "5": {"class_type": "ModelSamplingFlux", "inputs": {"model": ["1", 0], "max_shift": 1.21, "base_shift": 0.5, "width": width, "height": height}},
        "6": {"class_type": "FluxGuidance", "inputs": {"conditioning": ["4", 0], "guidance": 4.0}},
        "7": {"class_type": "RandomNoise", "inputs": {"noise_seed": 107}},
        "8": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "dpmpp_sde"}},
        "9": {"class_type": "BasicScheduler", "inputs": {"model": ["5", 0], "scheduler": "beta", "steps": 1, "denoise": 1.0}},
        "10": {"class_type": "BasicGuider", "inputs": {"model": ["5", 0], "conditioning": ["6", 0]}},
        "11": {
            "class_type": "EmptySD3LatentImage",
            "inputs": {"width": width, "height": height, "batch_size": 1},
        },
        "12": {
            "class_type": "SamplerCustomAdvanced",
            "inputs": {"noise": ["7", 0], "guider": ["10", 0], "sampler": ["8", 0], "sigmas": ["9", 0], "latent_image": ["11", 0]},
        },
        "13": {"class_type": "VAEDecode", "inputs": {"samples": ["12", 0], "vae": ["3", 0]}},
        "14": {"class_type": "SaveImage", "inputs": {"images": ["13", 0], "filename_prefix": prefix}},
    }


def z_image_prompt(unet, prefix, gguf=False, loras=None, width=320, height=320):
    model_loader = "UnetLoaderGGUF" if gguf else "UNETLoader"
    clip_loader = "CLIPLoaderGGUF" if gguf else "CLIPLoader"
    model_inputs = {"unet_name": unet}
    if not gguf:
        model_inputs["weight_dtype"] = "default"
    prompt = {
        "1": {"class_type": model_loader, "inputs": model_inputs},
        "2": {
            "class_type": clip_loader,
            "inputs": {"clip_name": "Qwen3-4B-UD-Q6_K_XL.gguf" if gguf else "qwen_3_4b.safetensors", "type": "lumina2"},
        },
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
        "4": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": PROMPT, "clip": ["2", 0]},
        },
        "5": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": NEGATIVE, "clip": ["2", 0]},
        },
        "6": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": 3.0}},
        "7": {
            "class_type": "EmptySD3LatentImage",
            "inputs": {"width": width, "height": height, "batch_size": 1},
        },
        "8": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["6", 0],
                "positive": ["4", 0],
                "negative": ["5", 0],
                "latent_image": ["7", 0],
                "seed": 102,
                "steps": 1,
                "cfg": 1.0,
                "sampler_name": "res_multistep",
                "scheduler": "simple",
                "denoise": 1.0,
            },
        },
        "9": {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["3", 0]}},
        "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": prefix}},
    }
    last_model_ref, last_clip_ref = ["6", 0], ["2", 0]
    for idx, (lora, strength) in enumerate(loras or [], start=20):
        node_id = str(idx)
        prompt[node_id] = {
            "class_type": "LoraLoader",
            "inputs": {
                "model": last_model_ref,
                "clip": last_clip_ref,
                "lora_name": lora,
                "strength_model": strength,
                "strength_clip": strength,
            },
        }
        last_model_ref = [node_id, 0]
        last_clip_ref = [node_id, 1]
    if loras:
        prompt["8"]["inputs"]["model"] = last_model_ref
        prompt["4"]["inputs"]["clip"] = last_clip_ref
        prompt["5"]["inputs"]["clip"] = last_clip_ref
    return prompt


def qwen_image_prompt(unet, prefix, lora=None, edit=False, width=320, height=320):
    prompt = {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": unet, "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_vae.safetensors"}},
        "4": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": 3.1}},
        "5": {"class_type": "EmptySD3LatentImage", "inputs": {"width": width, "height": height, "batch_size": 1}},
        "8": {"class_type": "CLIPTextEncode", "inputs": {"text": NEGATIVE, "clip": ["2", 0]}},
    }
    model_ref = ["4", 0]
    if lora:
        prompt["6"] = {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {"model": model_ref, "lora_name": lora, "strength_model": 1.0},
        }
        model_ref = ["6", 0]
    if edit:
        prompt["9"] = {"class_type": "LoadImage", "inputs": {"image": "female_wizard.png"}}
        prompt["7"] = {
            "class_type": "TextEncodeQwenImageEdit",
            "inputs": {"clip": ["2", 0], "vae": ["3", 0], "image": ["9", 0], "prompt": "make the lighting warmer"},
        }
    else:
        prompt["7"] = {"class_type": "CLIPTextEncode", "inputs": {"text": PROMPT, "clip": ["2", 0]}}
    prompt.update(
        {
            "10": {
                "class_type": "KSampler",
                "inputs": {
                    "model": model_ref,
                    "positive": ["7", 0],
                    "negative": ["8", 0],
                    "latent_image": ["5", 0],
                    "seed": 103,
                    "steps": 1,
                    "cfg": 1.0 if edit else 4.0,
                    "sampler_name": "euler_ancestral" if edit else "euler",
                    "scheduler": "beta" if edit else "simple",
                    "denoise": 1.0,
                },
            },
            "11": {"class_type": "VAEDecode", "inputs": {"samples": ["10", 0], "vae": ["3", 0]}},
            "12": {"class_type": "SaveImage", "inputs": {"images": ["11", 0], "filename_prefix": prefix}},
        }
    )
    return prompt


def flux2_prompt(unet, prefix, lora=None, width=256, height=256):
    if "klein" in unet.lower() or "biglove" in unet.lower():
        clip_name = "qwen_3_8b_fp8mixed.safetensors"
        vae_name = "flux2-vae.safetensors" if "biglove" in unet.lower() else "full_encoder_small_decoder.safetensors"
    else:
        clip_name = "mistral_3_small_flux2_bf16.safetensors"
        vae_name = "full_encoder_small_decoder.safetensors"
    prompt = {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": unet, "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": clip_name, "type": "flux2"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": vae_name}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": PROMPT, "clip": ["2", 0]}},
        "5": {"class_type": "FluxGuidance", "inputs": {"conditioning": ["4", 0], "guidance": 4.0}},
        "6": {"class_type": "RandomNoise", "inputs": {"noise_seed": 104}},
        "7": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
        "8": {"class_type": "Flux2Scheduler", "inputs": {"steps": 1, "width": width, "height": height}},
        "9": {"class_type": "EmptyFlux2LatentImage", "inputs": {"width": width, "height": height, "batch_size": 1}},
    }
    model_ref = ["1", 0]
    if lora:
        prompt["10"] = {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {"model": model_ref, "lora_name": lora, "strength_model": 1.0},
        }
        model_ref = ["10", 0]
    prompt.update(
        {
            "11": {"class_type": "BasicGuider", "inputs": {"model": model_ref, "conditioning": ["5", 0]}},
            "12": {
                "class_type": "SamplerCustomAdvanced",
                "inputs": {"noise": ["6", 0], "guider": ["11", 0], "sampler": ["7", 0], "sigmas": ["8", 0], "latent_image": ["9", 0]},
            },
            "13": {"class_type": "VAEDecode", "inputs": {"samples": ["12", 0], "vae": ["3", 0]}},
            "14": {"class_type": "SaveImage", "inputs": {"images": ["13", 0], "filename_prefix": prefix}},
        }
    )
    return prompt


def qwen_rapid_prompt(prefix):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "Qwen-Rapid-AIO-NSFW-v23.safetensors"}},
        "2": {"class_type": "LoadImage", "inputs": {"image": "female_wizard.png"}},
        "3": {"class_type": "LoadImage", "inputs": {"image": "dungeon_empty.png"}},
        "4": {
            "class_type": "TextEncodeQwenImageEditPlus",
            "inputs": {
                "clip": ["1", 1],
                "vae": ["1", 2],
                "image1": ["2", 0],
                "image2": ["3", 0],
                "prompt": "Put the subject from the first image into the second image scene.",
            },
        },
        "5": {"class_type": "TextEncodeQwenImageEditPlus", "inputs": {"clip": ["1", 1], "prompt": ""}},
        "6": {"class_type": "EmptyLatentImage", "inputs": {"width": 320, "height": 320, "batch_size": 1}},
        "7": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["1", 0],
                "positive": ["4", 0],
                "negative": ["5", 0],
                "latent_image": ["6", 0],
                "seed": 105,
                "steps": 1,
                "cfg": 1.0,
                "sampler_name": "euler_ancestral",
                "scheduler": "beta",
                "denoise": 1.0,
            },
        },
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["1", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"images": ["8", 0], "filename_prefix": prefix}},
    }


TESTS = [
    ("flux1_schnell_fp8", lambda: checkpoint_prompt("flux1-schnell-fp8.safetensors", "smoke_rebuild_flux1_schnell", 320, 320, 1, 1.0), 600),
    ("fluxed_up_checkpoint", lambda: flux_checkpoint_prompt("fluxedUpFluxNSFW_100BF16.safetensors", "smoke_rebuild_fluxed_up", 320, 320), 600),
    ("pony_diffusion_v6", lambda: checkpoint_prompt("ponyDiffusionV6XL_v6StartWithThisOne.safetensors", "smoke_rebuild_pony_v6", 320, 320, 1, 3.5), 600),
    ("cognitiveriver_pony", lambda: checkpoint_prompt("cognitiveriver_ponyV20.safetensors", "smoke_rebuild_cognitiveriver", 320, 320, 1, 3.5), 600),
    ("flux2_dev", lambda: flux2_prompt("flux2_dev_fp8mixed.safetensors", "smoke_rebuild_flux2_dev"), 900),
    ("biglove_klein2", lambda: flux2_prompt("bigLove_klein2_fp8_pruned.safetensors", "smoke_rebuild_biglove_klein2"), 900),
    ("flux2_klein_base_9b", lambda: flux2_prompt("flux-2-klein-base-9b-fp8.safetensors", "smoke_rebuild_flux2_klein_base_9b"), 900),
    ("flux2_klein_9b_lora", lambda: flux2_prompt("flux-2-klein-9b-fp8.safetensors", "smoke_rebuild_flux2_klein_9b_lora", "FLUX2_KLEIN_UNLOCKED_V1.safetensors"), 900),
    ("z_image_turbo_bf16_loras", lambda: z_image_prompt("z_image_turbo_bf16.safetensors", "smoke_rebuild_z_image_turbo_loras", False, [("Mystic-XXX-ZIT-V7.safetensors", 0.2), ("Z-Detail-Slider.safetensors", 0.1)]), 900),
    ("z_image_turbo_gguf", lambda: z_image_prompt("z_image_turbo-Q8_0.gguf", "smoke_rebuild_z_image_turbo_gguf", True), 900),
    ("z_image_base_bf16", lambda: z_image_prompt("z_image_bf16.safetensors", "smoke_rebuild_z_image_base_bf16", False), 900),
    ("z_image_base_gguf_ogre_stack", lambda: z_image_prompt("z-image-Q8_0.gguf", "smoke_rebuild_z_image_base_gguf", True, [("128 bean effect 3_000101000.safetensors", 0.2), ("ZIB-Image-Fun-Lora-Distill-2603_UDCAI_ComfyUI.safetensors", 0.2)]), 900),
    ("qwen_image_2512_lightning", lambda: qwen_image_prompt("qwen_image_2512_fp8_e4m3fn.safetensors", "smoke_rebuild_qwen_2512_lightning", "Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors"), 900),
    ("jib_mix_qwen_2512", lambda: qwen_image_prompt("jibMixQwen_v60.safetensors", "smoke_rebuild_jib_mix_qwen", "jib_qwen_fix_000002750.safetensors"), 900),
    ("qwen_image_edit_2511", lambda: qwen_image_prompt("qwen_image_edit_2511_bf16.safetensors", "smoke_rebuild_qwen_edit_2511", "Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors", True), 900),
    ("qwen_rapid_aio_v23", lambda: qwen_rapid_prompt("smoke_rebuild_qwen_rapid_aio_v23"), 900),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8188")
    parser.add_argument("--only", nargs="*", help="Run only named tests")
    parser.add_argument("--skip", nargs="*", default=[], help="Skip named tests")
    args = parser.parse_args()

    selected = []
    only = set(args.only or [])
    skip = set(args.skip or [])
    for name, factory, timeout_s in TESTS:
        if only and name not in only:
            continue
        if name in skip:
            continue
        selected.append((name, factory, timeout_s))

    results = {}
    for name, factory, timeout_s in selected:
        try:
            files = run_prompt(args.base_url, name, factory(), timeout_s)
            results[name] = {"ok": True, "files": files}
        except Exception as exc:
            print(f"FAIL {name}: {exc}", flush=True)
            results[name] = {"ok": False, "error": str(exc)}
        finally:
            free_memory(args.base_url)
            time.sleep(2)

    print(json.dumps(results, indent=2, sort_keys=True), flush=True)
    return 1 if any(not item["ok"] for item in results.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
