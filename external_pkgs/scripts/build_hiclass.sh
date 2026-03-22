#!/usr/bin/env bash
set -euo pipefail

# ==== SETTINGS (EDIT) ====
HICLASS_DIR="${HICLASS_DIR:-/ABS/PATH/TO/hi_class}"

echo "[*] Sanity checks ..."
if [[ -z "${HICLASS_DIR}" || ! -d "${HICLASS_DIR}" ]]; then
  echo "Error: HICLASS_DIR is not set or not a directory"; exit 1;
fi
if [[ ! -x "${HICLASS_DIR}/class" && ! -f "${HICLASS_DIR}/Makefile" ]]; then
  echo "Warning: no 'class' binary yet; will try to build."
fi
echo "[*] Copying custom sources into $HICLASS_DIR/source ..."
cp -v "$(dirname "$0")/../src/idm_model.c" "$HICLASS_DIR/source/"
cp -v "$(dirname "$0")/../src/idm_model.h" "$HICLASS_DIR/source/"
if [[ ! -f "$HICLASS_DIR/source/idm_model.c" || ! -f "$HICLASS_DIR/source/idm_model.h" ]]; then
  echo "Error: Failed to copy idm_model.c/h to $HICLASS_DIR/source/"; exit 1;
fi
echo "[i] Now patch hi_CLASS sources per src/PATCH_GUIDE.md if not already patched."

read -p "Press Enter to build hi_CLASS (or Ctrl+C to abort)..." _

pushd "$HICLASS_DIR"
make -j || { echo "Build failed"; exit 1; }
popd

echo "[✓] Build complete."
