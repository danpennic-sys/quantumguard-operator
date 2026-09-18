#!/usr/bin/env bash
# Optional helper: structural check of LICENSE.json (does not verify Ed25519).
# Full cryptographic verification belongs in a small Go tool aligned with QuantumGuard.
set -euo pipefail
LICENSE="${QG_LICENSE_PATH:-./LICENSE.json}"
if [[ ! -f "$LICENSE" ]]; then
  echo "LICENSE not found: $LICENSE" >&2
  exit 1
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "jq required for this helper" >&2
  exit 1
fi
product=$(jq -r '.product // empty' "$LICENSE")
version=$(jq -r '.version // empty' "$LICENSE")
licensee=$(jq -r '.licensee // empty' "$LICENSE")
sig=$(jq -r '.signature // empty' "$LICENSE")
if [[ "$product" != "quantumguard-operator" ]]; then
  echo "unexpected product: $product" >&2
  exit 1
fi
if [[ -z "$version" || -z "$licensee" || -z "$sig" ]]; then
  echo "missing required fields" >&2
  exit 1
fi
echo "OK structural: product=$product version=$version licensee=$licensee"
echo "Note: cryptographic signature verification not performed by this script."
