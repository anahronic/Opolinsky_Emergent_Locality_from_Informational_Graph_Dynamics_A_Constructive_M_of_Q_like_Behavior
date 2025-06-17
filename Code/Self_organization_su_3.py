import numpy as np
import matplotlib.pyplot as plt

def run_simulation(params):
    N, T, eta, gamma, initial_k_strength, diffusion_coeff, seed, d = \
        params['N'], params['T'], params['eta'], params['gamma'], \
        params['initial_k_strength'], params['diffusion_coeff'], \
        params['seed'], params['d']

    rng = np.random.default_rng(seed)
    sigma = rng.standard_normal((N, d))
    K = rng.random((N, N)) * initial_k_strength
    np.fill_diagonal(K, 0)

    correlations_history = []

    for t in range(T):
        norm = np.linalg.norm(sigma, axis=1, keepdims=True) + 1e-8
        normalized_sigma = sigma / norm
        corr_matrix = normalized_sigma @ normalized_sigma.T
        corr_matrix /= np.max(np.abs(corr_matrix))

        dK = eta * K * corr_matrix - gamma * K
        K += dK

        sigma_change = diffusion_coeff * K @ sigma
        sigma += sigma_change

        sigma_norm = np.linalg.norm(sigma, axis=1, keepdims=True) + 1e-8
        sigma /= sigma_norm

        correlations_history.append(np.mean(corr_matrix))

    return K, correlations_history

def plot_results(K_final, correlations_history, params):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 14), constrained_layout=True)

    im = ax1.imshow(np.abs(K_final), cmap='viridis', aspect='auto')
    ax1.set_title(f"Final Connectivity Matrix |K(i,j)| for d={params['d']}")
    ax1.set_xlabel("Node Index")
    ax1.set_ylabel("Node Index")
    fig.colorbar(im, ax=ax1, label="Connection Strength |K|", shrink=0.8)

    ax2.plot(correlations_history, color='orange')
    ax2.set_title(f"Evolution of Mean Correlation (d={params['d']})")
    ax2.set_xlabel("Time Step")
    ax2.set_ylabel("Mean Correlation")
    ax2.grid(True, linestyle='--', alpha=0.6)

    fig.suptitle(f"Simulation Results for SU({params['d']})-like Model", fontsize=16)
    plt.show()

SIM_PARAMS_SU3 = {
    'N': 100,
    'T': 50,
    'eta': 0.05,
    'gamma': 0.01,
    'initial_k_strength': 0.01,
    'diffusion_coeff': 0.1,
    'seed': 300,
    'd': 3  # SU(3)-like behavior
}

final_K_su3, correlations_su3 = run_simulation(SIM_PARAMS_SU3)
plot_results(final_K_su3, correlations_su3, SIM_PARAMS_SU3)
