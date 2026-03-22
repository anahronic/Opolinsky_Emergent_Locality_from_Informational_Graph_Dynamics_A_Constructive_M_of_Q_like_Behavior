#!/usr/bin/env python3
import numpy as np, sys, os
import matplotlib.pyplot as plt
import argparse

def read_class_pk(fname):
    # Expect a two-column (k [h/Mpc], P[k]) or multi-column file from CLASS
    data = np.loadtxt(fname)
    k = data[:,0]
    P = data[:,1]
    return k, P

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pk1')
    ap.add_argument('pk2')
    ap.add_argument('--labels', nargs=2, default=['LCDM','InfDE'])
    ap.add_argument('--ratio', action='store_true')
    args = ap.parse_args()
    if not os.path.isfile(args.pk1) or not os.path.isfile(args.pk2):
        print('Error: input files not found'); sys.exit(1)

        print("Usage: plot_pk_overlay.py <pk_file_1> <pk_file_2> [labels...]")
        sys.exit(1)
    k1, P1 = read_class_pk(args.pk1)
    k2, P2 = read_class_pk(args.pk2)

    plt.figure()
    plt.loglog(k1, P1, label=args.labels[0])
    plt.loglog(k2, P2, label=args.labels[1])
    plt.xlabel('k [h/Mpc]')
    plt.ylabel('P(k) [(Mpc/h)^3]')
    plt.legend()
    out = 'pk_overlay.png'
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f'Saved {out}')

    if args.ratio:
        plt.figure()
        # Interpolate P2 onto k1 for a clean ratio
        from numpy import interp
        P2i = interp(k1, k2, P2)
        plt.semilogx(k1, P1/(P2i+1e-300) - 1)
        plt.xlabel('k [h/Mpc]')
        plt.ylabel('ΔP/P')
        plt.axhline(0, ls='--')
        out2 = 'pk_ratio.png'
        plt.savefig(out2, dpi=150, bbox_inches='tight')
        print(f'Saved {out2}')

if __name__ == "__main__":
    main()
