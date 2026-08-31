#!/usr/bin/env python3
"""Fast direct-API smoke tests for the locally supported image-model inventory.

This intentionally does not use the ComfyUI frontend. Canonical workflow
conversion and full-generation coverage belong to workflow_prompt.py and
workflow_queue.py; this script answers the narrower post-rebuild question:
"Can every supported generation weight load and produce a plausible PNG, and
are its specialized runtime dependencies discoverable?"
"""

import argparse
import json
import math
import struct
import sys
import time
import urllib.error
import urllib.request
import uuid
import zlib
from dataclasses import dataclass
from pathlib import Path


PROMPT = "a small red cube on a wooden table, soft studio light, detailed photograph"
NEGATIVE = "low quality, blurry, distorted, black image"
DEFAULT_OUTPUT_DIR = Path("/mnt/data/comfyui/output")


@dataclass(frozen=True)
class SmokeTest:
    name: str
    group: str
    factory: object
    timeout_s: int = 900
    required_nodes: tuple = ()
    required_choices: tuple = ()


def post_json(base_url, path, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}{path}",
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
    with urllib.request.urlopen(f"{base_url.rstrip('/')}{path}", timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def advertised_choices(object_info, node_name, input_name):
    spec = object_info[node_name]["input"]["required"][input_name]
    if spec and isinstance(spec[0], list):
        return set(spec[0])
    if len(spec) > 1 and isinstance(spec[1], dict):
        return set(spec[1].get("options", []))
    return set()


def validate_runtime_dependencies(test, object_info):
    missing_nodes = sorted(set(test.required_nodes) - set(object_info))
    if missing_nodes:
        raise RuntimeError(f"missing required ComfyUI nodes: {missing_nodes}")
    for node_name, input_name, choice in test.required_choices:
        if node_name not in object_info:
            raise RuntimeError(f"missing required ComfyUI node: {node_name}")
        choices = advertised_choices(object_info, node_name, input_name)
        if choice not in choices:
            raise RuntimeError(
                f"{node_name}.{input_name} does not advertise required asset: {choice}"
            )


def free_memory(base_url):
    try:
        post_json(base_url, "/free", {"unload_models": True, "free_memory": True})
    except Exception as exc:
        print(f"warn: /free failed: {exc}", flush=True)


def wait_for_prompt(base_url, prompt_id, timeout_s):
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        history = get_json(base_url, f"/history/{prompt_id}")
        if prompt_id in history:
            entry = history[prompt_id]
            status = entry.get("status", {})
            if status.get("status_str") == "error":
                messages = status.get("messages", [])
                raise RuntimeError(f"ComfyUI error: {messages}")
            if status.get("status_str") != "success" or status.get("completed") is not True:
                raise RuntimeError(f"prompt did not complete successfully: {status}")
            return entry
        time.sleep(2)
    raise TimeoutError(f"timed out waiting for prompt {prompt_id}")


def outputs_from_history(entry):
    files = []
    for node in entry.get("outputs", {}).values():
        for key in ("images", "gifs"):
            for item in node.get(key, []):
                filename = item.get("filename")
                if filename:
                    files.append(
                        {
                            "filename": filename,
                            "subfolder": item.get("subfolder") or "",
                            "type": item.get("type") or "output",
                        }
                    )
    return files


def paeth_predictor(left, above, upper_left):
    estimate = left + above - upper_left
    left_distance = abs(estimate - left)
    above_distance = abs(estimate - above)
    upper_left_distance = abs(estimate - upper_left)
    if left_distance <= above_distance and left_distance <= upper_left_distance:
        return left
    if above_distance <= upper_left_distance:
        return above
    return upper_left


def png_metrics(path):
    """Read enough PNG to validate dimensions and RGB signal using stdlib only."""
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError(f"not a PNG: {path}")

    offset = 8
    width = height = bit_depth = color_type = interlace = None
    idat = bytearray()
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        kind = data[offset + 4 : offset + 8]
        payload = data[offset + 8 : offset + 8 + length]
        offset += 12 + length
        if kind == b"IHDR":
            width, height, bit_depth, color_type, _, _, interlace = struct.unpack(
                ">IIBBBBB", payload
            )
        elif kind == b"IDAT":
            idat.extend(payload)
        elif kind == b"IEND":
            break

    if not width or not height or not idat:
        raise RuntimeError(f"incomplete PNG: {path}")
    if bit_depth != 8 or interlace != 0:
        raise RuntimeError(
            f"unsupported PNG layout for smoke validation: "
            f"bit_depth={bit_depth}, interlace={interlace}"
        )

    channels_by_color_type = {0: 1, 2: 3, 4: 2, 6: 4}
    channels = channels_by_color_type.get(color_type)
    if channels is None:
        raise RuntimeError(f"unsupported PNG color type: {color_type}")

    raw = zlib.decompress(bytes(idat))
    stride = width * channels
    expected = (stride + 1) * height
    if len(raw) != expected:
        raise RuntimeError(f"unexpected PNG payload size: {len(raw)} != {expected}")

    previous = bytearray(stride)
    rgb_values = []
    position = 0
    for _ in range(height):
        filter_type = raw[position]
        position += 1
        filtered = raw[position : position + stride]
        position += stride
        row = bytearray(stride)
        for index, value in enumerate(filtered):
            left = row[index - channels] if index >= channels else 0
            above = previous[index]
            upper_left = previous[index - channels] if index >= channels else 0
            if filter_type == 0:
                decoded = value
            elif filter_type == 1:
                decoded = value + left
            elif filter_type == 2:
                decoded = value + above
            elif filter_type == 3:
                decoded = value + ((left + above) // 2)
            elif filter_type == 4:
                decoded = value + paeth_predictor(left, above, upper_left)
            else:
                raise RuntimeError(f"unsupported PNG filter type: {filter_type}")
            row[index] = decoded & 0xFF

        if color_type in (0, 4):
            rgb_values.extend(row[index] for index in range(0, stride, channels))
        else:
            for index in range(0, stride, channels):
                rgb_values.extend(row[index : index + 3])
        previous = row

    minimum = min(rgb_values)
    maximum = max(rgb_values)
    mean = sum(rgb_values) / len(rgb_values)
    variance = sum((value - mean) ** 2 for value in rgb_values) / len(rgb_values)
    return {
        "width": width,
        "height": height,
        "rgb_min": minimum,
        "rgb_max": maximum,
        "rgb_mean": round(mean, 3),
        "rgb_stddev": round(math.sqrt(variance), 3),
    }


def validate_output(output_dir, item):
    if item["type"] != "output":
        raise RuntimeError(f"expected saved output, got type={item['type']}")
    path = output_dir / item["subfolder"] / item["filename"]
    if not path.is_file():
        raise RuntimeError(f"history output does not exist: {path}")
    metrics = png_metrics(path)
    if metrics["width"] < 256 or metrics["height"] < 256:
        raise RuntimeError(f"output resolution is too small: {metrics}")
    if metrics["rgb_max"] < 8 or metrics["rgb_mean"] < 0.5:
        raise RuntimeError(f"output appears black: {metrics}")
    if metrics["rgb_max"] - metrics["rgb_min"] < 2:
        raise RuntimeError(f"output appears blank/constant: {metrics}")
    return path, metrics


def run_prompt(base_url, name, prompt, timeout_s, output_dir):
    print(f"RUN {name}", flush=True)
    response = post_json(
        base_url,
        "/prompt",
        {"prompt": prompt, "client_id": str(uuid.uuid4())},
    )
    if response.get("node_errors"):
        raise RuntimeError(f"ComfyUI node errors: {response['node_errors']}")
    prompt_id = response.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(f"ComfyUI response missing prompt_id: {response}")

    entry = wait_for_prompt(base_url, prompt_id, timeout_s)
    files = outputs_from_history(entry)
    if len(files) != 1:
        raise RuntimeError(f"expected exactly one saved output, got {files}")
    path, metrics = validate_output(output_dir, files[0])
    print(
        f"PASS {name}: {path.name} "
        f"{metrics['width']}x{metrics['height']} "
        f"mean={metrics['rgb_mean']} stddev={metrics['rgb_stddev']}",
        flush=True,
    )
    return str(path), metrics


def checkpoint_prompt(ckpt, prefix, width=320, height=320, steps=2, cfg=3.5):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": ckpt}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": PROMPT, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": NEGATIVE, "clip": ["1", 1]}},
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
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": PROMPT, "clip": ["2", 0]}},
        "5": {
            "class_type": "ModelSamplingFlux",
            "inputs": {
                "model": ["1", 0],
                "max_shift": 1.21,
                "base_shift": 0.5,
                "width": width,
                "height": height,
            },
        },
        "6": {"class_type": "FluxGuidance", "inputs": {"conditioning": ["4", 0], "guidance": 4.0}},
        "7": {"class_type": "RandomNoise", "inputs": {"noise_seed": 107}},
        "8": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "dpmpp_sde"}},
        "9": {
            "class_type": "BasicScheduler",
            "inputs": {"model": ["5", 0], "scheduler": "beta", "steps": 2, "denoise": 1.0},
        },
        "10": {"class_type": "BasicGuider", "inputs": {"model": ["5", 0], "conditioning": ["6", 0]}},
        "11": {
            "class_type": "EmptySD3LatentImage",
            "inputs": {"width": width, "height": height, "batch_size": 1},
        },
        "12": {
            "class_type": "SamplerCustomAdvanced",
            "inputs": {
                "noise": ["7", 0],
                "guider": ["10", 0],
                "sampler": ["8", 0],
                "sigmas": ["9", 0],
                "latent_image": ["11", 0],
            },
        },
        "13": {"class_type": "VAEDecode", "inputs": {"samples": ["12", 0], "vae": ["3", 0]}},
        "14": {"class_type": "SaveImage", "inputs": {"images": ["13", 0], "filename_prefix": prefix}},
    }


