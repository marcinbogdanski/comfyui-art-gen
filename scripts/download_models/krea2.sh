#!/usr/bin/env bash
set -euo pipefail

MODELS_DIR="${COMFYUI_MODELS_DIR:-${COMFYUI_PATH:-/workspace/ComfyUI}/models}"
REVISION="952f49d49653cb42e7d6cf7cbfad74738073ec7d"
BASE_URL="https://huggingface.co/Comfy-Org/Krea-2/resolve/${REVISION}"
WAN_VAE_URL="https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1_VAE_bf16.safetensors"
RANK256_REVISION="c28120b6ebfff2629d475dcde0bbdbf45cbc06e9"
RANK256_URL="https://huggingface.co/Kutches/Kr3a/resolve/${RANK256_REVISION}/krea2_raw_to_turbo_r256_comfy.safetensors"
REALISM_VAE_REVISION="62184b03592269cfcc4bdcdb22178e19229a23b6"
REALISM_VAE_URL="https://huggingface.co/Osrivers/Wan2.1_VAE_upscale2x_imageonly_real_v1.safetensors/resolve/${REALISM_VAE_REVISION}/Wan2.1_VAE_upscale2x_imageonly_real_v1.safetensors"
NMKD_REVISION="f6bace545e358eab5491f8f39b90a2dd42e8cc77"
NMKD_URL="https://huggingface.co/uwg/upscaler/resolve/${NMKD_REVISION}/ESRGAN/4x_NMKD-Superscale-SP_178000_G.pth"

mkdir -p "${MODELS_DIR}/diffusion_models"
mkdir -p "${MODELS_DIR}/loras"
mkdir -p "${MODELS_DIR}/text_encoders"
mkdir -p "${MODELS_DIR}/vae"
mkdir -p "${MODELS_DIR}/vae/wanvideo"
mkdir -p "${MODELS_DIR}/upscale_models"

download() {
  local url=$1
  local relative_path=$2
  local sha256=$3
  local auth_header=${4:-}
  local target="${MODELS_DIR}/${relative_path}"

  if [[ -f "${target}" ]] &&
    printf '%s  %s\n' "${sha256}" "${target}" | sha256sum -c - >/dev/null 2>&1; then
    echo "Already verified: ${target}"
    return
  fi

  local curl_args=(-fL -C - --retry 5 --retry-delay 5 -o "${target}")
  if [[ -n "${auth_header}" ]]; then
    curl_args+=(-H "${auth_header}")
  fi
  curl "${curl_args[@]}" "${url}"
  printf '%s  %s\n' "${sha256}" "${target}" | sha256sum -c -
}

download \
  "${BASE_URL}/diffusion_models/krea2_raw_int8_convrot.safetensors" \
  "diffusion_models/krea2_raw_int8_convrot.safetensors" \
  "5585a4a38c4bcfb6fde2d480a4aa6edf7f665721ebde56d30662c35a45f5fa5c"
download \
  "${BASE_URL}/diffusion_models/krea2_turbo_int8_convrot.safetensors" \
  "diffusion_models/krea2_turbo_int8_convrot.safetensors" \
  "8e4eeda70dd5037ab1ba2bef6b417f9f901e26093117cf397f741fc1fdaaf3f1"
download \
  "${BASE_URL}/text_encoders/qwen3vl_4b_fp8_scaled.safetensors" \
  "text_encoders/qwen3vl_4b_fp8_scaled.safetensors" \
  "54bd5144df0bbc25dd6ccadfcb826b521445a1b06ae5a42570bdd2974ca87094"
download \
  "${BASE_URL}/text_encoders/qwen3vl_4b_bf16.safetensors" \
  "text_encoders/qwen3vl_4b_bf16.safetensors" \
  "36f3ff447ef59201722e8f9ce6020c9819fdcfba6aa2608c4e09b1c0ce114e34"
download \
  "${BASE_URL}/vae/qwen_image_vae.safetensors" \
  "vae/qwen_image_vae.safetensors" \
  "a70580f0213e67967ee9c95f05bb400e8fb08307e017a924bf3441223e023d1f"
download \
  "${WAN_VAE_URL}" \
  "vae/wanvideo/Wan2_1_VAE_bf16.safetensors" \
  "1ab9a32cc2c740f6e39d80d367ce5dcc28db8c71b79b28670546b8973e9d75f9"
download \
  "${BASE_URL}/loras/krea2_turbo_lora_rank_64_bf16.safetensors" \
  "loras/krea2_turbo_lora_rank_64_bf16.safetensors" \
  "db8c5bae0a415d448da9d842111d6e51f7d32e47143a3118eb267e5c4773de87"
