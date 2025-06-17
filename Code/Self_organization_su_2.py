# -*- coding: utf-8 -*-
"""
Simulation with SU(2)-like internal states: complex 2D vectors.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def run_simulation(params):
    """
    Runs the simulation for SU(2)-like internal states (d=2 complex vectors).
    """
    N, T, eta, gamma, initial_k_strength, diffusion_coeff, seed = \
        params['N'], params['T'], params['eta'], params['gamma'], \
        params['initial_k_strength'], params['diffusion_coeff'], params['seed']

    rng = np.random.default_rng(seed)
    sigma = rng.random((N, 2)) + 1j * rng.random((N, 2))  # SU(2)-like: 2D complex vectors
    K = rng.random((N, N)) * initial_k_strength
    np.fill_diagonal(K, 0)

    correlations_history = []

    print(f"Starting SU(2) simulation for {T} time steps with seed={seed}...")

    for t in range(T):
        # Compute pairwise correlations using norm products
        norms = np.linalg.norm(sigma, axis=1)
        corr_matrix = np.outer(norms, norms)
        corr_matrix /= np.max(corr_matrix)

        # Hebbian-like update
        dK = eta * K * corr_matrix - gamma * K
        K += dK

        # Update internal states
        sigma_change = diffusion_coeff * K @ sigma
        sigma += sigma_change
        sigma /= np.linalg.norm(sigma, axis=1, keepdims=True)  # Normalize each vector

        correlations_history.append(np.mean(corr_matrix))

    print("SU(2) Simulation complete.")
    return K, correlations_history

def plot_results(K_final, correlations_history, params):
    """
    Plots results and saves figure to 'figures/' folder.
    """
    os.makedirs("figures", exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 14), constrained_layout=True)

    im = ax1.imshow(np.abs(K_final), cmap='viridis', aspect='auto')
    ax1.set_title("Final Connectivity Matrix |K(i,j)| (SU(2))")
    ax1.set_xlabel("Node Index")
    ax1.set_ylabel("Node Index")
    fig.colorbar(im, ax=ax1, label="|K|", shrink=0.8)

    ax2.plot(correlations_history, color='orange')
    ax2.set_title("Mean Correlation Over Time (SU(2))")
    ax2.set_xlabel("Time Step")
    ax2.set_ylabel("Mean Correlation")
    ax2.grid(True, linestyle='--', alpha=0.6)

    fig.suptitle(f"SU(2) Simulation | N={params['N']} | T={params['T']} | seed={params['seed']}", fontsize=14)

    filename = "figures/su2_simulation_output.png"
    plt.savefig(filename, dpi=300)
    print(f"Plot saved to {filename}")
    plt.show()

if __name__ == '__main__':
    SU2_PARAMS = {
        'N': 100,
        'T': 50,
        'eta': 0.05,
        'gamma': 0.01,
        'initial_k_strength': 0.01,
        'diffusion_coeff': 0.1,
        'seed': 202
    }

    final_K, correlations = run_simulation(SU2_PARAMS)
    plot_results(final_K, correlations, SU2_PARAMS)
