#!/usr/bin/env bash
# quick demo: run a one-off sweep and save a screenshot
python3 - <<'PY'
from core.airfoil_utils import naca4_to_coords, write_dat
from core.panel_solver import panel_method_cl
x,y = naca4_to_coords("2412", n=100)
write_dat("examples/naca2412.dat", x,y, name="NACA 2412")
cl,info = panel_method_cl(x,y,4.0)
print("Cl (2D) at alpha=4 deg:", cl)
PY
