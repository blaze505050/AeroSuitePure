# core/panel_solver.py
import numpy as np
from typing import List, Tuple
import math

def panel_method_cl(x: List[float], y: List[float], alpha_deg: float) -> Tuple[float, dict]:
    """
    Very simple vortex-panel solver (constant-strength panels) for inviscid flow.
    Returns Cl (2D, per unit span). Also returns dictionary with Cp distribution arrays.
    """
    # convert to arrays
    xc = np.array(x); yc = np.array(y)
    N = len(xc)-1
    # panel control points and lengths
    xj = (xc[:-1] + xc[1:])/2.0
    yj = (yc[:-1] + yc[1:])/2.0
    sj = np.sqrt((xc[1:]-xc[:-1])**2 + (yc[1:]-yc[:-1])**2)
    # panel angles
    theta = np.arctan2(yc[1:]-yc[:-1], xc[1:]-xc[:-1])
    # Build influence matrix A for vortex panels
    A = np.zeros((N, N))
    RHS = np.zeros(N)
    alpha = np.deg2rad(alpha_deg)
    # free-stream normal velocity at control points
    for i in range(N):
        for j in range(N):
            if i == j:
                # self term
                A[i,j] = 0.5
            else:
                # influence of vortex on control point normal
                dx1 = xc[j] - xj[i]
                dy1 = yc[j] - yj[i]
                dx2 = xc[j+1] - xj[i]
                dy2 = yc[j+1] - yj[i]
                def phi(dx,dy):
                    return math.atan2(dy,dx)
                # induced tangential difference / (2*pi)
                A[i,j] = (phi(dx2,dy2) - phi(dx1,dy1)) / (2*math.pi)
        # right-hand side: -U_infty * normal component
        nx = math.sin(theta[i])  # normal pointing outward approximated
        ny = -math.cos(theta[i])
        RHS[i] = - (math.cos(alpha)*nx + math.sin(alpha)*ny)
    # Kutta condition: circulation continuity: sum(gamma_j * (something)) = 0
    # For constant-vortex panels, apply integral condition by replacing last equation
    # Build augmented system
    A_aug = np.zeros((N+1, N+1))
    A_aug[:N,:N] = A
    A_aug[:N,-1] = 0.0
    A_aug[-1,:N] = 0.0
    # enforce gamma_0 + gamma_{N-1} = 0 (simple Kutta)
    A_aug[-1,0] = 1.0
    A_aug[-1,N-1] = 1.0
    RHS_aug = np.zeros(N+1)
    RHS_aug[:N] = RHS
    # solve linear system with a tiny regularization to handle near-singular matrices
    # add small Tikhonov-like regularization on the panel unknowns (not the augmented row)
    reg = 1e-10 * max(1.0, np.mean(np.abs(A_aug[:N, :N])))
    A_reg = A_aug.copy()
    A_reg[:N, :N] += reg * np.eye(N)
    # Attempt direct solve; if the system is ill-conditioned or singular,
    # apply Tikhonov regularization and finally fall back to least-squares.
    sol = None
    try:
        # check condition number; if very large, prefer regularized solve
        cond = np.linalg.cond(A_aug)
        if cond < 1e12:
            sol = np.linalg.solve(A_aug, RHS_aug)
        else:
            raise np.linalg.LinAlgError("Ill-conditioned")
    except np.linalg.LinAlgError:
        # try small Tikhonov regularization on the top-left block
        reg2 = 1e-8 * np.eye(N+1)
        reg2[-1, -1] = 0.0
        try:
            sol = np.linalg.solve(A_aug + reg2, RHS_aug)
        except np.linalg.LinAlgError:
            # Fall back to a least-squares solution to handle near-singular systems
            sol, *_ = np.linalg.lstsq(A_aug, RHS_aug, rcond=None)

    gamma = sol[:N]
    Gamma = np.sum(gamma * sj)
    Cl2d = 2.0 * Gamma
    gamma = np.array(gamma)
    try:
        A_small = A.copy()
        induced = A_small.T.dot(gamma)
    except Exception:
        induced = np.zeros_like(theta)
    Vt = np.array([math.cos(alpha - th) for th in theta]) + 0.5 * induced
    Cp = 1.0 - Vt**2
    return Cl2d, {"gamma": gamma.tolist(), "Cp": Cp.tolist(), "x_panel": xj.tolist(), "y_panel": yj.tolist(), "theta": theta.tolist()}
