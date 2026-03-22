
# Informational-DE hi\_CLASS Addon

This package provides a minimal, **production-style scaffold** to evaluate an informational dark-energy EFT in **hi\_CLASS / CLASS** and fit it with **MontePython**.

The model is encoded via **scale- and time-dependent modified gravity functions**:
- \mu(k,a) = 1 + [β_I(a) k^2]/[k^2 + k_*^2(a)]
- γ(k,a) = 1 - [η_I(a) k^2]/[k^2 + k_*^2(a)]

with transition scale
- k_*^2(a) = a^2 / (L_c^2 + c_I^2 τ_I^2)

and optional small anisotropic stress ∝ (k L_c)^2.

This repo gives:
1. A **drop-in C module** (`src/idm_model.c/.h`) that computes μ, γ, Σ and can be wired into hi_CLASS (parameterized MG path).
2. A **patch guide** (`src/PATCH_GUIDE.md`) showing exactly where to hook these functions inside hi_CLASS sources.
3. A **generator** (`tools/mu_gamma_table_generator.py`) to export tabulated μ, γ on a (k,a) grid for testing and for external-table workflows.
4. Example **ini** files for CLASS/hi_CLASS and **MontePython** parameter file.

> ⚠️ Note: hi_CLASS evolves quickly; file names and function signatures can differ by version. This scaffold uses *generic* hook points with `// BEGIN CUSTOM` markers, so you can adapt with minimal edits.
> The code is standard C99 and does not change the background evolution (only linear perturbations).

---

## Quick Start

### 0) Get hi_CLASS (or CLASS + MG branch)
```bash
git clone https://github.com/miguelzuma/hi_class.git  # or your fork
cd hi_class
```

### 1) Copy addon sources
```bash
# from this repo root:
cp src/idm_model.* /path/to/hi_class/source/
cp -r tools /path/to/hi_class/
```

### 2) Patch hooks (5-minute manual edit)
Follow `src/PATCH_GUIDE.md` and add the small `// BEGIN CUSTOM` blocks into:
- `source/perturbations.c` (query μ, γ, Σ during Poisson & slip computations)
- `source/input.c` (parse new input parameters: L_c, tau_I, beta_I, eta_I, c_I; and optional flags)
- `include/common.h` or `include/perturbations.h` (declare a small struct for the model parameters)

Then build:
```bash
make -j
```

### 3) Generate μ,γ tables (optional / for tests)
```bash
python3 tools/mu_gamma_table_generator.py \
  --Lc_Mpch 2.0 --tau_Gyr 0.3 --betaI 0.2 --etaI 0.1 --cI 1.0 \
  --kmin 1e-4 --kmax 5.0 --Nk 400 --amin 0.1 --amax 1.0 --Na 60 \
  --out tables/mu_gamma_table.npz
```

### 4) Run CLASS/hi_CLASS
Use `configs/hi_class_informational.ini` as a template; tune parameters there.

### 5) Fit with MontePython
Use `configs/montepython_informational.param` with your likelihoods (Planck, DESI, lensing, ISW×lensing).

---

## Parameters

- `alphaPi` — optional anisotropic-stress amplitude (dimensionless). If non-zero, contributes a term ∝ (k·Lc)^2 to the effective slip / shear. Requires wiring in Einstein equations (see PATCH_GUIDE).

- `L_c` — coherence length in **comoving** h^{-1} Mpc (input as `Lc_Mpch`), typically 1–3.
- `tau_I` — relaxation time in Gyr.
- `beta_I, eta_I` — dimensionless amplitudes. Recommend |β_I|,|η_I| ≲ 0.3 as priors.
- `c_I` — characteristic propagation speed (dimensionless, 0–1).

Derived:
- `k_*^2(a) = a^2 / (L_c^2 + c_I^2 τ_I^2)` → knee around `k_* ~ 0.3–1 h Mpc^{-1}` for L_c ~ 1–3.

---

## Validation Checklist

- Reproduce ΛCDM by setting β_I=η_I=0.
- Check stability flags in hi_CLASS (no negative total effective Newton constant; no pathological oscillations).
- Verify small impact on **BAO** and **CMB primary**; localize deviations near `k ~ k_*`.
- Test ISW and ISW×lensing with different τ_I (0.1–1 Gyr).

---

## License
MIT

## Quick Run Recipes

### A) Build and test CLASS
```bash
export HICLASS_DIR=/abs/path/to/hi_class
./scripts/build_hiclass.sh
./scripts/run_class.sh configs/hi_class_informational_safe.ini
```

### B) MCMC with MontePython
```bash
export HICLASS_DIR=/abs/path/to/hi_class
export MP_DIR=/abs/path/to/montepython
export MP_DATA=/abs/path/to/montepython/data
./scripts/run_montepython.sh configs/montepython_informational_planck18_desi.param
```
> Убедитесь, что Planck2018 и DESI DR1 лайклихуды установлены в `MP_DATA` (согласно их инструкциям).

### Notes on Likelihoods
- **Planck 2018**: используйте стандартные `plikHM_TTTEEE`, `lowl`, `simall_EE`, `lensing`. Для PR4 потребуется отдельный плагин.
- **DESI DR1**: BAO + full-shape (RSD). Убедитесь, что версии датасетов совпадают с плагином.

### Safe Priors
- Держите |β_I|,|η_I| ≲ 0.3 на первых прогонах.
- L_c в [0.5, 5] h^{-1} Mpc, τ_I в [0.05, 2] Gyr.
- При проблемах со стабильностью уменьшайте P_k_max_h/Mpc до 3.0.


## Dependencies
- Python: `numpy` (required), `matplotlib` (optional; used by `--plot` helpers)
- C build: working toolchain for CLASS/hi_CLASS


**Note on outputs:** `mTk` requests matter transfer functions and is supported by CLASS/hi_CLASS; useful for ISW diagnostics (low-ℓ sensitivity).


**Units:** `tau_Gyr` (Gyr) is internally converted to an effective comoving length in `h^{-1} Mpc`: `L_tau = c_I * c * tau / (Mpc) / h`, and `k_*^2(a)=a^2/(L_c^2+L_tau^2)`.


**Priors tip:** set `betaI ≥ 0` (the model uses `betaI^2`), while `etaI` can be signed.


**ISW cross-correlation:** If your MontePython setup includes galaxy–CMB ISW likelihoods (e.g., NVSS/DES×Planck), add them to `data.experiments` for sensitivity to the slip and time-delay effects driven by `tau_Gyr`.
