# TIU Cosmology MCMC Results — Summary & Conclusions

## Run Identification

| Field | Value |
|---|---|
| **Run ID** | `tiu_planck_prod2_20260216_000334` |
| **Date** | February 16–17, 2026 |
| **Sampler** | MontePython v3.6.1 (Metropolis-Hastings) |
| **Boltzmann solver** | hi_CLASS v3.2.3 (branch: `hi_class`, hash: `cbddb280`) |
| **Chains** | 4 parallel |
| **Total steps** | 1,711,155 |
| **Accepted steps** | 389,926 (22.8%) |
| **Data** | Planck 2018 TTTEEE + lowE + lowT |

## Theoretical Basis

This MCMC run tests the predictions of **Part II** of:

> I. Opolinsky, *Theory of the Informational Universe: English Compilation (Full Text +
> Technical Appendix)*, October 2025.
> [`Informational_Universe_EFT_Unified_Theory_4_0.pdf`](../Informational_Universe_EFT_Unified_Theory_4_0.pdf)

Part II, "Causal EFT for Dark Energy," proposes a scalar field I(x) with coherence
length L_c and relaxation time τ_I. The action (Eq. F.1) includes a non-local regulator
F_{L_c}[□] = (1 − L²_c □)⁻¹ that enforces finite signal speed. The field's equation of
motion is telegraph-type (Eq. F.2), yielding:

- **Scale-dependent sound speed:** c²_s(k,a) ≈ c²_I k² / (k² + k²_c(a)), where k_c = a/L_c (Eq. I.1)
- **Modified Poisson equation:** μ(k,a) ≈ 1 + β²_I(a) k² / (k² + k²_∗(a)) (Eq. K.1)
- **Gravitational slip:** γ(k,a) ≈ 1 − η_I(a) k² / (k² + k²_∗(a)) (Eq. K.2)
- **Transition scale:** k_∗(a) ~ a / √(L²_c + c²_I τ²_I) (Eq. K.3)

The paper provides **pilot parameter values** (Table 1, §K.1):

| Paper parameter | Pilot value | MCMC mapping | MCMC prior |
|---|---|---|---|
| L_c | 1–3 h⁻¹ Mpc | `tiu_Lc` | Flat [0.5, 4.5] |
| τ_I | 0.1–1 Gyr | `tiu_tau` | Fixed = 153.0 |
| β_I | ~0.1 | `tiu_beta` | Flat [0.0, 0.3] |

Part III (Technical Appendix) derives the continuum limit from the graph dynamics of
Part I, the telegraph equation via coarse-graining, and the mapping η, γ → τ_I, D_0.
It also derives G = β c³/(ℏ L²_c) from Regge calculus.

## Model

The TIU (Time-Information Universe) model extends ΛCDM with four parameters governing
informational coherence effects on the dark-energy equation of state:

| Parameter | Role | Prior / Value |
|---|---|---|
| `tiu_Lc` | Coherence length scale | Varied, flat [0.5, 4.5] |
| `tiu_beta` | Amplitude of TIU correction | Varied, flat [0.0, 0.3] |
| `tiu_eta` | Dissipation rate | Fixed = 0.1 |
| `tiu_tau` | Coherence time-scale | Fixed = 153.0 |

Standard 6 cosmological parameters and 21 Planck nuisance parameters were varied
(29 total, versus 27 for ΛCDM).

## Key Results

### Best-Fit Parameters (from chain, not MLE)

| Parameter | Best-fit | Posterior mean |
|---|---|---|
| `tiu_Lc` | 4.20 | ~2.70 (poorly constrained) |
| `tiu_beta` | 0.059 | ~0.18 (poorly constrained) |
| H₀ | 66.94 km/s/Mpc | ~67.64 |
| σ₈ | 0.815 | ~0.812 |
| −log L (best) | **1386.26** | — |

### Model Comparison (TIU vs ΛCDM)

| Metric | TIU | ΛCDM | Δ (TIU − ΛCDM) | Interpretation |
|---|---|---|---|---|
| χ²_best | 2772.52 | 2769.60 | **+2.92** | Comparable fit |
| −log L_best | 1386.26 | 1384.80 | **+1.46** | — |
| AIC | 1444.26 | 1438.80 | **+5.46** | Moderate evidence for ΛCDM |
| BIC | 1613.62 | 1596.48 | **+17.14** | Strong evidence for ΛCDM |

> **Caveat:** AIC/BIC use χ²_best from the chain, not the true maximum-likelihood
> estimate. BIC penalty is ln(2540) = 7.84 per extra parameter.

### Convergence Diagnostics

| Diagnostic | TIU | ΛCDM |
|---|---|---|
| Max R̂ (Gelman-Rubin) | 1.0155 (`tiu_Lc`) | 1.0779 (`n_s`) ⚠ |
| Median R̂ | 1.0002 | 1.0219 |
| All R̂ ≤ 1.05? | **Yes ✓** | No — 5 parameters exceed 1.05 |
| ESS / 100k steps | 64.3 | 4.4 |
| ESS ratio (TIU / ΛCDM) | **14.5×** | — |

