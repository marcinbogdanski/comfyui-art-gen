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