def z_image_prompt(
    unet,
    prefix,
    *,
    gguf=False,
    loras=None,
    clip_name=None,
    vae_name="ae.safetensors",
    width=320,
    height=320,
    steps=2,
    cfg=1.0,
):
    model_loader = "UnetLoaderGGUF" if gguf else "UNETLoader"
    clip_name = clip_name or ("Qwen3-4B-UD-Q6_K_XL.gguf" if gguf else "qwen_3_4b.safetensors")
    clip_is_gguf = clip_name.lower().endswith(".gguf")
    clip_loader = "CLIPLoaderGGUF" if clip_is_gguf else "CLIPLoader"
    model_inputs = {"unet_name": unet}
    if not gguf:
        model_inputs["weight_dtype"] = "default"
    prompt = {
        "1": {"class_type": model_loader, "inputs": model_inputs},
        "2": {
            "class_type": clip_loader,
            "inputs": {
                "clip_name": clip_name,
                "type": "lumina2",
            },
        },
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": vae_name}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": PROMPT, "clip": ["2", 0]}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"text": NEGATIVE, "clip": ["2", 0]}},
        "6": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": 3.0}},
        "7": {
            "class_type": "EmptySD3LatentImage",
            "inputs": {"width": width, "height": height, "batch_size": 1},
        },
    }
    model_ref, clip_ref = ["6", 0], ["2", 0]
    for index, (lora, strength) in enumerate(loras or [], start=20):
        node_id = str(index)
        prompt[node_id] = {
            "class_type": "LoraLoader",
            "inputs": {
                "model": model_ref,
                "clip": clip_ref,
                "lora_name": lora,
                "strength_model": strength,
                "strength_clip": strength,
            },
        }
        model_ref, clip_ref = [node_id, 0], [node_id, 1]
    prompt["4"]["inputs"]["clip"] = clip_ref
    prompt["5"]["inputs"]["clip"] = clip_ref
    prompt.update(
        {
            "8": {
                "class_type": "KSampler",
                "inputs": {
                    "model": model_ref,
                    "positive": ["4", 0],
                    "negative": ["5", 0],
                    "latent_image": ["7", 0],
                    "seed": 102,
                    "steps": steps,
                    "cfg": cfg,
                    "sampler_name": "res_multistep",
                    "scheduler": "simple",
                    "denoise": 1.0,
                },
            },
            "9": {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["3", 0]}},
            "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": prefix}},
        }
    )
    return prompt