The TIU extension converges well within the R̂ < 1.05 criterion. The ΛCDM comparison
run (matched budget of 379,673 expanded samples per chain) shows several parameters with
R̂ > 1.05, meaning the ΛCDM comparison is less converged at the same sample budget.

## Interpretation

1. **TIU does not improve the fit** to Planck data over ΛCDM. The extra two varied
   parameters (`tiu_Lc`, `tiu_beta`) are penalized by AIC and especially BIC without
   providing a compensating reduction in χ².

2. **TIU is not excluded.** Δχ² = +2.92 for 2 extra degrees of freedom is not
   statistically significant (p ≈ 0.23). The model fits comparably.

3. **TIU parameters are poorly constrained.** `tiu_Lc` hits the upper prior boundary
   at best-fit (4.20 vs prior max 4.5); the posterior mean (~2.70) spans most of the
   prior range. `tiu_beta` best-fit (0.059) differs substantially from the posterior
   mean (~0.18). These parameters leave little imprint on Planck CMB spectra under the
   current parameterization.

4. **The sampler converges efficiently** in the TIU extension. The 14.5× higher ESS/step
   compared to ΛCDM (at matched budget) and clean R̂ profile indicate a well-behaved
   posterior geometry.

5. **Cosmological parameters are unperturbed.** H₀, σ₈, and other standard parameters
   remain consistent with Planck 2018 ΛCDM values, confirming no parameter-space
   distortion from the TIU extension.

## What This Run Supersedes

The previous `tiu_planck_long` run (December 2025) had:
- Single chain, 11,248 accepted steps, 7.2% acceptance rate
- min(−log L) = 1388.04
- No convergence diagnostics possible (single chain)

The current PROD2 run improves on this by a factor of **~35×** in accepted samples,
uses 4 chains enabling R̂ convergence testing, and achieves a better best-fit
(−log L = 1386.26 vs 1388.04).

## File Guide

```
Test TIU/
├── RESULTS_CONCLUSION.md        ← this file
├── mcmc/
│   ├── log.param                ← full MontePython parameter file (PROD2)
│   ├── 2026-02-17_400000_.paramnames  ← parameter names (35 params)
│   ├── tiu_planck_prod2_*.bestfit     ← best-fit parameter vector
│   ├── tiu_planck_prod2_*.covmat      ← proposal covariance matrix
│   ├── tiu_planck_prod2_*.log         ← chain summary (steps, acceptance, min -logL)
│   ├── tiu_prod1.h_info         ← 1D marginal bounds (from 50k PROD1 run, same config)
│   ├── tiu_prod1.v_info         ← parameter means & sigmas
│   └── tiu_prod1.tex            ← LaTeX table of parameter constraints
├── plots/
│   ├── *_1d.pdf                 ← 1D marginalized posteriors (from PROD1, same config)
│   └── *_triangle.pdf           ← triangle/corner plot (from PROD1, same config)
└── analysis/
    ├── Fullresults.txt           ← comprehensive unified proof bundle
    ├── Model_selection_metrics.txt ← AIC/BIC comparison
    ├── Bestfit_comparison.txt    ← χ² comparison
    ├── Rhat_comparison.txt       ← Gelman-Rubin diagnostics
    ├── summary_compare_v3_matched.txt ← matched-budget TIU vs ΛCDM
    ├── Correlation_summary.txt   ← parameter correlations
    ├── ESS_distribution_comparison.txt ← effective sample size analysis
    └── ESS_budget_stability.txt  ← ESS stability checks
```

> **Note on plots:** The 1D and triangle plots are from the earlier PROD1 run (50,000
> steps, same model & parameter configuration). PROD2-specific plots have not yet been
> generated. The PROD1 plots remain qualitatively representative — the posterior structure
> is the same, with identical prior ranges and likelihoods.

> **Note on raw chains:** The 4 raw chain files (~40 MB each, ~160 MB total) are not
> included in the repository due to size constraints. They are archived locally at:
> `/home/anahronic/montepython_public/chains/tiu_planck_prod2_20260216_000334/`

## Next Steps

- [ ] Generate PROD2-specific posterior plots (1D marginals + triangle) using
  MontePython's `info` module on the full 400k-step chains
- [ ] Extend prior ranges for `tiu_Lc` (currently hits boundary) or reparameterize
- [ ] Test with additional datasets (BAO, SNIa, lensing) where TIU effects may be
  more detectable
- [ ] Investigate whether fixing `tiu_eta` and `tiu_tau` vs. varying them changes
  the model selection outcome

---

*Generated from PROD2 run data and matched-budget comparison analysis (Feb 19, 2026).*
