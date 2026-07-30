# Adding a Model or LoRA

## Goal

Add a new model or LoRA with enough source context, local files, and a simplified
reference workflow that a future agent can understand the source and reproduce
the selected example as closely as practical.

This is a goal and decision process, not a replacement for existing rules.
Before acting, read:

- `AGENTS.md`
- `workflows/README.md`
- `/mnt/data/comfyui/models/MODEL_SUMMARY_RULES.md`
- `/mnt/data/comfyui/models/MODEL_SUMMARY.md`

The control repo and `/mnt/data/comfyui/models` have different jobs. Keep source
artifacts in the model archive according to its rules, and keep local runnable
workflow references in this repo.

## Start With Research Only

When asked to add a model or LoRA from only a URL or a loose target, start with
a research-only phase. In this phase, read the relevant instructions and source
pages, inspect available metadata/workflows, and identify likely local scope.
Do not download weights, create sidecars, edit workflows, rename files, delete
files, stage files, or commit.

Temporary files under `/tmp` are acceptable for inspecting source metadata or
downloaded reference artifacts during research. Do not create durable repo files
or model-archive files until the proposed scope is accepted and the user gives
an explicit implementation instruction. Scope acceptance alone is still
discussion/planning, not permission to execute.

End the research phase with a concise proposed plan and scope manifest:

```text
Candidate:
- URL:
- Model or LoRA name:
- Exact version:
- Base model:
- Official/source page:
- Best source image or workflow:
- Has embedded workflow metadata:
- Extra models or LoRAs required:
- Local files likely needed:
- Proposed canonical workflow path:
- Proposed archive sidecars:
- Risks or ambiguities:

Proposed scope:
control repo:
- ...

model archive:
- ...

Out of scope:
- ...
```

The scope section should be concrete enough to guide staging and review. Include
shared-file hunk limits and explicit exclusions when nearby work may exist. For
example:

```text
TASK: Add MCNL original Qwen workflow

IN SCOPE
control repo:
- models/qwen-image/base/nsfw/qwen-mcnl.md
- workflows/qwen-image/base/nsfw/qwen_base_lora_mcnl.json
- scripts/download_models/qwen-image.sh

model archive:
- diffusion_models/qwen_image_fp8_e4m3fn.md
- diffusion_models/qwen_image_fp8_e4m3fn.html
- diffusion_models/qwen_image_fp8_e4m3fn.json
- loras/qwen_MCNL_v1.0.md
- loras/qwen_MCNL_v1.0.png
- MODEL_SUMMARY.md, only MCNL/Qwen FP8 hunks
- .gitignore, only qwen_image_fp8_e4m3fn weight ignore

OUT OF SCOPE
- SNOFS
- Qwen4Play
- `.work.json`
- fallback workflows
- memory unless explicitly requested
- any weights in git
```

Implementation may begin only after the proposed scope is accepted or modified
and the user gives an explicit implementation instruction, or when the user's
message clearly combines both scope approval and execution. If the user already
provides an explicit implementation plan and asks for execution, follow it, but
still keep edits and staging within that stated scope.

## Recommended Task Shape

For model/LoRA additions that touch both this repo and the model archive, prefer
this shape:

1. Research-only pass: classify the candidate, select the best source
   image/workflow, resolve likely filename mappings, and produce the proposed
   scope manifest above.
2. Archive implementation: download and verify weights, save source/reference
   artifacts, create sidecars, and update archive summary/ignore files under
   `/mnt/data/comfyui/models` only.
3. Control implementation: create or update the local runnable workflow and
   short control-repo documentation only.
4. Coordination: the main agent reviews both outputs and leaves unrelated
   changed, ignored, or untracked files alone.
5. Stage: stage the model archive and control repo separately, limited to the
   exact accepted scope. This staged state is the final form for human review.
6. Validation: run local staged checks, then use fresh-context sub-agent audits
   for the focused archive checklist and the final broad two-repo staged review.

Steps 2 and 3 may be done by focused workers when useful. Give each worker one
write scope only: either the model archive or the control repo, not both. A
worker that implemented a scope is not the independent validator for that same
scope.

The final broad review should be allowed to fail. If it finds an issue, fix the
staged state and rerun the broad review before committing.

## Source Selection

Prefer sources in the order defined by `AGENTS.md`: user-provided link, then
official or popular upstream source, then mirrors only when needed and
documented.

Identify the available model files and variants before downloading. Prefer the
source workflow's exact named model file when available. If the exact source
filename is local-only, map it to the closest source-listed file by model
version, precision, size, hash, and source notes. If the mapping is unclear,
pause and ask.

Avoid treating a Civitai "primary" file as canonical when its size or metadata
is suspicious for the model family. Explain the discrepancy and choose the
variant that best matches the source workflow or pause if uncertain.

## Reference Workflow Selection

Browse the available source workflows or source images. If there is only one
usable source workflow, inspect it. If there are multiple image examples, inspect
the first one first.

When using a workflow-bearing image as the reference, first save or extract the
exact source artifact that contains the workflow metadata. Use that extracted
workflow as the source of truth before editing the local simplified workflow. Do
not rely only on website summary metadata when full workflow metadata is
available.

Use a source workflow when it meets these requirements:

- it uses the canonical or clearly mapped target model option;
- it has no required img2img/reference input unless that input is available and
  intended for the local reference;
- it has no extra LoRAs or models beyond the target source and normal support
  files, unless those dependencies are part of the target source context;
- the initial generation path is clear enough to reproduce locally.

If the first workflow does not meet these requirements, inspect a few of the
first source images/workflows and look for a clean example that can be adapted.

