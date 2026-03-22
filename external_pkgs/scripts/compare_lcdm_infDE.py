
#!/usr/bin/env python3

import numpy as np, json, os, subprocess, tempfile, shutil, pathlib, sys

INI_BASE = os.environ.get("INI_BASE", os.path.join(os.path.dirname(__file__), "..", "configs", "hi_class_informational_reviewed.ini"))
HICLASS  = os.environ.get("HICLASS_DIR", "/ABS/PATH/TO/hi_class")

def run_class(ini_path):
    exe = os.path.join(HICLASS, "class")
    if not os.path.isfile(exe):
        raise RuntimeError("CLASS/hi_CLASS binary not found at HICLASS_DIR/class")
    print(f"Running CLASS with {ini_path}")
    subprocess.check_call([exe, ini_path])

def modify_ini(in_path, out_path, overrides):
    with open(in_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for k,v in overrides.items():
        found=False
        for i,L in enumerate(lines):
            if L.strip().startswith(k+" "):
                lines[i] = f"{k} = {v}\n"
                found=True
                break
        if not found:
            lines.append(f"{k} = {v}\n")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def main():
    tmp = tempfile.mkdtemp(prefix="infDE_cmp_")
    try:
        # LCDM (betaI=etaI=0)
        lcdm_ini = os.path.join(tmp, "lcdm.ini")
        modify_ini(INI_BASE, lcdm_ini, {"betaI":"0.0", "etaI":"0.0"})
        run_class(lcdm_ini)

        # Informational-DE (as in ini)
        ide_ini = os.path.join(tmp, "infde.ini")
        shutil.copy2(INI_BASE, ide_ini)
        run_class(ide_ini)

        print("Done. Compare mPk/matter_power and C_ell outputs in the current directory.")
        print("Tip: use getdist or your plotting tool to overlay spectra.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
