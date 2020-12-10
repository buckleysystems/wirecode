# Functions that work on XY positions.
# Unless otherwise specified they operate on complex numbers z = x + iy

from typing import Dict


def p_to_z(p: Dict[str, float]) -> complex:
    return p["X"] + 1j * p["Y"]


def z_to_p(z: complex) -> Dict[str, float]:
    return {"X": z.real, "Y": z.imag}


def midpoint(z1: complex, z2: complex) -> complex:
    return (z1 + z2) / 2