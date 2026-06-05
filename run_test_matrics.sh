#!/usr/bin/env bash
set -euo pipefail

python3 scripts/workflow_queue.py --prompt prompts/prompt5a.md --matrix workflows/test_matrix.txt -b 4 --workers 4 --id prompt5a
python3 scripts/workflow_queue.py --prompt prompts/prompt5b.md --matrix workflows/test_matrix.txt -b 4 --workers 4 --id prompt5b
