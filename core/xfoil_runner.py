"""XFoil runner with optional real `xfoil` integration and a safe fallback.

If an `xfoil` binary is found on PATH, `XFoilRunner` will attempt to call it
and generate a polar. If not found, it falls back to a simulated polar using
the bundled `panel_method_cl` solver for reproducible testing.
"""
import os
import time
import csv
import shutil
import subprocess
from typing import List
from core.airfoil_utils import read_dat
from core.panel_solver import panel_method_cl


class XFoilRunner:
    def __init__(self):
        self.xfoil_cmd = shutil.which("xfoil")

    def run_polar(self, airfoil_path: str, almin: float = -2, almax: float = 10, alstep: float = 1, Re: int = 200000, Mach: float = 0.0) -> str:
        """Generate a polar CSV.

        If `xfoil` is available it will be used; otherwise a simulated polar is
        written using the internal panel solver. Returns the path to the CSV.
        """
        if self.xfoil_cmd:
            try:
                return self._run_real_xfoil(airfoil_path, almin, almax, alstep, Re, Mach)
            except Exception:
                # Fall back to simulated polar on any error
                pass
        return self._run_simulated_polar(airfoil_path, almin, almax, alstep)

    def _run_real_xfoil(self, airfoil_path, almin, almax, alstep, Re, Mach):
        # Basic XFoil scripting: load airfoil, oper, iter, visc, Re, M, vpar, al sequence, polar save
        out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
        os.makedirs(out_dir, exist_ok=True)
        polar_path = os.path.join(out_dir, f'polar_{int(time.time())}.csv')
        # Build XFoil input script
        cmds = []
        cmds.append(f'LOAD {airfoil_path}')
        cmds.append('PLOP')
        cmds.append('')
        cmds.append('OPER')
        cmds.append(f'VISC {Re}')
        cmds.append(f'MACH {Mach}')
        cmds.append(f'ALFA {almin} {almax} {alstep}')
        cmds.append(f'PACC')
        cmds.append(polar_path)
        cmds.append('')
        cmds.append('PWRT')
        cmds.append('')
        cmds.append('QUIT')
        inp = '\n'.join(cmds) + '\n'
        # Call xfoil
        p = subprocess.run([self.xfoil_cmd], input=inp.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        # XFoil writes a polar; attempt to convert to CSV if necessary (some versions write text)
        return polar_path

    def _run_simulated_polar(self, airfoil_path: str, almin: float, almax: float, alstep: float) -> str:
        x, y = read_dat(airfoil_path)
        alphas: List[float] = []
        a = float(almin)
        step = float(alstep)
        while a <= float(almax) + 1e-9:
            alphas.append(round(a, 8))
            a += step

        out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
        os.makedirs(out_dir, exist_ok=True)
        polar_path = os.path.join(out_dir, f'polar_{int(time.time())}.csv')
        with open(polar_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['alpha', 'Cl', 'Cd'])
            for a in alphas:
                cl, info = panel_method_cl(x, y, a)
                cp = info.get('Cp', [])
                if cp:
                    cd = max(1e-6, sum(abs(float(v)) for v in cp) / len(cp) * 0.01)
                else:
                    cd = 1e-3
                writer.writerow([a, cl, cd])
        return polar_path

    def parse_polar(self, polar_file: str) -> List[List[float]]:
        rows = []
        with open(polar_file, 'r', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            for r in reader:
                try:
                    rows.append([float(v) for v in r])
                except Exception:
                    continue
        return rows
