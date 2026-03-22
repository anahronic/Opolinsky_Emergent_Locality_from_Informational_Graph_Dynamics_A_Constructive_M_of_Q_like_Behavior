
# PATCH GUIDE — hooking the Informational-DE μ/γ model into hi_CLASS

This guide assumes a standard hi_CLASS layout:
- `source/perturbations.c` for linear perturbations
- `source/input.c` for input parsing
- `include/perturbations.h` or `include/common.h` for global structs/prototypes

We add:
- a tiny parameter struct `idm_params`
- initialization from `.ini` inputs
- calls to `idm_mu_gamma()` when computing Poisson equation & slip

## 1) Add parameter struct (header)

**File**: `include/perturbations.h` (or `include/common.h`)

```c
// BEGIN CUSTOM: Informational-DE params
struct idm_params {
  double Lc_Mpch;   // h^{-1} Mpc
  double tau_Gyr;   // Gyr
  double betaI;     // dimensionless
  double etaI;      // dimensionless
  double cI;        // dimensionless (<=1)
  int    idm_enable;
};
// END CUSTOM
```

In the main `perturbs` or a global container, add an instance:
```c
// BEGIN CUSTOM
struct idm_params idm;
// END CUSTOM
```

## 2) Parse inputs

**File**: `source/input.c`

Search for other MG/EFT inputs and add:
```c
// BEGIN CUSTOM: read Informational-DE inputs
class_read_double("Lc_Mpch", ppt->idm.Lc_Mpch);
class_read_double("tau_Gyr", ppt->idm.tau_Gyr);
class_read_double("betaI",   ppt->idm.betaI);
class_read_double("etaI",    ppt->idm.etaI);
class_read_double("cI",      ppt->idm.cI);
class_read_int("idm_enable", ppt->idm.idm_enable);
// END CUSTOM
```

Provide sane defaults when absent:
```c
// BEGIN CUSTOM defaults
if (ppt->idm.Lc_Mpch == 0.) ppt->idm.Lc_Mpch = 2.0;
if (ppt->idm.tau_Gyr == 0.) ppt->idm.tau_Gyr = 0.3;
if (ppt->idm.cI       == 0.) ppt->idm.cI     = 1.0;
// END CUSTOM
```

## 3) Call μ/γ in perturbations

**File**: `source/perturbations.c`

At the point where the code computes modified Poisson equation & slip (similar to existing MG hooks), insert:

```c
// BEGIN CUSTOM: query μ(k,a) and γ(k,a)
double mu_k_a = 1.0, gamma_k_a = 1.0, sigma_k_a = 1.0;
if (ppt->idm.idm_enable == _TRUE_) {
  class_call(idm_mu_gamma(pba, ppt, k, a, &mu_k_a, &gamma_k_a, &sigma_k_a),
             ppt->error_message, ppt->error_message);
}
// Use mu_k_a in place of G_eff/G in Poisson; use gamma_k_a for Φ/Ψ slip;
// and sigma_k_a if your pipeline expects Σ = μ(1+γ)/2 (example).
/* Example (schematic):
   psi = - (mu_k_a * 4*pi*G*a*a / k^2) * delta_rho  ;
   phi = gamma_k_a * psi;
*/
// END CUSTOM
```

Near the includes at top:
```c
// BEGIN CUSTOM
#include "idm_model.h"
// END CUSTOM
```

## 4) Add the files

Copy `src/idm_model.c` and `src/idm_model.h` into your `source/` (or `include/`) tree and add them to the Makefile if needed.

Rebuild:
```bash
make -j
```

## 5) Run

Use the provided ini (`configs/hi_class_informational.ini`) as a starting point.


## 6) Makefile note

In the CLASS/hi_CLASS `Makefile`, ensure the new module is compiled and linked. Add:

```
# near other OBJECTS additions
OBJECTS += idm_model.o
```

Re-run `make -j` after editing.
