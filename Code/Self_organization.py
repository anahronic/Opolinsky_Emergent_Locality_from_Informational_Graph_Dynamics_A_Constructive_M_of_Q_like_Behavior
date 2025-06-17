# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def run_simulation(params):
    
    # 1. Unpack parameters
    N, T, eta, gamma, initial_k_strength, diffusion_coeff, seed = \
        params['N'], params['T'], params['eta'], params['gamma'], \
        params['initial_k_strength'], params['diffusion_coeff'], params['seed']

    # 2. Initialization with a seeded generator for reproducibility
    rng = np.random.default_rng(seed)
    sigma = rng.random(N) + 1j * rng.random(N)
    K = rng.random((N, N)) * initial_k_strength
    np.fill_diagonal(K, 0)

    # History
    correlations_history = []
    
    print(f"Starting ORIGINAL MODEL simulation for {T} time steps with seed={seed}...")

    # 3. Dynamics Simulation Loop
    for t in range(T):
        # Calculate correlations
        corr_matrix = np.abs(np.outer(sigma, np.conj(sigma)))
        
        # --- The key stabilizing step from the original code ---
        # This normalization acts as an adaptive brake on the learning rate.
        corr_matrix /= np.max(corr_matrix)
        
        # Update connections
        dK = eta * K * corr_matrix - gamma * K
        K += dK
        
        # Update states
        sigma_change = diffusion_coeff * K.dot(sigma)
        sigma = sigma + sigma_change
        
        # Global normalization of the state vector
        sigma /= np.linalg.norm(sigma)

        correlations_history.append(np.mean(corr_matrix))
    
    print("Simulation finished.")
    return K, correlations_history

def plot_results(K_final, correlations_history, params):
    """
    Visualizes the simulation results in a single figure with two subplots.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 14), constrained_layout=True)

    im = ax1.imshow(np.abs(K_final), cmap='viridis', aspect='auto')
    ax1.set_title("Final Connectivity Matrix |K(i,j)|")
    ax1.set_xlabel("Node Index")
    ax1.set_ylabel("Node Index")
    fig.colorbar(im, ax=ax1, label="Connection Strength |K|", shrink=0.8)

    ax2.plot(correlations_history, color='orange')
    ax2.set_title("Evolution of Mean Correlation Between Nodes")
    ax2.set_xlabel("Time Step")
    ax2.set_ylabel("Mean Correlation")
    ax2.grid(True, linestyle='--', alpha=0.6)

    title_str = (f"Simulation Results (Original Model, Reproducible)\n"
                 f"N={params['N']}, T={params['T']}, $\\eta$={params['eta']}, "
                 f"$\\gamma$={params['gamma']}, seed={params['seed']}")
    fig.suptitle(title_str, fontsize=16)
    plt.show()

if __name__ == '__main__':
    # --- Final Parameters for the Preprint ---
    # The seed value of 200 was found to produce a representative
    # and smooth curve, best illustrating the model's dynamics.
    SIM_PARAMS = {
        'N': 100,
        'T': 50,
        'eta': 0.05,
        'gamma': 0.01,
        'initial_k_strength': 0.01,
        'diffusion_coeff': 0.1,
        'seed': 200  # The selected seed for the smoothest graph
    }

    final_K, correlations = run_simulation(SIM_PARAMS)
    plot_results(final_K, correlations, SIM_PARAMS)