#!/usr/bin/env bash
set -euo pipefail

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

REPORT=0
PYTEST_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --report)
      REPORT=1
      shift
      ;;
    *)
      PYTEST_ARGS+=("$1")
      shift
      ;;
  esac
done

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
if [[ $REPORT -eq 1 ]]; then
  mkdir -p reports
  REPORT_FILE="reports/qa_report_${TIMESTAMP}.html"
  PYTEST_ARGS+=("--html" "$REPORT_FILE" "--self-contained-html")
fi

pytest "${PYTEST_ARGS[@]}"

if [[ $REPORT -eq 1 ]]; then
  echo "HTML report saved to $REPORT_FILE"
fi
