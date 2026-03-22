
# Emergent Locality from Informational Graph Dynamics

This repository contains the LaTeX source, Python simulation code, and supporting materials for the research project:

**"Emergent Locality from Informational Graph Dynamics: A Constructive Model of Quantum-like Behavior"** by *Igor Opolinsky, ChatGPT, Gemini (2025)*

---

## 🧠 Summary

We propose a model in which quantum-like behavior and notions of locality emerge from the evolution of a fully connected graph of informational interactions. Each node in the graph carries an internal state vector (`σ_i ∈ ℝ^d`), and each directed edge `K(i,j)` describes the strength of informational flow from node `j` to node `i`.

The model incorporates:
- **Hebbian-type plasticity** in the connectivity matrix,
- **Nonlinear normalization dynamics** of internal states,
- **Emergence of locality** and "particles" without predefined geometry.

Simulations demonstrate:
- Stable clusters (interpreted as "particles"),
- Disconnected regions (interpreted as "vacuum"),
- Probabilistic effects under partial observation (suggesting emergence of a Born-rule-like behavior).

---

## 📁 Repository Structure

```
├── main.tex                            # LaTeX source of the graph dynamics paper
├── Emergent_Locality_...pdf            # Compiled paper (Part I)
├── Informational_Universe_EFT_Unified_Theory_4_0.pdf  # Full theory compilation (Parts I–III)
├── Causal Effective Field Theory for Dark Energy with Coherence.pdf  # Part II standalone
├── README.md                           # This file
├── README_Commercial_Use.txt           # Terms for commercial use
├── LICENSE.txt                         # CC BY-NC-SA 4.0 license
├── Code/                               # Python simulation code (graph dynamics)
├── figures/                            # Simulation output plots
├── informational_DE_hiCLASS_v7.zip     # hi_CLASS dark energy module archive
├── external_pkgs/                      # hi_CLASS addon: configs, source, scripts
│   ├── README.md                       # Addon documentation
│   ├── configs/                        # .ini / .param files for hi_CLASS & MontePython
│   ├── src/                            # C source: idm_model.c/.h, PATCH_GUIDE.md
│   ├── scripts/                        # Build & run scripts
│   └── tools/                          # mu/gamma table generator
└── Test TIU/                           # MCMC cosmological test results (Feb 2026)
    ├── RESULTS_CONCLUSION.md           # Summary, interpretation, file guide
    ├── mcmc/                           # Run metadata: log.param, bestfit, covmat, paramnames
    ├── plots/                          # 1D & triangle posterior plots
    └── analysis/                       # TIU vs ΛCDM comparison reports
```

---

## 🧪 Simulations

The model is implemented in Python 3 using NumPy and Matplotlib.  
Internal state dimensionality `d` can be set to:
- `d=1`: Scalar states → domain separation  
- `d=2`: SU(2)-like behavior → symmetry breaking into orthogonal clusters  
- `d=3`: SU(3)-like behavior → stable particle-like entities

### 🔧 Requirements

- Python 3.8+  
- `numpy`  
- `matplotlib`

### ▶️ Running the Simulation

Navigate to the `code/` directory and run:

```bash
python3 simulation.py
```

Edit the parameter set inside the script to explore different dimensionalities and seed values.

---

## � TIU Cosmological Test (Part II → Data)

Part II of the unified theory paper proposes a **Causal Effective Field Theory for Dark Energy**
with coherence length L_c and relaxation time τ_I. This EFT was implemented in
[hi_CLASS](https://github.com/miguelzuma/hi_class_public) v3.2.3 and tested against
**Planck 2018 TTTEEE + lowE + lowT** data using MontePython v3.6.1.

### Production Run (Feb 2026)

- **4 parallel MCMC chains, 1.7 million total steps, 390k accepted (22.8%)**
- TIU parameters varied: `tiu_Lc` ∈ [0.5, 4.5], `tiu_beta` ∈ [0.0, 0.3]
- TIU parameters fixed: `tiu_eta` = 0.1, `tiu_tau` = 153.0
- Best-fit: −log L = 1386.26 (vs ΛCDM: 1384.80)
- **Δχ² = +2.92** → comparable fit to ΛCDM
- **ΔAIC = +5.46** → moderate evidence for ΛCDM
- **ΔBIC = +17.14** → strong evidence for ΛCDM (complexity penalty)
- All R̂ ≤ 1.05 ✓ (well converged)

**Conclusion:** TIU is not excluded by Planck data, but the extra parameters are not
justified by improved fit. Standard cosmological parameters (H₀, σ₈) remain consistent
with Planck ΛCDM values. See [`Test TIU/RESULTS_CONCLUSION.md`](Test%20TIU/RESULTS_CONCLUSION.md)
for the full analysis.

---

## �🔒 License

This project is released under the  
**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license.  
Full terms can be found in the LICENSE file.

This means:

✅ You may copy, redistribute, and adapt the work for non-commercial purposes.  
🔁 Derivative works must carry the same license.  
📎 You must give appropriate credit to the original authors.

---

## 💼 Commercial Use

Commercial use of this model, code, or derivative implementations requires a separate licensing agreement.

- See: `README_Commercial_Use.txt`  
- Contact: [spectator.ibn.al.haytham@gmail.com](mailto:spectator.ibn.al.haytham@gmail.com)

We welcome commercial inquiries and collaboration offers, including licensing, consulting, or applied research using the model (e.g., in AI, complex systems, quantum-inspired algorithms).

---

## 📘 Citation

If you use this work in your academic research, please cite it.

**Plain Text:**

Opolinsky, I., ChatGPT, Gemini (2025). *Emergent Locality from Informational Graph Dynamics: A Constructive Model of Quantum-like Behavior*. arXiv preprint.

**BibTeX:**

```bibtex
@misc{Opolinsky2025Emergent,
  title={{Emergent Locality from Informational Graph Dynamics: A Constructive Model of Quantum-like Behavior}},
  author={Igor Opolinsky and ChatGPT and Gemini},
  year={2025},
  note={arXiv preprint},
  eprint={XXXX.XXXXX},
  archivePrefix={arXiv}
}
```

*Note: Replace `XXXX.XXXXX` with the actual arXiv ID once assigned.*

---

## 🌌 Vision

We believe that this framework can help bridge the gap between information theory, emergent spacetime, and quantum foundations.

If you're interested in contributing, applying this model, or extending it to new domains — reach out!