def qwen_image_prompt(
    unet,
    prefix,
    *,
    loras=None,
    edit=False,
    gguf=False,
    clip_name="qwen_2.5_vl_7b_fp8_scaled.safetensors",
    steps=2,
    cfg=None,
    width=320,
    height=320,
):
    model_loader = "UnetLoaderGGUF" if gguf else "UNETLoader"
    model_inputs = {"unet_name": unet}
    if not gguf:
        model_inputs["weight_dtype"] = "default"
    prompt = {
        "1": {"class_type": model_loader, "inputs": model_inputs},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": clip_name, "type": "qwen_image"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_vae.safetensors"}},
        "4": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": 3.1}},
        "5": {
            "class_type": "EmptySD3LatentImage",
            "inputs": {"width": width, "height": height, "batch_size": 1},
        },
    }
    model_ref, clip_ref = ["4", 0], ["2", 0]
    for index, (lora, strength) in enumerate(loras or [], start=20):
        node_id = str(index)
        prompt[node_id] = {
            "class_type": "LoraLoader",
            "inputs": {
                "model": model_ref,
                "clip": clip_ref,
                "lora_name": lora,
                "strength_model": strength,
                "strength_clip": strength,
            },
        }
        model_ref, clip_ref = [node_id, 0], [node_id, 1]
    if edit:
        prompt["9"] = {"class_type": "LoadImage", "inputs": {"image": "female_wizard.png"}}
        prompt["7"] = {
            "class_type": "TextEncodeQwenImageEdit",
            "inputs": {
                "clip": clip_ref,
                "vae": ["3", 0],
                "image": ["9", 0],
                "prompt": "make the lighting warmer",
            },
        }
    else:
        prompt["7"] = {"class_type": "CLIPTextEncode", "inputs": {"text": PROMPT, "clip": clip_ref}}
    prompt["8"] = {"class_type": "CLIPTextEncode", "inputs": {"text": NEGATIVE, "clip": clip_ref}}
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
                    "steps": steps,
                    "cfg": cfg if cfg is not None else (1.0 if edit or loras else 4.0),
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


