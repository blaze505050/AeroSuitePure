from typing import Tuple
from core.airfoil_utils import read_dat

def load_airfoil(path: str) -> Tuple[list, list]:
    """Load an airfoil `.dat` file and return x,y coordinate lists.
    Simple wrapper around `read_dat` for compatibility with tests.
    """
    return read_dat(path)
