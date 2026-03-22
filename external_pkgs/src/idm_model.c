
#include "idm_model.h"

/* helper: square */
static inline double sqr(double x){ return x*x; }

/*
 * k is in h/Mpc (consistent with CLASS k unit);
 * a is the scale factor.
 * This implements:
 *   k_*^2(a) = a^2 / ( L_c^2 + c_I^2 τ_I^2 )
 *   μ(k,a) = 1 + [β_I^2 k^2]/[k^2 + k_*^2(a)]
 *   γ(k,a) = 1 - [η_I   k^2]/[k^2 + k_*^2(a)]
 *   Σ = μ (1+γ)/2  (can be used by lensing pipelines)
 */
int idm_mu_gamma(
  struct background * pba,
  struct perturbs   * ppt,
  double k, double a,
  double * mu, double * gamma, double * sigma
){
  if (ppt->idm.idm_enable == _FALSE_) {
    if (mu)    *mu    = 1.0;
    if (gamma) *gamma = 1.0;
    if (sigma) *sigma = 1.0;
    return _SUCCESS_;
  }

  /* read params */
  const double Lc = ppt->idm.Lc_Mpch;   /* h^{-1} Mpc */
  const double tau= ppt->idm.tau_Gyr;   /* Gyr */
  const double cI = ppt->idm.cI;        /* dimensionless */
  if (cI > 1.0) {
    fprintf(stderr, "[idm_model] WARNING: cI=%.3e > 1 (superluminal), clipping not enforced.\n", cI);
  }
  const double bI = ppt->idm.betaI;
  const double eI = ppt->idm.etaI;

  /* optional anisotropic stress scaling ~(k*Lc)^2 */
  const double alphaPi = ppt->idm.alphaPi;
  const double pi_scale = alphaPi * (k*k) * (Lc*Lc); /* dimensionless suggestion */
  (void)pi_scale; /* placeholder unless wired into Einstein eqs */


  /* compute k_*^2(a) */
  /* UNIT CONV: convert tau [Gyr] into an effective length [h^{-1} Mpc] using c * tau / h */
  const double GYR_TO_SEC = 3.155760e16;       /* 1 Gyr in seconds */
  const double C_MS       = 2.99792458e8;      /* speed of light in m/s */
  const double MPC_IN_M   = 3.0856775814913673e22; /* 1 Mpc in meters */
  /* Effective comoving length scale (in h^{-1} Mpc) associated with tau and propagation speed cI */
  const double L_tau_hMpc = (cI * C_MS * tau * GYR_TO_SEC) / (MPC_IN_M * pba->h + 1e-300);
  const double denom = sqr(Lc) + sqr(L_tau_hMpc);   /* (h^{-1} Mpc)^2 */
  /* warn if denom <= 0 */
  if (denom <= 0.0) {
    fprintf(stderr, "[idm_model] WARNING: non-positive denom in k*_calc (Lc=%.3e, L_tau=%.3e)\n", Lc, L_tau_hMpc);
  }
  const double kstar2 = (denom>0.0) ? sqr(a)/denom : 1e9; /* safe large */

  const double frac = k*k / (k*k + kstar2 + 1e-60);

  double mu_val    = 1.0 + sqr(bI) * frac; /* β_I^2 */
  double gamma_val = 1.0 - (eI)    * frac; /* η_I   */

  if (mu)    *mu    = mu_val;
  if (gamma) *gamma = gamma_val;
  if (sigma) *sigma = mu_val * (1.0 + gamma_val) * 0.5;

  return _SUCCESS_;
}
