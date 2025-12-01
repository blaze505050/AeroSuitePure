from core.airfoil_utils import naca4_to_coords, read_dat, write_dat
import os

def test_naca_coords_length():
    x,y = naca4_to_coords('2412', n=50)
    assert len(x) == len(y)
    assert len(x) > 10

def test_write_and_read(tmp_path):
    x = [0.0, 0.5, 1.0]
    y = [0.0, 0.1, 0.0]
    p = tmp_path / 'test.dat'
    write_dat(str(p), x, y, name='test')
    xr, yr = read_dat(str(p))
    assert len(xr) == 3
    assert abs(xr[1] - 0.5) < 1e-6