download \
  "${RANK256_URL}" \
  "loras/krea2_raw_to_turbo_r256_comfy.safetensors" \
  "e9e99b6f28a8fcae4ad7d0298c185b23af71f5fc85ad1819d624724c98df4892"
download \
  "${REALISM_VAE_URL}" \
  "vae/Wan2.1_VAE_upscale2x_imageonly_real_v1.safetensors" \
  "2413554bbec24215185662d009893cf4666b8e777efece2d895e03e1a6b63e06"
download \
  "${NMKD_URL}" \
  "upscale_models/4x_NMKD-Superscale-SP_178000_G.pth" \
  "1d1b0078fe71446e0469d8d4df59e96baa80d83cda600d68237d655830821bcc"

if [[ -z "${CIVITAI_API_KEY:-}" ]]; then
  echo "CIVITAI_API_KEY is required for the Krea 2 community downloads." >&2
  exit 1
fi

CIVITAI_AUTH="Authorization: Bearer ${CIVITAI_API_KEY}"

download \
  "https://civitai.com/api/download/models/3147117?fileId=3027612" \
  "loras/KNP_000003000.safetensors" \
  "6ec564e04eed317ae24093b4907004ac59a7c528d19d025bb41b4d719c4d16ec" \
  "${CIVITAI_AUTH}"
download \
  "https://civitai.com/api/download/models/3139241?fileId=3019607" \
  "diffusion_models/redcraft23INT8INT4FP8_30Krea2.safetensors" \
  "a5dd85f90f873f80e2b07cb8d06fd6011755fcfb22434dfbb04155345eaa44b9" \
  "${CIVITAI_AUTH}"
download \
  "https://civitai.com/api/download/models/3151928?fileId=3032723" \
  "diffusion_models/moodyKrea2Mix_v50.safetensors" \
  "d6ecc9e916c4920a2cce762cabe737d87ba3cb987e10443cb48e777cbd747a37" \
  "${CIVITAI_AUTH}"
download \
  "https://civitai.com/api/download/models/3172362?fileId=3059229" \
  "loras/snofs_krea_v1_2.safetensors" \
  "e36d715ba3b0b56b0215cc30293659e344a9da60909035cd523c3da62c0c3a3e" \
  "${CIVITAI_AUTH}"
download \
  "https://civitai.com/api/download/models/3116175?fileId=2996388" \
  "loras/MysticXXX_KREA2_v3.safetensors" \
  "3437fb03a86c0a3be180b3da67f6a042a13d928d79d46b8835c3d04be6ec4382" \
  "${CIVITAI_AUTH}"
download \
  "https://civitai.com/api/download/models/3173268?fileId=3053854" \
  "diffusion_models/darkBeast30BF16INT8_darkBeast330.safetensors" \
  "b60cb86fc1c8a84f37991c0c4d9bffe9ba4a2ce6ae1ec26ff2691bb21d87c433" \
  "${CIVITAI_AUTH}"
download \
  "https://civitai.com/api/download/models/3125118?fileId=3005583" \
  "loras/Krea2_TextFusion_Refusal_Reduction.safetensors" \
  "84ec722ddab93f6489c5315bca25de5dd1a7b7ec5045a3c4ce2f97f62e54e8e6" \
  "${CIVITAI_AUTH}"
download \
  "https://civitai.com/api/download/models/3220691?fileId=3102670" \
  "loras/snofs_krea_v1_3D.safetensors" \
  "5f373c7d5320d6dc83468393f141657d98667c77feaf5e313326dce68cd76a50" \
  "${CIVITAI_AUTH}"
download \
  "https://civitai.com/api/download/models/3109006?fileId=2988982" \
  "loras/realism_engine_krea2_v3.1.safetensors" \
  "a6712629445a2e91a616568e82befa8c8c7518e891a0f7c9918138634b5b54a5" \
  "${CIVITAI_AUTH}"
download \
  "https://civitai.com/api/download/models/3258954?fileId=3142504" \
  "diffusion_models/museByStableYogi_v35Int8Extended.safetensors" \
  "53d9a2aa388b0ac1d6cc031cead1a2ebc887867c11c489ed463d674a4e1939af" \
  "${CIVITAI_AUTH}"
download \
  "https://civitai.com/api/download/models/3187539?fileId=3068196" \
  "diffusion_models/finepornV4INT8NVFP4BF16_v4_int8.safetensors" \
  "7d23304de81fad36b7dfc696befe4354560ca4e04cd26ce1099f388a3aa48ef" \
  "${CIVITAI_AUTH}"
download \
  "https://civitai.com/api/download/models/3112728?fileId=2996235" \
  "diffusion_models/lustify-v10-krea-turbo-int8_convrot.safetensors" \
  "0505412ed2ac568286c4bf43f8ace93f9f5a6dd7a607f47f1912a68767e6900d" \
  "${CIVITAI_AUTH}"
