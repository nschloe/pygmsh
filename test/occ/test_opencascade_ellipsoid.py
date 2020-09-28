from math import pi

from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.occ.Geometry() as geom:
        geom.add_ellipsoid([1.0, 1.0, 1.0], [1.0, 2.0, 3.0], mesh_size=0.1)
        mesh = geom.generate_mesh()

    ref = 8.0 * pi
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("occ_ellipsoid.vtu")
