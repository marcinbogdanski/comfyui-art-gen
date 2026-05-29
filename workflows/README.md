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
