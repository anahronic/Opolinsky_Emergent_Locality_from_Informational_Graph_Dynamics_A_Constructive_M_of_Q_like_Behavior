
#ifndef IDM_MODEL_H
#define IDM_MODEL_H

#include "common.h"  /* CLASS base types */
#include "background.h"
#include "primordial.h"
#include "input.h"
#include "arrays.h"
#include "perturbations.h"
#include <math.h>

/* Parameter container, mirrored from header patch
 * UNITS:
 *  - Lc_Mpch : coherence length in h^{-1} Mpc (comoving)
 *  - tau_Gyr : relaxation time in Gyr (proper). Internally converted to an effective length
 *              in h^{-1} Mpc via:  L_tau = c_I * c * tau / (Mpc) / h .
 *  - betaI, etaI, cI : dimensionless
 */
struct idm_params {
  double Lc_Mpch;   /* h^{-1} Mpc */
  double tau_Gyr;   /* Gyr */
  double betaI;     /* dimensionless */
  double etaI;      /* dimensionless */
  double cI;        /* dimensionless */
  int    idm_enable;
  double alphaPi;   /* optional anisotropic stress amplitude */
};

/* Public API */
int idm_mu_gamma(
  struct background * pba,
  struct perturbs   * ppt,
  double k,      /* in h/Mpc */
  double a,      /* scale factor */
  double * mu,   /* out */
  double * gamma,/* out */
  double * sigma /* out (optional Σ = μ(1+γ)/2) */
);

#endif /* IDM_MODEL_H */
