# ComfyUI Workflow Examples

Curated workflow copies from the live ComfyUI workspace:

```text
/mnt/data/comfyui/user/default/workflows
```

Only tested/canonical no-suffix workflow JSON files are copied here. Live GUI
work files remain in ComfyUI as `.work.json` files and are not copied by
default.

Suffix convention in the live workspace:

- `.json`: fixed/tested GUI-loadable workflow
- `.work.json`: editable GUI work copy
- `.api.json`: executable API prompt graph for `POST /prompt`

The `wan22` folder also includes the API prompt for the tested A14B I2V
workflow because it is useful for scripted runs.

Model files and generated outputs stay under `/mnt/data/comfyui` and are not
stored in git.