def krea2_prompt(
    unet,
    prefix,
    *,
    turbo,
    loras=None,
    enhancer=None,
    clip_name="qwen3vl_4b_fp8_scaled.safetensors",
    vae_name="qwen_image_vae.safetensors",
    steps=None,
    cfg=None,
    sampler="euler",
    scheduler="simple",
    width=512,
    height=512,
):
    prompt = {
        "1": {
            "class_type": "UNETLoader",
            "inputs": {"unet_name": unet, "weight_dtype": "default"},
        },
        "2": {
            "class_type": "CLIPLoader",
            "inputs": {
                "clip_name": clip_name,
                "type": "krea2",
                "device": "default",
            },
        },
        "3": {
            "class_type": "VAELoader",
            "inputs": {"vae_name": vae_name},
        },
        "4": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": PROMPT, "clip": ["2", 0]},
        },
        "6": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": width, "height": height, "batch_size": 1},
        },
    }
    if turbo:
        prompt["5"] = {
            "class_type": "ConditioningZeroOut",
            "inputs": {"conditioning": ["4", 0]},
        }
        model_ref = ["1", 0]
        steps = steps if steps is not None else 8
        cfg = cfg if cfg is not None else 1.0
    else:
        prompt["5"] = {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": "", "clip": ["2", 0]},
        }
        prompt["7"] = {
            "class_type": "ModelSamplingFlux",
            "inputs": {
                "model": ["1", 0],
                "max_shift": 1.15,
                "base_shift": 0.5,
                "width": width,
                "height": height,
            },
        }
        model_ref = ["7", 0]
        steps = steps if steps is not None else 28
        cfg = cfg if cfg is not None else 3.5

    for index, (lora, strength) in enumerate(loras or [], start=20):
        node_id = str(index)
        prompt[node_id] = {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {
                "model": model_ref,
                "lora_name": lora,
                "strength_model": strength,
            },
        }
        model_ref = [node_id, 0]

    if enhancer is not None:
        prompt["30"] = {
            "class_type": "Krea2T-Enhancer-Advanced",
            "inputs": {
                "model": model_ref,
                "enabled": True,
                "strength": enhancer["strength"],
                "text_scale": enhancer["text_scale"],
                "debug": True,
            },
        }
        model_ref = ["30", 0]

    prompt.update(
        {
            "8": {
                "class_type": "KSampler",
                "inputs": {
                    "model": model_ref,
                    "positive": ["4", 0],
                    "negative": ["5", 0],
                    "latent_image": ["6", 0],
                    "seed": 106,
                    "steps": steps,
                    "cfg": cfg,
                    "sampler_name": sampler,
                    "scheduler": scheduler,
                    "denoise": 1.0,
                },
            },
            "9": {
                "class_type": "VAEDecode",
                "inputs": {"samples": ["8", 0], "vae": ["3", 0]},
            },
            "10": {
                "class_type": "SaveImage",
                "inputs": {"images": ["9", 0], "filename_prefix": prefix},
            },
        }
    )
    return prompt


def flux2_prompt(
    unet,
    prefix,
    *,
    loras=None,
    clip_name=None,
    vae_name=None,
    steps=2,
    guidance=4.0,
    width=320,
    height=320,
):
    lower = unet.lower()
    is_klein = "klein" in lower or any(
        marker in lower for marker in ("biglove", "darkbeast", "pornmaster", "snofs")
    )
    clip_name = clip_name or (
        "qwen_3_8b_fp8mixed.safetensors"
        if is_klein
        else "mistral_3_small_flux2_bf16.safetensors"
    )
    vae_name = vae_name or (
        "flux2-vae.safetensors" if is_klein else "full_encoder_small_decoder.safetensors"
    )
    prompt = {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": unet, "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": clip_name, "type": "flux2"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": vae_name}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": PROMPT, "clip": ["2", 0]}},
        "5": {"class_type": "FluxGuidance", "inputs": {"conditioning": ["4", 0], "guidance": guidance}},
        "6": {"class_type": "RandomNoise", "inputs": {"noise_seed": 104}},
        "7": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
        "8": {
            "class_type": "Flux2Scheduler",
            "inputs": {"steps": steps, "width": width, "height": height},
        },
        "9": {
            "class_type": "EmptyFlux2LatentImage",
            "inputs": {"width": width, "height": height, "batch_size": 1},
        },
    }
    model_ref = ["1", 0]
    for index, (lora, strength) in enumerate(loras or [], start=20):
        node_id = str(index)
        prompt[node_id] = {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {
                "model": model_ref,
                "lora_name": lora,
                "strength_model": strength,
            },
        }
        model_ref = [node_id, 0]
    prompt.update(
        {
            "11": {"class_type": "BasicGuider", "inputs": {"model": model_ref, "conditioning": ["5", 0]}},
            "12": {
                "class_type": "SamplerCustomAdvanced",
                "inputs": {
                    "noise": ["6", 0],
                    "guider": ["11", 0],
                    "sampler": ["7", 0],
                    "sigmas": ["8", 0],
                    "latent_image": ["9", 0],
                },
            },
            "13": {"class_type": "VAEDecode", "inputs": {"samples": ["12", 0], "vae": ["3", 0]}},
            "14": {"class_type": "SaveImage", "inputs": {"images": ["13", 0], "filename_prefix": prefix}},
        }
    )
    return prompt


