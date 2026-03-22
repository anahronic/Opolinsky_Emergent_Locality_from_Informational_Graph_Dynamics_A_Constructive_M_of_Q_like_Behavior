#!/usr/bin/env bash
set -euo pipefail
# Optional: export COVMAT=/abs/path/to/covmat.cov to reuse covariance

# ==== EDIT THESE PATHS ====
export HICLASS_DIR="${HICLASS_DIR:-/ABS/PATH/TO/hi_class}"
export MP_DIR="${MP_DIR:-/ABS/PATH/TO/montepython}"
export MP_DATA="${MP_DATA:-/ABS/PATH/TO/montepython/data}"

PARAM_FILE="${1:-$(dirname "$0")/../configs/montepython_informational_planck18_desi.param}"
NCHAINS="${NCHAINS:-4}"
SEED="${SEED:-12345}"

cd "$MP_DIR"

# Ensure data path is correct for likelihoods
export PYTHONPATH="$MP_DIR:$PYTHONPATH"

echo "[*] Launching MontePython with $NCHAINS chains..."
for c in $(seq 1 $NCHAINS); do
  ( python3 montepython/MontePython.py run \
      -p "$PARAM_FILE" \
      -o chains \
      -N 100000 \
      --seed $((SEED + c)) \
      --keep-failure \
      --superupdate  \
      --silent \
      ${COVMAT:+--covmat ${COVMAT}} \
    ) &
done

wait
echo "[✓] MCMC completed. Chains in $MP_DIR/chains"
