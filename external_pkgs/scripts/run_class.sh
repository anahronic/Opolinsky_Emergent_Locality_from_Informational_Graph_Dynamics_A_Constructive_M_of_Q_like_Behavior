#!/usr/bin/env bash
set -euo pipefail
HICLASS_DIR="${HICLASS_DIR:-/ABS/PATH/TO/hi_class}"
INI="${1:-$(dirname "$0")/../configs/hi_class_informational_safe.ini}"

if [[ ! -f "$INI" ]]; then echo "Error: .ini file $INI not found"; exit 1; fi
if [[ ! -x "$HICLASS_DIR/class" ]]; then echo "Error: CLASS binary not found at $HICLASS_DIR/class"; exit 1; fi
"$HICLASS_DIR/class" "$INI" ${CLASS_LOG:+| tee "$CLASS_LOG"}