Pause and report to the user when:

- every candidate needs unavailable image/reference inputs;
- every candidate depends on unrelated LoRAs or extra models;
- source-local filenames cannot be mapped confidently;
- examples are dominated by postprocessing/upscalers and the initial generation
  path cannot be separated;
- the best candidate uses a heavily quantized or otherwise suspicious model file
  and the canonical mapping is ambiguous;
- no source workflow or workflow-bearing reference image is available.

## Implementation Shape

When requirements are met:

- archive source/reference artifacts under `/mnt/data/comfyui/models` following
  `MODEL_SUMMARY_RULES.md`;
- after downloading a source/reference image, verify the actual file type from
  its file header and use the matching extension; do not trust the source URL
  extension;
- download required model files into `/mnt/data/comfyui/models`, keeping weights
  out of git and documenting repeatable download commands in this repo when
  useful;
- create a simplified local workflow in `workflows/` that uses plain nodes where
  practical and produces the selected reference image as closely as practical;
- save canonical workflow `.json` files pretty-printed with 2-space indentation
  (the ComfyUI GUI "Save" default, matching the rest of `workflows/`). When
  editing an existing workflow, preserve its formatting and change only the
  needed nodes; do not `jq`/reserialize a whole workflow just for a small edit,
  as that produces noisy diffs;
- diff the exact source workflow against the local workflow while simplifying,
  and account for generation-affecting differences that remain;
- preserve exact source prompt, seed, sampler, steps, CFG, dimensions, model
  mapping, VAE/text encoder choices, and negative conditioning where possible;
- document intentional substitutions, such as local filename mappings or a
  missing source VAE replaced by an available local VAE;
- add exactly one plain ComfyUI `Note` node titled `Metadata` to the local
  workflow. Its body must start with JSON front matter, followed by a line
  containing only `---`, followed by concise free-form source notes. Keep this
  workflow note to source/reference facts only; if more information seems useful
  there, ask the human first;
- include `trigger_words` and `trigger_required` in the `Metadata` JSON. Use
  `trigger_words` as a list of source-documented trigger or activation words.
  Use `trigger_required` as one of `required`, `optional`, `no`, or `unknown`.
  Use `no` when the source explicitly lists no trigger words or has an empty
  trainedWords/activation-keyword list. Use `unknown` only when source trigger
  metadata cannot be found;
- when `trigger_required` is `required`, `scripts/workflow_prompt.py` prepends
  the listed `trigger_words` to scripted prompts. Do not add graph concat nodes
  just to inject trigger words unless the user explicitly asks for graph-side
  trigger handling;
- keep `.work.json` copies local and ignored unless explicitly asked to track
  them.

Metadata note example:

```text
{
  "trigger_words": ["99bsy99"],
  "trigger_required": "required"
}
---
Reference image: https://civitai.red/images/120285584
Trigger word: 99bsy99
```

Pixel-perfect reproduction is not required. The local workflow should generate
the same image in the practical sense: same subject, composition, style, and
settings, with differences explained by model-file, VAE, precision, runtime, or
postprocessing substitutions.

## Validation

For every new or edited canonical GUI workflow `.json`, run the frontend smoke
test before marking the workflow ready:

```bash
python3 scripts/workflow_prompt.py -w workflows/path/to/workflow.json
```

This is a required check: it loads the saved GUI workflow in the actual ComfyUI
frontend, converts it with `app.graphToPrompt()`, submits the converted prompt
to `/prompt` from Python, and waits for ComfyUI history success. A hand-written
or separately derived API prompt smoke test is not a substitute. Keep tests
small enough for the target GPU when the workflow design allows that, and record
the frontend smoke result and output path in the relevant model doc. If this
required check cannot be run, stop and report the blocker and next action
instead of presenting the workflow as ready.

The metadata note should have the expected shape:

- there is exactly one `Note` node titled `Metadata`;
- the note text contains a `---` separator after the JSON front matter;
- the front matter parses as JSON;
- `trigger_words` is a list;
- `trigger_required` is one of `required`, `optional`, `no`, or `unknown`.

Do not add a newly created workflow to `workflows/test_matrix.txt` unless the
human asks for it or the accepted scope includes it; the matrix is a curated
regression set, not an automatic inventory of all workflows.

For the current complete `workflows/test_matrix.txt` set, use one required
no-generation preflight command:

```bash
python3 scripts/workflow_queue.py --prompt prompts/prompt1.md --dry-run --batch 1 --seed 1 --id dryrun_matrix
```

For workflows included in the matrix, this validates the
prompt/metadata/batch/seed/output assumptions encoded in
`scripts/workflow_prompt.py` and runs frontend conversion without submitting
generation jobs.

After the smoke test, stop for human review unless the user has asked for
commits or further automation.

After staging model-archive files and before asking the human for review or
committing, re-read `/mnt/data/comfyui/models/MODEL_SUMMARY_RULES.md` and
execute its staged changes checklist against the staged/index version of the
files.

For two-repo changes, run two fresh-context sub-agent validations after staging:

- focused model-archive audit: verify the staged archive set against
  `MODEL_SUMMARY_RULES.md`, including source artifacts, sidecar JSON, ignored
  weights, exact file types, and surrounding unstaged/untracked state;
- broad two-repo audit: verify both repos together, including staged file
  exclusivity and completeness, no `.work.json` or weights staged, workflow/doc
  consistency, archive/control boundary rules, and frontend smoke-test claims.

Do not treat a passing focused archive audit as a substitute for the broad
two-repo audit. If either audit fails, fix the issue, restage the intended files,
and rerun the failed audit before committing.
