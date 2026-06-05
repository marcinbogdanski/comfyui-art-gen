# ComfyUI Workflow Examples

Curated workflow copies from the live ComfyUI workspace:

```text
/mnt/data/comfyui/user/default/workflows
```

Only tested/canonical no-suffix workflow JSON files are copied here. Some are
copied from the live workspace; current original model baselines can also be
raw official Comfy-Org workflow templates. Live GUI work files and API prompt
graphs remain in ComfyUI and are not copied by default.

Suffix convention in the live workspace:

- `.json`: fixed/tested GUI-loadable workflow
- `.work.json`: editable GUI work copy
- `.api.json`: executable API prompt graph for `POST /prompt`

Tracking convention:

- Track canonical no-suffix `.json` workflows.
- Keep `.work.json` files as ignored local GUI work copies. They may be copied
  or synced locally, but they should not be staged or committed unless a request
  explicitly says to track the `.work.json` file itself.
- Do not interpret broad requests like "stage related workflow files" as
  permission to force-add ignored `.work.json` files.

Model files and generated outputs stay under `/mnt/data/comfyui` and are not
stored in git.

## Metadata Note

Every canonical workflow `.json` should contain exactly one plain ComfyUI `Note`
node titled `Metadata`. Keep this as workflow metadata, not as graph logic.

The note body starts with JSON front matter, then a separator line containing
only `---`, then free-form source notes:

```text
{
  "trigger_words": ["99bsy99"],
  "trigger_required": "required"
}
---
Reference image: https://example.invalid/image
Trigger word: 99bsy99
```

Required fields:

- `trigger_words`: list of source-documented trigger or activation words.
- `trigger_required`: one of `required`, `optional`, `no`, or `unknown`.

Use `no` when the source explicitly lists no trigger words or has an empty
trainedWords/activation-keyword list. Use `unknown` only when source trigger
metadata cannot be found. `scripts/workflow_prompt.py` prepends
`trigger_words` to scripted prompts only when `trigger_required` is `required`.

## Frontend Smoke Test

Before a new or edited canonical GUI workflow `.json` is considered ready for
review, validate it with `scripts/workflow_prompt.py`. The script loads the GUI
workflow in Chromium, calls the actual ComfyUI frontend `app.graphToPrompt()`
path, submits the converted prompt to ComfyUI from Python, and waits for history
success. A hand-written or separately derived API prompt graph is not a
substitute for this check.

```bash
python3 scripts/workflow_prompt.py -w workflows/path/to/workflow.json
```

For conversion-only debugging, use `scripts/workflow_prompt.py --dry-run` or
call `scripts/gui_workflow_convert.mjs` directly with `--output`; the MJS script
only writes converted API prompt JSON.

## Matrix Dry Run

Before treating the complete matrix as ready, run the workflow queue in dry-run
mode:

```bash
python3 scripts/workflow_queue.py --prompt prompts/prompt1.md --dry-run
```

This uses `workflows/test_matrix.txt` by default. It runs each workflow through
`scripts/workflow_prompt.py`, validates the script assumptions with assertions,
applies scripted prompt/metadata/batch/seed/output mutations when requested, and
loads the resulting workflow through the real ComfyUI frontend converter. It
does not submit converted prompts, so it does not queue generation jobs.