def qwen_rapid_prompt(prefix):
    return {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": "Qwen-Rapid-AIO-NSFW-v23.safetensors"},
        },
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
        "6": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": 320, "height": 320, "batch_size": 1},
        },
        "7": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["1", 0],
                "positive": ["4", 0],
                "negative": ["5", 0],
                "latent_image": ["6", 0],
                "seed": 105,
                "steps": 2,
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
    # Retained older inventory that is intentionally outside the current matrix.
    SmokeTest(
        "flux1_schnell_fp8",
        "legacy",
        lambda p: checkpoint_prompt("flux1-schnell-fp8.safetensors", p, steps=1, cfg=1.0),
        600,
    ),
    SmokeTest(
        "fluxed_up_checkpoint",
        "legacy",
        lambda p: flux_checkpoint_prompt("fluxedUpFluxNSFW_100BF16.safetensors", p),
        600,
    ),
    SmokeTest(
        "pony_diffusion_v6",
        "legacy",
        lambda p: checkpoint_prompt("ponyDiffusionV6XL_v6StartWithThisOne.safetensors", p),
        600,
    ),
    SmokeTest(
        "cognitiveriver_pony",
        "legacy",
        lambda p: checkpoint_prompt("cognitiveriver_ponyV20.safetensors", p),
        600,
    ),
    SmokeTest(
        "biglove_klein2_fp8",
        "legacy",
        lambda p: flux2_prompt("bigLove_klein2_fp8_pruned.safetensors", p),
    ),
    SmokeTest(
        "z_image_turbo_gguf",
        "legacy",
        lambda p: z_image_prompt("z_image_turbo-Q8_0.gguf", p, gguf=True, steps=1),
    ),
    SmokeTest(
        "z_image_base_gguf_ogre_stack",
        "legacy",
        lambda p: z_image_prompt(
            "z-image-Q8_0.gguf",
            p,
            gguf=True,
            loras=[
                ("128 bean effect 3_000101000.safetensors", 0.2),
                ("ZIB-Image-Fun-Lora-Distill-2603_UDCAI_ComfyUI.safetensors", 0.2),
            ],
        ),
    ),
    SmokeTest("qwen_rapid_aio_v23", "legacy", qwen_rapid_prompt),
    SmokeTest(
        "krea2_raw_official",
        "krea2",
        lambda p: krea2_prompt(
            "krea2_raw_int8_convrot.safetensors",
            p,
            turbo=False,
        ),
    ),
    SmokeTest(
        "krea2_turbo_official",
        "krea2",
        lambda p: krea2_prompt(
            "krea2_turbo_int8_convrot.safetensors",
            p,
            turbo=True,
        ),
    ),
    SmokeTest(
        "krea2_turbo_textfusion_unlock",
        "krea2",
        lambda p: krea2_prompt(
            "krea2_turbo_int8_convrot.safetensors",
            p,
            turbo=True,
            loras=[("Krea2_TextFusion_Refusal_Reduction.safetensors", 1.0)],
        ),
    ),
    SmokeTest(
        "krea2_turbo_krea2t_enhancer_advanced",
        "krea2",
        lambda p: krea2_prompt(
            "krea2_turbo_int8_convrot.safetensors",
            p,
            turbo=True,
            enhancer={"strength": 1.0, "text_scale": 1.5},
        ),
    ),
    SmokeTest(
        "krea2_turbo_knp_v43_unlock_stack",
        "krea2",
        lambda p: krea2_prompt(
            "krea2_turbo_int8_convrot.safetensors",
            p,
            turbo=True,
            loras=[
                ("Krea2_TextFusion_Refusal_Reduction.safetensors", 1.0),
                ("KNP_000003000.safetensors", 1.0),
            ],
            scheduler="beta",
        ),
    ),
    SmokeTest(
        "krea2_redcraft_v3_int8",
        "krea2",
        lambda p: krea2_prompt(
            "redcraft23INT8INT4FP8_30Krea2.safetensors",
            p,
            turbo=True,
            steps=12,
        ),
    ),
    SmokeTest(
        "krea2_moody_mix_v5_int8",
        "krea2",
        lambda p: krea2_prompt(
            "moodyKrea2Mix_v50.safetensors",
            p,
            turbo=True,
            sampler="euler_ancestral",
        ),
    ),
    SmokeTest(
        "krea2_raw_snofs_v12",
        "krea2",
        lambda p: krea2_prompt(
            "krea2_raw_int8_convrot.safetensors",
            p,
            turbo=False,
            loras=[("snofs_krea_v1_2.safetensors", 1.0)],
        ),
    ),
    SmokeTest(
        "krea2_turbo_mystic_v3",
        "krea2",
        lambda p: krea2_prompt(
            "krea2_turbo_int8_convrot.safetensors",
            p,
            turbo=True,
            loras=[("MysticXXX_KREA2_v3.safetensors", 1.0)],
            steps=12,
            scheduler="beta",
        ),
    ),
    SmokeTest(
        "krea2_darkbeast_v3_int8",
        "krea2",
        lambda p: krea2_prompt(
            "darkBeast30BF16INT8_darkBeast330.safetensors",
            p,
            turbo=True,
            steps=12,
        ),
    ),
    SmokeTest(
        "krea2_raw_snofs_v13d",
        "krea2",
        lambda p: krea2_prompt(
            "krea2_raw_int8_convrot.safetensors",
            p,
            turbo=True,
            loras=[
                ("snofs_krea_v1_3D.safetensors", 1.0),
                ("krea2_raw_to_turbo_r256_comfy.safetensors", 1.0),
            ],
            clip_name="qwen3vl_4b_bf16.safetensors",
        ),
        required_nodes=("KreaTwoStageSampler",),
    ),
    SmokeTest(
        "krea2_raw_realism_engine_v31",
        "krea2",
        lambda p: krea2_prompt(
            "krea2_raw_int8_convrot.safetensors",
            p,
            turbo=True,
            loras=[
                ("krea2_turbo_lora_rank_64_bf16.safetensors", 0.6),
                ("realism_engine_krea2_v3.1.safetensors", 0.9),
            ],
            clip_name="qwen3vl_4b_bf16.safetensors",
        ),
        required_nodes=("VAEUtils_CustomVAELoader", "VAEUtils_VAEDecodeTiled"),
        required_choices=(
            (
                "VAEUtils_CustomVAELoader",
                "vae_name",
                "Wan2.1_VAE_upscale2x_imageonly_real_v1.safetensors",
            ),
        ),
    ),
    SmokeTest(
        "krea2_turbo_muse_v35_int8_extended",
        "krea2",
        lambda p: krea2_prompt(
            "museByStableYogi_v35Int8Extended.safetensors",
            p,
            turbo=True,
            vae_name="wanvideo/Wan2_1_VAE_bf16.safetensors",
            steps=12,
            cfg=1.5,
            scheduler="beta",
        ),
    ),
    SmokeTest(
        "krea2_turbo_fineporn_v4_int8",
        "krea2",
        lambda p: krea2_prompt(
            "finepornV4INT8NVFP4BF16_v4_int8.safetensors",
            p,
            turbo=True,
            clip_name="qwen3vl_4b_bf16.safetensors",
            steps=10,
            scheduler="beta",
        ),
    ),
    SmokeTest(
        "krea2_turbo_lustify_v10_int8",
        "krea2",
        lambda p: krea2_prompt(
            "lustify-v10-krea-turbo-int8_convrot.safetensors",
            p,
            turbo=True,
            vae_name="wanvideo/Wan2_1_VAE_bf16.safetensors",
        ),
        required_nodes=("UpscaleModelLoader",),
        required_choices=(
            (
                "UpscaleModelLoader",
                "model_name",
                "4x_NMKD-Superscale-SP_178000_G.pth",
            ),
        ),
    ),
    # Pre-Krea workflow-matrix asset coverage. Krea assets are grouped above.
    SmokeTest(
        "flux2_dev_turbo_lora",
        "matrix",
        lambda p: flux2_prompt(
            "flux2_dev_fp8mixed.safetensors",
            p,
            loras=[("Flux_2-Turbo-LoRA_comfyui.safetensors", 1.0)],
        ),
    ),
    SmokeTest(
        "flux2_klein_biglove_bf16",
        "matrix",
        lambda p: flux2_prompt("bigLove_klein2_bf16_pruned.safetensors", p),
    ),
    SmokeTest(
        "flux2_klein_pornmaster_turbo",
        "matrix",
        lambda p: flux2_prompt(
            "pornmasterFlux2Klein_v4.safetensors",
            p,
            loras=[("klein_9B_Turbo_r128.safetensors", 1.0)],
            steps=4,
        ),
    ),
    SmokeTest(
        "flux2_klein_darkbeast",
        "matrix",
        lambda p: flux2_prompt("darkBeast_dbkBlitzV15_pruned_bf16.safetensors", p),
    ),
    SmokeTest(
        "flux2_klein_unchained_lora",
        "matrix",
        lambda p: flux2_prompt(
            "flux-2-klein-9b.safetensors",
            p,
            loras=[("KLEIN-Unchained-V2.safetensors", 1.0)],
        ),
    ),
    SmokeTest(
        "flux2_klein_snofs_lora",
        "matrix",
        lambda p: flux2_prompt(
            "flux-2-klein-base-9b.safetensors",
            p,
            clip_name="qwen_3_8b.safetensors",
            loras=[("klein_snofs_v1_4.safetensors", 1.0)],
        ),
    ),
    SmokeTest(
        "flux2_klein_snofs_distilled",
        "matrix",
        lambda p: flux2_prompt(
            "snofsSexNudesAndOtherFunStuff_v14Distilled.safetensors",
            p,
            clip_name="qwen_3_8b.safetensors",
        ),
    ),
    SmokeTest(
        "flux2_klein_base_9b",
        "matrix",
        lambda p: flux2_prompt(
            "flux-2-klein-base-9b-fp8.safetensors",
            p,
            vae_name="full_encoder_small_decoder.safetensors",
        ),
    ),
    SmokeTest(
        "flux2_klein_9b_distilled",
        "matrix",
        lambda p: flux2_prompt(
            "flux-2-klein-9b-fp8.safetensors",
            p,
            vae_name="full_encoder_small_decoder.safetensors",
        ),
    ),
    SmokeTest(
        "qwen_2512_jib_mix",
        "matrix",
        lambda p: qwen_image_prompt("jibMixQwen_v60.safetensors", p),
    ),
    SmokeTest(
        "qwen_2512_qwen4play",
        "matrix",
        lambda p: qwen_image_prompt(
            "qwen_image_2512_bf16.safetensors",
            p,
            clip_name="qwen_2.5_vl_7b.safetensors",
            loras=[
                ("Qwen4Play-2512.1_e10.safetensors", 1.0),
                ("Qwen-Image-2512-Lightning-8steps-V1.0-fp32.safetensors", 1.0),
            ],
            steps=4,
            cfg=1.0,
        ),
    ),
    SmokeTest(
        "qwen_base_snofs_lora",
        "matrix",
        lambda p: qwen_image_prompt(
            "qwen-image-Q8_0.gguf",
            p,
            gguf=True,
            loras=[("Qwen_Snofs_1_3.safetensors", 1.0)],
            cfg=4.0,
        ),
    ),
    SmokeTest(
        "qwen_2512_original_lightning",
        "matrix",
        lambda p: qwen_image_prompt(
            "qwen_image_2512_fp8_e4m3fn.safetensors",
            p,
            loras=[("Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors", 1.0)],
            steps=4,
            cfg=1.0,
        ),
    ),
    SmokeTest(
        "qwen_base_mcnl_lora",
        "matrix",
        lambda p: qwen_image_prompt(
            "qwen_image_fp8_e4m3fn.safetensors",
            p,
            loras=[("qwen_MCNL_v1.0.safetensors", 1.0)],
            cfg=2.5,
        ),
    ),
    SmokeTest(
        "qwen_image_edit_2511",
        "matrix",
        lambda p: qwen_image_prompt(
            "qwen_image_edit_2511_bf16.safetensors",
            p,
            loras=[("Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors", 1.0)],
            edit=True,
            steps=4,
        ),
    ),
    SmokeTest(
        "z_image_base_pornmaster",
        "matrix",
        lambda p: z_image_prompt(
            "pornmasterZImage_baseV1_bf16.safetensors",
            p,
            loras=[
                ("Z-Image-Fun-Lora-Distill-8-Steps-2603-ComfyUI.safetensors", 0.5),
                ("Z-Image-Fun-Lora-Distill-4-Steps-2603-ComfyUI.safetensors", 0.5),
            ],
            steps=4,
        ),
    ),
    SmokeTest(
        "z_image_base_moody_wild",
        "matrix",
        lambda p: z_image_prompt("moodyWildMixZIBZID_v40BASE40STEPSCFG4_fp16_full.safetensors", p),
    ),
    SmokeTest(
        "z_image_base_redcraft",
        "matrix",
        lambda p: z_image_prompt("redcraftERNIERedmix_zibDistilled.safetensors", p),
    ),
    SmokeTest(
        "z_image_base_original",
        "matrix",
        lambda p: z_image_prompt("z_image_bf16.safetensors", p, cfg=4.0),
    ),
    SmokeTest(
        "z_image_turbo_stable_yogi",
        "matrix",
        lambda p: z_image_prompt("zimageTurboNSFWBy_2602NSFWBF16.safetensors", p, steps=1),
    ),
    SmokeTest(
        "z_image_turbo_nsfw_master",
        "matrix",
        lambda p: z_image_prompt(
            "z_image_turbo_bf16.safetensors",
            p,
            loras=[("NSFW_master_ZIT_000017532.safetensors", 1.0)],
            steps=1,
        ),
    ),
    SmokeTest(
        "z_image_turbo_photorealistic",
        "matrix",
        lambda p: z_image_prompt(
            "zImageTurboNSFW_82BF16.safetensors",
            p,
            clip_name="Qwen3-4b-Z-Image-Turbo-AbliteratedV1.safetensors",
            steps=1,
        ),
    ),
    SmokeTest(
        "z_image_turbo_darkbeast",
        "matrix",
        lambda p: z_image_prompt("darkBeast_dbzit9DIMRclaw.safetensors", p, steps=1),
    ),
    SmokeTest(
        "z_image_turbo_moody_pro",
        "matrix",
        lambda p: z_image_prompt("moodyProMix_zitV10R1DPO.safetensors", p, steps=1),
    ),
    SmokeTest(
        "z_image_turbo_mystic_lora",
        "matrix",
        lambda p: z_image_prompt(
            "z_image_turbo_bf16.safetensors",
            p,
            loras=[("Mystic-XXX-ZIT-V7.safetensors", 1.0)],
            steps=1,
        ),
    ),
    SmokeTest(
        "z_image_turbo_original",
        "matrix",
        lambda p: z_image_prompt("z_image_turbo_bf16.safetensors", p, steps=1),
    ),
]


