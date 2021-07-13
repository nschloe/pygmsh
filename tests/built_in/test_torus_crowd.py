import numpy as np
from helpers import compute_volume

import pygmsh


def test():
    # internal radius of torus
    irad = 0.15
    # external radius of torus
    orad = 0.27

    Z_pos = (irad + orad) * np.concatenate(
        [+np.ones(8), -np.ones(8), +np.ones(8), -np.ones(8)]
    )

    Alpha = np.concatenate(
        [
            np.arange(8) * np.pi / 4.0,
            np.arange(8) * np.pi / 4.0 + np.pi / 16.0,
            np.arange(8) * np.pi / 4.0,
            np.arange(8) * np.pi / 4.0 + np.pi / 16.0,
        ]
    )

    A1 = (
        (irad + orad)
        / np.tan(np.pi / 8.0)
        * np.concatenate(
            [1.6 * np.ones(8), 1.6 * np.ones(8), 1.9 * np.ones(8), 1.9 * np.ones(8)]
        )
    )

    with pygmsh.geo.Geometry() as geom:
        for alpha, a1, z in zip(Alpha, A1, Z_pos):
            # Rotate torus to the y-z-plane.
            R1 = pygmsh.rotation_matrix([0.0, 1.0, 0.0], 0.5 * np.pi)
            R2 = pygmsh.rotation_matrix([0.0, 0.0, 1.0], alpha)
            x0 = np.array([a1, 0.0, 0.0])
            x1 = np.array([0.0, 0.0, z])
            # First rotate to y-z-plane, then move out to a1, rotate by angle
            # alpha, move up by z.
            #
            #    xnew = R2*(R1*x+x0) + x1
            #
            geom.add_torus(
                irad=irad,
                orad=orad,
                mesh_size=0.1,
                R=np.dot(R2, R1),
                x0=np.dot(R2, x0) + x1,
            )
        geom.add_box(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0, mesh_size=0.3)
        mesh = geom.generate_mesh()

    ref = len(A1) * 2 * np.pi ** 2 * orad * irad ** 2 + 2.0 ** 3
    assert np.isclose(compute_volume(mesh), ref, rtol=2e-2)
    return mesh


if __name__ == "__main__":
    test().write("torus_crowd.vtu")
