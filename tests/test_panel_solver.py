from core.airfoil_utils import naca4_to_coords
from core.panel_solver import panel_method_cl

def test_panel_solver_runs():
    x,y = naca4_to_coords('0012', n=60)
    cl, info = panel_method_cl(x, y, 2.0)
    assert isinstance(cl, float)
    assert 'Cp' in info
    assert len(info['Cp']) == len(x)-1
