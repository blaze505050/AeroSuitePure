# gui/gui_tk.py
import tkinter as tk
from tkinter import filedialog, messagebox
import threading, os, time
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from core.airfoil_utils import read_dat, write_dat, naca4_to_coords, scale_modify_airfoil
from core.panel_solver import panel_method_cl
from core.optimizer import simple_ga
import numpy as np
import csv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(BASE_DIR, "outputs")
PLOT_DIR = os.path.join(OUT_DIR, "plots")
# Ensure outputs and plots exist. If `plots` exists but is a file, rename it to avoid FileExistsError.
os.makedirs(OUT_DIR, exist_ok=True)
if os.path.exists(PLOT_DIR):
    if not os.path.isdir(PLOT_DIR):
        # rename the existing file to a backup and create the directory
        bak = PLOT_DIR + ".bak"
        try:
            os.rename(PLOT_DIR, bak)
        except Exception:
            # if rename fails, remove the file (last resort)
            try:
                os.remove(PLOT_DIR)
            except Exception:
                pass
        os.makedirs(PLOT_DIR, exist_ok=True)
else:
    os.makedirs(PLOT_DIR, exist_ok=True)

class App:
    def __init__(self, root):
        self.root = root
        root.title("AeroSuitePure — Airfoil Opt (Tk)")
        frm = tk.Frame(root); frm.pack(padx=6, pady=6)

        tk.Label(frm, text="Airfoil (.dat or NACA####):").grid(row=0, column=0, sticky="w")
        self.air_entry = tk.Entry(frm, width=24); self.air_entry.grid(row=0, column=1)
        self.air_entry.insert(0, "NACA2412")
        tk.Button(frm, text="Load .dat", command=self.load_file).grid(row=0, column=2)
        tk.Button(frm, text="Gen NACA", command=self.gen_naca).grid(row=0, column=3)

        tk.Label(frm, text="Alpha (deg):").grid(row=1, column=0, sticky="w")
        self.alpha_e = tk.Entry(frm, width=8); self.alpha_e.grid(row=1, column=1)
        self.alpha_e.insert(0, "4.0")

        tk.Label(frm, text="Sweep end:").grid(row=1, column=2, sticky="w")
        self.alpha_end = tk.Entry(frm, width=6); self.alpha_end.grid(row=1, column=3)
        self.alpha_end.insert(0, "10")

        tk.Label(frm, text="Step:").grid(row=1, column=4, sticky="w")
        self.alpha_step = tk.Entry(frm, width=6); self.alpha_step.grid(row=1, column=5)
        self.alpha_step.insert(0, "1")

        tk.Button(frm, text="Run Sweep", command=self.threaded(self.run_sweep)).grid(row=2, column=1)
        tk.Button(frm, text="Optimize (GA)", command=self.threaded(self.optimize)).grid(row=2, column=2)
        tk.Button(frm, text="Export CSV", command=self.export_csv).grid(row=2, column=3)

        self.status = tk.Label(root, text="Ready", anchor="w")
        self.status.pack(fill="x", padx=6, pady=4)

        self.fig = Figure(figsize=(6,3))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.sweep_result = None
        self.current_dat = None

    def threaded(self, fn):
        def wrapper():
            t = threading.Thread(target=fn)
            t.daemon = True
            t.start()
        return wrapper

    def log(self, msg):
        self.status.config(text=msg)
        self.root.update_idletasks()

    def load_file(self):
        p = filedialog.askopenfilename(filetypes=[("dat","*.dat"),("All","*.*")])
        if p:
            self.air_entry.delete(0, tk.END); self.air_entry.insert(0, p)
            messagebox.showinfo("Loaded", p)

    def gen_naca(self):
        code = self.air_entry.get().strip().upper()
        if code.startswith("NACA"):
            code = code[4:]
        x,y = naca4_to_coords(code, n=100)
        outp = os.path.join(BASE_DIR, "examples", f"{code}.dat")
        write_dat(outp, x, y, name=f"NACA {code}")
        self.air_entry.delete(0, tk.END); self.air_entry.insert(0, outp)
        messagebox.showinfo("Saved", outp)

    def run_sweep(self):
        try:
            src = self.air_entry.get().strip()
            if src.upper().startswith("NACA"):
                code = src.upper().replace("NACA","")
                dat = os.path.join(BASE_DIR,"examples", f"{code}.dat")
                x,y = naca4_to_coords(code, n=120); write_dat(dat, x,y, name=f"NACA {code}")
            else:
                dat = src
            x, y = read_dat(dat)
            a0 = float(self.alpha_e.get()); a1 = float(self.alpha_end.get()); step = float(self.alpha_step.get())
            alphas = np.arange(a0, a1+1e-9, step)
            cl_list = []; cd_list = []; out_rows = []
            self.log("Running sweep...")
            for a in alphas:
                cl, info = panel_method_cl(x,y,a)
                # approximate Cd via inviscid proxy (not physical): use Cp variance as proxy -> smaller means less drag
                cp = np.array(info["Cp"])
                cd = max(1e-4, np.mean(np.abs(cp))*0.01)  # heuristic proxy
                cl_list.append(cl); cd_list.append(cd)
                out_rows.append((a, cl, cd))
                self.log(f"α={a:.2f}°  Cl={cl:.4f} Cd≈{cd:.5f}")
            self.sweep_result = {"alpha": alphas.tolist(), "Cl": cl_list, "Cd": cd_list}
            # plot Cl and Cd
            self.ax.clear()
            self.ax.plot(alphas, cl_list, marker='o', label='Cl')
            self.ax.plot(alphas, cd_list, marker='x', label='Cd (proxy)')
            self.ax.set_xlabel("Alpha (deg)")
            self.ax.legend()
            self.canvas.draw()
            self.log("Sweep finished.")
        except Exception as e:
            self.log("Error: " + str(e))

    def evaluate_candidate(self, params, x,y, alpha):
        cam, th = params
        xm, ym = scale_modify_airfoil(x,y,cam,th)
        cl, info = panel_method_cl(xm,ym,alpha)
        # proxy Cd
        cd = max(1e-4, np.mean(np.abs(info["Cp"]))*0.01)
        if cd <= 0: return -1e9
        return cl / cd

    def optimize(self):
        try:
            src = self.air_entry.get().strip()
            if src.upper().startswith("NACA"):
                code = src.upper().replace("NACA","")
                dat = os.path.join(BASE_DIR,"examples", f"{code}.dat")
                x,y = naca4_to_coords(code, n=120); write_dat(dat, x,y, name=f"NACA {code}")
            else:
                dat = src
            x,y = read_dat(dat)
            alpha = float(self.alpha_e.get())
            self.log("Running GA (small)... please wait")
            def eval_fn(ind):
                return self.evaluate_candidate(ind, x,y, alpha)
            best, score = simple_ga(eval_fn, pop_size=10, gens=8)
            self.log(f"GA done. Best score (Cl/Cd)={score:.3f} cam={best[0]:.3f} th={best[1]:.3f}")
            xm, ym = scale_modify_airfoil(x,y,best[0],best[1])
            out = os.path.join(OUT_DIR, f"optimized_{int(time.time())}.dat")
            write_dat(out, xm, ym, name="optimized")
            messagebox.showinfo("Optimized", f"Saved optimized airfoil:\n{out}")
        except Exception as e:
            self.log("Error: " + str(e))

    def export_csv(self):
        if not self.sweep_result:
            messagebox.showwarning("No data", "Run a sweep first")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not path:
            return
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["alpha_deg","Cl","Cd_proxy"])
            for a,cl,cd in zip(self.sweep_result["alpha"], self.sweep_result["Cl"], self.sweep_result["Cd"]):
                writer.writerow([a,cl,cd])
        messagebox.showinfo("Saved", path)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
                