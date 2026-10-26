#!/usr/bin/env bash
set -uo pipefail

TF_DIR="${1:-terraform}"
OUT="${OUT:-results}"
mkdir -p "$OUT"

if command -v terraform >/dev/null; then
  terraform -chdir="$TF_DIR" fmt -check -recursive || { echo "terraform fmt failed"; exit 1; }
  terraform -chdir="$TF_DIR" init -backend=false -input=false >/dev/null
  terraform -chdir="$TF_DIR" validate || exit 1
fi

checkov -d "$TF_DIR" \
  --config-file .checkov.yaml \
  --output json --output sarif \
  --output-file-path "$OUT" \
  --soft-fail --quiet

if command -v tfsec >/dev/null; then
  for fmt in json sarif; do
    tfsec "$TF_DIR" --custom-check-dir .tfsec --format "$fmt" --out "$OUT/tfsec.$fmt" --soft-fail --no-colour
  done
else
  echo "tfsec not installed, skipping"
fi

python3 scripts/summarize.py --checkov "$OUT/results_json.json" --tfsec "$OUT/tfsec.json" "${@:2}"
