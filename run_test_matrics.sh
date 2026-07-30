#!/usr/bin/env bash
set -euo pipefail

python3 scripts/workflow_queue.py --prompt prompts/prompt6.md --matrix workflows/test_matrix.txt -b 4 --workers 2 --id prompt6
python3 scripts/workflow_queue.py --prompt prompts/prompt7.md --matrix workflows/test_matrix.txt -b 4 --workers 2 --id prompt7
python3 scripts/workflow_queue.py --prompt prompts/prompt8.md --matrix workflows/test_matrix.txt -b 4 --workers 2 --id prompt8
