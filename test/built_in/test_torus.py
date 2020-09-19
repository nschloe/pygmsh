import numpy as np
from helpers import compute_volume

import pygmsh


def test(irad=0.05, orad=0.6):
    """Torus, rotated in space."""
    geom = pygmsh.built_in.Geometry()

    R = pygmsh.rotation_matrix([1.0, 0.0, 0.0], np.pi / 2)
    geom.add_torus(irad=irad, orad=orad, mesh_size=0.03, x0=[0.0, 0.0, -1.0], R=R)

    mesh = pygmsh.generate_mesh(geom)

    ref = 2 * np.pi ** 2 * orad * irad ** 2
    assert np.isclose(compute_volume(mesh), ref, rtol=5e-2)
    return mesh


if __name__ == "__main__":
    test().write("torus.vtu")
