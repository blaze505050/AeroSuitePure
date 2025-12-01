"""Generate example sweeps and save plots to `outputs/plots`.

This script runs sweeps for a couple of standard NACA airfoils, saves CSV
polar files and Matplotlib PNGs into `outputs/plots` so they can be used as
real screenshots for the README or portfolio.
"""
import os
import time
import numpy as np
import matplotlib.pyplot as plt

from core.airfoil_utils import naca4_to_coords, write_dat, read_dat
from core.panel_solver import panel_method_cl

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(BASE, 'outputs')
PLOTS = os.path.join(OUT, 'plots')
os.makedirs(PLOTS, exist_ok=True)

def run_sweep_for(code):
    code_str = code if code.startswith('NACA') else f'NACA{code}'
    num = code_str.replace('NACA','')
    x,y = naca4_to_coords(num, n=120)
    dat = os.path.join(BASE, 'examples', f'{num}.dat')
    write_dat(dat, x, y, name=f'NACA {num}')
    alphas = np.arange(-4, 12, 1.0)
    cls = []
    cds = []
    for a in alphas:
        cl, info = panel_method_cl(x, y, a)
        cp = np.array(info.get('Cp', []))
        cd = max(1e-6, np.mean(np.abs(cp))*0.01) if cp.size else 1e-3
        cls.append(cl); cds.append(cd)
    # save CSV
    csv_path = os.path.join(OUT, f'sweep_{num}_{int(time.time())}.csv')
    with open(csv_path, 'w', newline='') as f:
        import csv
        w = csv.writer(f)
        w.writerow(['alpha','Cl','Cd'])
        for a,cl,cd in zip(alphas, cls, cds):
            w.writerow([a,cl,cd])
    # plot
    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(alphas, cls, marker='o', label='Cl')
    ax.plot(alphas, cds, marker='x', label='Cd (proxy)')
    ax.set_title(f'Sweep — {code_str}')
    ax.set_xlabel('Alpha (deg)')
    ax.legend()
    img_path = os.path.join(PLOTS, f'sweep_{num}.png')
    fig.savefig(img_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print('Saved', img_path)

def main():
    for code in ['2412','0012']:
        run_sweep_for(code)

if __name__ == '__main__':
    main()
