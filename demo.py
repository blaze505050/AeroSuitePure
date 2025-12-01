from core.airfoil_utils import naca4_to_coords, write_dat
from core.panel_solver import panel_method_cl

def main():
    # Try a few panel discretizations to avoid occasional singular systems
    ns = [120, 100, 80, 200]
    cl = None
    for n in ns:
        x, y = naca4_to_coords("2412", n=n)
        write_dat(f"examples/naca2412_n{n}.dat", x, y, name=f"NACA 2412 n={n}")
        try:
            cl_try, info = panel_method_cl(x, y, 4.0)
            cl = cl_try
            print(f"Success with n={n}: Cl (2D) at alpha=4 deg: {cl}")
            break
        except Exception as e:
            print(f"n={n} failed: {e}")
    if cl is None:
        print("All panel resolutions failed — panel solver produced singular systems.")

if __name__ == "__main__":
    main()
