from core.xfoil_runner import XFoilRunner
from core.airfoil_loader import load_airfoil

print("AeroSuitePure Test Started...")

# Load airfoil
airfoil_path = "examples/naca2412.dat"
print("Loading airfoil:", airfoil_path)

# Run XFoil
xf = XFoilRunner()
print("Running XFOIL (simulated)...")

polar_file = xf.run_polar(
    airfoil_path,
    almin=-2,
    almax=10,
    alstep=1,
    Re=200000,
    Mach=0.0,
)

print("Polar file generated:", polar_file)

# Parse data
data = xf.parse_polar(polar_file)

print("First 5 data points:")
for row in data[:5]:
    print(row)

print("Test Completed Successfully!")
