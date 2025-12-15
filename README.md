# AeroSuitePure — quick start
# AeroSuitePure — quick start

This project contains a tiny airfoil panel-solver demo and a simple Tkinter GUI.

Requirements
- Python 3.8+ (3.13 used in testing here)
- `numpy`, `matplotlib` (install with `pip install -r requirements.txt`)
- `tkinter` for the GUI (usually bundled with the official Windows Python installer)

Quick run (PowerShell)

1. Create a venv (optional but recommended):
```powershell
python -m venv .venv
.
# Activate (PowerShell):
.venv\Scripts\Activate.ps1
```

2. Install dependencies:
```powershell
pip install --upgrade pip
pip install -r .\requirements.txt
```

3. Run the demo (generates `examples/naca2412_n*.dat` and prints Cl):
```powershell
python .\demo.py
```

4. Run the GUI:
```powershell
python -m gui.gui_tk
```

Notes
- If `Activate.ps1` is blocked by PowerShell execution policy, either run the venv Python directly: `.
.venv\Scripts\python.exe .\demo.py`, or set policy: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force`.
- `test_run.py` uses a bundled fake XFoil runner so it can run without the `xfoil` binary.

Generated assets
- Example sweep plots and CSVs are produced by `scripts/generate_examples.py` and saved into `outputs/plots` and `outputs`.

Development & CI
- A lightweight GitHub Actions workflow is included at `.github/workflows/ci.yml` to run the test suite automatically on push.

To produce real screenshots (locally):
```powershell
.
.venv\Scripts\python.exe .\scripts\generate_examples.py
```

AeroSuitePure — quick run instructions
=====================================

This repository contains a small educational airfoil toolkit (NACA generator, simple panel solver, and a Tk GUI).

Quick requirements
- Python 3.10+ (tested with 3.13)
- `numpy`, `matplotlib` (listed in `requirements.txt`)
- `tkinter` for the GUI (usually included with Windows Python)

Setup (PowerShell)
-------------------
1) Create a virtual environment (recommended):

```powershell
python -m venv .venv
# Activate (PowerShell)
.venv\Scripts\Activate.ps1
```

If you cannot run `Activate.ps1` due to execution policy, either run the venv python directly or allow per-user scripts:

```powershell
# Run venv python directly (no activation required):
.\.venv\Scripts\python.exe .\demo.py

# Or change current-user policy (run PowerShell as Administrator if needed):
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
.venv\Scripts\Activate.ps1
```

2) Install dependencies (inside the activated venv):

```powershell
pip install --upgrade pip
pip install -r .\requirements.txt
```

Run the demo
------------
- There's a `demo.py` script that generates a NACA2412 `.dat` and runs the panel solver. Run it from the project root:

```powershell
python .\demo.py
```

Run the GUI
----------
- Start the Tk GUI from the project root using the module form so imports resolve correctly:

```powershell
python -m gui.gui_tk
```

Notes & troubleshooting
-----------------------
- If `python -m gui.gui_tk` raises a `FileExistsError` about `outputs/plots`, it's because that path exists as a file. The GUI will attempt to rename it to `outputs/plots.bak` and create a directory; if that fails, delete or rename the file manually.
- `test_run.py` in the repo references `core.xfoil_runner` and `core.airfoil_loader`, which are not included here — that test will fail until those modules are added or the test is adapted.
- The panel solver is intentionally simple and uses small regularization for numerical robustness. For production results, replace with a validated panel method implementation or couple with a viscous solver.

