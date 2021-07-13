import numpy as np
from helpers import compute_volume

import pygmsh


def test(irad=0.05, orad=0.6):
    """Torus, rotated in space."""
    with pygmsh.geo.Geometry() as geom:
        R = pygmsh.rotation_matrix([1.0, 0.0, 0.0], np.pi / 2)
        geom.add_torus(irad=irad, orad=orad, mesh_size=0.03, x0=[0.0, 0.0, -1.0], R=R)

        R = pygmsh.rotation_matrix([0.0, 1.0, 0.0], np.pi / 2)
        geom.add_torus(
            irad=irad,
            orad=orad,
            mesh_size=0.03,
            x0=[0.0, 0.0, 1.0],
            variant="extrude_circle",
        )
        mesh = geom.generate_mesh()

    ref = 2 * 2 * np.pi ** 2 * orad * irad ** 2
    assert np.isclose(compute_volume(mesh), ref, rtol=5e-2)
    return mesh


if __name__ == "__main__":
    test().write("torus.vtu")
