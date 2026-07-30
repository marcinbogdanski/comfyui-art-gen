# Ideas

Future workflow-control ideas. These are not settled specs.

## Negative Prompt Routing

When a workflow supports negative prompting, route the structured negative
prompt into the negative `CLIPTextEncode` node. A likely rule is to use the
negative node only when exactly one `CLIPTextEncode` has `Negative` in its
display name.

## Dynamic Trigger Words

Allow workflows to map semantic prompt keywords to model-specific trigger words.
For example, a prompt keyword such as `doggy` could map to a LoRA/model trigger
token such as `d00gy` when the workflow metadata defines that mapping.

## Dynamic LoRA Activation

Allow workflows to include prepared LoRA loader nodes that are disabled or
neutral by default. If a structured prompt keyword maps to a supported LoRA,
the script could enable or configure that LoRA node for the run.

## Style LoRA Activation

Allow prompts to request a style through a structured style keyword, such as
`style: anime`. The workflow metadata would map supported style values to
model-specific LoRA nodes, and the script would activate the matching LoRA for
that run.

## ControlNet / Reference Activation

Allow workflows to include prepared disabled-by-default ControlNet or equivalent
reference branches. If a structured prompt keyword maps to a supported reference
asset, the script could load the matching `.png` and enable the branch.

# ControlNet Notes

Research notes for adding pose/structure control to the current model families.
These are not settled workflow specs.

### Generic Pattern

The common high-level pattern is:

1. Load a reference image or pose guide.
2. Convert it to a control image with a preprocessor, such as OpenPose/DWpose,
   Canny, depth, HED, lineart, softedge, MLSD, or scribble.
3. Feed that control image into a model-family-specific ControlNet, union
   control model, model patch, LoRA, or reference-conditioning branch.
4. Tune control strength/context scale so the pose is followed without
   collapsing style or character variation.

Pose control usually uses OpenPose/DWpose maps. For two-person body-contact
poses, verify the preprocessor output visually before judging the model; bad or
incomplete skeletons will produce misleading failures.

### Qwen-Image-2512

Qwen-Image-2512 has a dedicated ControlNet model, not just older Qwen-Image
control examples.

Concrete sources:

- Hugging Face: https://huggingface.co/alibaba-pai/Qwen-Image-2512-Fun-Controlnet-Union
  - `Qwen-Image-2512-Fun-Controlnet-Union.safetensors` is described as
    ControlNet weights for Qwen-Image-2512.
  - Supported controls include Canny, HED, Depth, Pose, MLSD, Scribble, and
    Gray.
  - The model card says it can be used like a standard ControlNet and supports
    inpainting mode.
- Comfy workflow template:
  https://comfy.org/ja/workflows/image_qwen_Image_2512_controlnet/
  - Explicitly labels the model as Qwen-Image 2512.
  - Describes uploading an image and choosing Canny, HED, Depth, Pose, MLSD,
    Scribble, or Grayscale.
- Comfy Qwen-Image-2512 docs:
  https://docs.comfy.org/tutorials/image/qwen/qwen-image-2512
  - Confirms Qwen-Image-2512 is the December update model and points users to
    current workflow templates after updating ComfyUI.

Likely experiment target: start with `qwen_2512_lora_snofs.json`, because it is
currently the strongest text-only workflow for two-person pose adherence.

### Qwen-Image Base

Related Qwen-Image control sources:

- Comfy blog:
  https://blog.comfy.org/p/comfyui-now-supports-qwen-image-controlnet
  - Mentions Qwen-Image DiffSynth ControlNets and Qwen-Image Union DiffSynth
    LoRA.
  - The union LoRA supports lineart, softedge, normal, and openpose.
- Comfy Qwen-Image docs:
  https://docs.comfy.org/tutorials/image/qwen/qwen-image
  - Lists Qwen-Image control options and model storage locations.

Do not assume older Qwen-Image control workflows are directly identical to
Qwen-Image-2512. Prefer the dedicated 2512 source above when working with 2512.

### Z-Image / Z-Image Turbo

Z-Image Turbo has Z-Image-specific union control support.

Useful sources:

- ZImageFunControlnet built-in node docs:
  https://docs.comfy.org/built-in-nodes/ZImageFunControlnet
- RunComfy Z-Image ControlNet workflow notes:
  https://www.runcomfy.com/comfyui-workflows/z-image-controlnet-in-comfyui-controlled-image-generation
- Alibaba PAI Z-Image Turbo ControlNet Union:
  https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union
- Alibaba PAI Z-Image Turbo ControlNet Union 2.1:
  https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.1

The common workflow shape is reference image -> selected preprocessor/control
type -> Z-Image union control/model patch -> sampler.

### Flux 2 / Klein

Flux 2 Klein appears less like a classic ControlNet path. Current practical
approaches are more reference/edit-conditioning oriented: provide a stick
figure, pose map, or depth map as a reference image and prompt the model to
match it.

Useful sources:

- Flux.2 Klein workflow notes:
  https://comfyui.nomadoor.net/en/basic-workflows/flux-2-klein/
  - Describes ControlNet-like pose use via image editing/reference input rather
    than classic ControlNet mechanics.
- Black Forest Labs FLUX.2 repo:
  https://github.com/black-forest-labs/flux2

Treat Flux 2 pose control as a separate experiment from Qwen/Z-Image control
branches. It may require a different workflow shape.

### General ControlNet References

- Comfy Pose ControlNet example:
  https://docs.comfy.org/tutorials/controlnet/pose-controlnet-2-pass
- Comfy ControlNet overview:
  https://docs.comfy.org/tutorials/controlnet/controlnet
- ControlNet paper:
  https://arxiv.org/abs/2302.05543