KNOWN_EXCLUSIONS = {
    "HunyuanImage-3.0-Instruct-Distil-NF4-v2": (
        "excluded from routine 24 GB smoke tests after a documented host-OOM "
        "container kill during block-swap generation"
    ),
    "Wan 2.2 I2V": (
        "video workflow with required image input; covered separately by its "
        "canonical workflow rather than this one-PNG dependency suite"
    ),
    "Qwen3.5-35B-A3B VLM": (
        "captioning/VLM dependency, not an image-generation model"
    ),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8188")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--id", help="Output prefix run ID; defaults to a UTC timestamp")
    parser.add_argument("--only", nargs="*", help="Run only named tests")
    parser.add_argument("--skip", nargs="*", default=[], help="Skip named tests")
    parser.add_argument(
        "--group",
        action="append",
        choices=sorted({test.group for test in TESTS}),
        help="Run only a test group; may be repeated",
    )
    parser.add_argument("--list", action="store_true", help="List tests and known exclusions")
    args = parser.parse_args()

    if args.list:
        for test in TESTS:
            print(f"{test.group}\t{test.name}")
        for name, reason in KNOWN_EXCLUSIONS.items():
            print(f"excluded\t{name}\t{reason}")
        return 0

    names = [test.name for test in TESTS]
    unknown = (set(args.only or []) | set(args.skip)) - set(names)
    if unknown:
        parser.error(f"unknown test names: {', '.join(sorted(unknown))}")

    only = set(args.only or [])
    skip = set(args.skip)
    groups = set(args.group or [])
    selected = [
        test
        for test in TESTS
        if (not only or test.name in only)
        and test.name not in skip
        and (not groups or test.group in groups)
    ]
    if not selected:
        parser.error("no tests selected")

    run_id = args.id or time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    results = {}
    object_info = get_json(args.base_url, "/object_info")
    started = time.monotonic()
    for index, test in enumerate(selected, start=1):
        prefix = f"smoke_{run_id}_{test.name}"
        print(f"[{index}/{len(selected)}]", flush=True)
        test_started = time.monotonic()
        try:
            validate_runtime_dependencies(test, object_info)
            path, metrics = run_prompt(
                args.base_url,
                test.name,
                test.factory(prefix),
                test.timeout_s,
                args.output_dir,
            )
            results[test.name] = {
                "ok": True,
                "seconds": round(time.monotonic() - test_started, 1),
                "file": path,
                "metrics": metrics,
            }
        except Exception as exc:
            print(f"FAIL {test.name}: {exc}", flush=True)
            results[test.name] = {
                "ok": False,
                "seconds": round(time.monotonic() - test_started, 1),
                "error": str(exc),
            }
        finally:
            free_memory(args.base_url)
            time.sleep(1)

    elapsed = time.monotonic() - started
    passed = sum(item["ok"] for item in results.values())
    print(
        f"SUMMARY {passed}/{len(results)} tests passed in {elapsed:.1f}s",
        flush=True,
    )
    print(json.dumps(results, indent=2, sort_keys=True), flush=True)
    return 1 if passed != len(results) else 0


if __name__ == "__main__":
    sys.exit(main())
