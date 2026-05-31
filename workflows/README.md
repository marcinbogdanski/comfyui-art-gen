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

## Frontend Smoke Test

Before a new or edited canonical GUI workflow `.json` is considered ready for
review, validate it with `scripts/gui_workflow_smoke.mjs`. The script loads a
GUI workflow in Chromium, calls the actual ComfyUI frontend
`app.graphToPrompt()` path, and can submit the converted prompt to ComfyUI. A
hand-written or separately derived API prompt graph is not a substitute for this
check.

Run it with the pinned Playwright Docker image so no browser is installed on the
host:

```bash
docker run --rm --network host --ipc=host \
  -v /home/user/art-generation/art-gen-ctrl:/work:ro \
  -w /tmp \
  mcr.microsoft.com/playwright:v1.57.0-noble \
  sh -lc 'npm init -y >/dev/null &&
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install playwright@1.57.0 >/dev/null &&
    cp /work/scripts/gui_workflow_smoke.mjs . &&
    node gui_workflow_smoke.mjs --submit --wait /work/workflows/path/to/workflow.json'
```

The `--submit --wait` flags are required for the readiness check; they queue the
converted prompt and wait for ComfyUI history success. Omit them only for
conversion-only debugging.
