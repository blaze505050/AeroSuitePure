# core/airfoil_utils.py
import math
from typing import List, Tuple

def read_dat(path: str) -> Tuple[List[float], List[float]]:
    x, y = [], []
    with open(path, "rt") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            parts = s.split()
            try:
                xi = float(parts[0]); yi = float(parts[1])
                x.append(xi); y.append(yi)
            except Exception:
                continue
    return x, y

def write_dat(path: str, x: List[float], y: List[float], name: str = "airfoil"):
    with open(path, "wt") as f:
        f.write(name + "\n")
        for xi, yi in zip(x, y):
            f.write(f"{xi:.6f} {yi:.6f}\n")

def naca4_to_coords(code: str, n: int = 80) -> Tuple[List[float], List[float]]:
    # simple NACA 4-digit generator (cos spacing)
    code = code.strip()
    if code.upper().startswith("NACA"):
        code = code[4:]
    if len(code) != 4:
        raise ValueError("NACA code must be 4 digits, e.g. 2412")
    m = int(code[0]) / 100.0
    p = int(code[1]) / 10.0
    t = int(code[2:]) / 100.0
    x = [0.5*(1-math.cos(math.pi*i/(n-1))) for i in range(n)]
    yt = [5*t*(0.2969*(xi**0.5) - 0.1260*xi - 0.3516*(xi**2) + 0.2843*(xi**3) - 0.1015*(xi**4)) for xi in x]
    yc = []
    dyc = []
    for xi in x:
        if p > 0 and xi < p:
            yc_i = m/(p**2)*(2*p*xi - xi**2)
            dyc_i = 2*m/(p**2)*(p - xi)
        elif p > 0:
            yc_i = m/((1-p)**2)*((1-2*p) + 2*p*xi - xi**2)
            dyc_i = 2*m/((1-p)**2)*(p - xi)
        else:
            yc_i = 0.0; dyc_i = 0.0
        yc.append(yc_i); dyc.append(dyc_i)
    xu, yu, xl, yl = [], [], [], []
    for xi, yti, yci, dyci in zip(x, yt, yc, dyc):
        theta = math.atan(dyci)
        xu.append(xi - yti*math.sin(theta))
        yu.append(yci + yti*math.cos(theta))
        xl.append(xi + yti*math.sin(theta))
        yl.append(yci - yti*math.cos(theta))
    xu_rev = list(reversed(xu)); yu_rev = list(reversed(yu))
    xcoords = xu_rev + xl[1:]
    ycoords = yu_rev + yl[1:]
    return xcoords, ycoords

def scale_modify_airfoil(x: List[float], y: List[float], camber_scale: float = 0.0, thickness_scale: float = 1.0):
    # Simple but effective: scale y for thickness and add a camber bump
    newy = [yi*thickness_scale for yi in y]
    cambed = []
    for xi, yi in zip(x, newy):
        cam = camber_scale * (4*(xi-0.5)**3) * (1.0 - xi)  # small bump near mid-chord
        cambed.append(yi + cam)
    return x, cambed
