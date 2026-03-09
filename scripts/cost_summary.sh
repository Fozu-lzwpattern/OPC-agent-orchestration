#!/bin/bash
# OPC 成本汇总 — 调用 project_tracker.py report
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/project_tracker.py" report
