
#!/usr/bin/env python3
import numpy as np
import argparse, os

def mu_gamma(k, a, Lc, tau, betaI, etaI, cI):
    # k in h/Mpc, Lc in h^{-1} Mpc, tau in Gyr (dimensionless here)
    kstar2 = (a*a)/((Lc*Lc) + (cI*tau)**2)
    frac = (k*k)/(k*k + kstar2 + 1e-60)
    mu = 1.0 + (betaI**2)*frac
    gamma = 1.0 - (etaI)*frac
    sigma = mu*(1.0+gamma)/2.0
    return mu, gamma, sigma, kstar2

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--Lc_Mpch', type=float, required=True)
    ap.add_argument('--tau_Gyr', type=float, required=True)
    ap.add_argument('--betaI', type=float, required=True)
    ap.add_argument('--etaI', type=float, required=True)
    ap.add_argument('--cI', type=float, default=1.0)
    ap.add_argument('--kmin', type=float, default=1e-4)
    ap.add_argument('--kmax', type=float, default=5.0)
    ap.add_argument('--Nk', type=int, default=300)
    ap.add_argument('--amin', type=float, default=0.1)
    ap.add_argument('--amax', type=float, default=1.0)
    ap.add_argument('--Na', type=int, default=60)
    ap.add_argument('--out', type=str, required=True)
    ap.add_argument('--plot', action='store_true'); args = ap.parse_args()

    ks = np.geomspace(args.kmin, args.kmax, args.Nk)
    as_ = np.linspace(args.amin, args.amax, args.Na)

    MU = np.zeros((args.Na, args.Nk))
    GA = np.zeros_like(MU)
    SI = np.zeros_like(MU)
    KS2= np.zeros_like(MU)

    for i,a in enumerate(as_):
        for j,k in enumerate(ks):
            MU[i,j], GA[i,j], SI[i,j], KS2[i,j] = mu_gamma(
                k, a, args.Lc_Mpch, args.tau_Gyr, args.betaI, args.etaI, args.cI
            )

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    np.savez(args.out, k=ks, a=as_, mu=MU, gamma=GA, sigma=SI, kstar2=KS2,
             meta=dict(Lc_Mpch=args.Lc_Mpch, tau_Gyr=args.tau_Gyr,
                       betaI=args.betaI, etaI=args.etaI, cI=args.cI))
    print(f"Wrote table: {args.out}  (shape mu={MU.shape})")

if __name__ == '__main__':
    main()


    if args.plot:
        import matplotlib.pyplot as plt
        # μ(k,a) diagnostic plot (one figure, default colors; no seaborn, single plot)
        plt.figure()
        for i, a in enumerate(as_):
            if i % max(1, len(as_)//6) == 0:
                plt.semilogx(ks, MU[i, :], label=f'a={a:.2f}')
        plt.xlabel('k [h/Mpc]')
        plt.ylabel('mu(k,a)')
        plt.legend()
        png = os.path.splitext(args.out)[0] + '_mu.png'
        plt.savefig(png, dpi=150, bbox_inches='tight')
        print(f"Saved plot: {png}")
        # gamma plot
        plt.figure()
        for i, a in enumerate(as_):
            if i % max(1, len(as_)//6) == 0:
                plt.semilogx(ks, GA[i, :], label=f'a={a:.2f}')
        plt.xlabel('k [h/Mpc]')
        plt.ylabel('gamma(k,a)')
        plt.legend()
        png2 = os.path.splitext(args.out)[0] + '_gamma.png'
        plt.savefig(png2, dpi=150, bbox_inches='tight')
        print(f"Saved plot: {png2}")
        # sigma plot
        plt.figure()
        for i, a in enumerate(as_):
            if i % max(1, len(as_)//6) == 0:
                plt.semilogx(ks, SI[i, :], label=f'a={a:.2f}')
        plt.xlabel('k [h/Mpc]')
        plt.ylabel('sigma(k,a)')
        plt.legend()
        png3 = os.path.splitext(args.out)[0] + '_sigma.png'
        plt.savefig(png3, dpi=150, bbox_inches='tight')
        print(f"Saved plot: {png3}")
