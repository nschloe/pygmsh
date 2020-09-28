from math import pi

from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.occ.Geometry() as geom:
        geom.add_ball([0.0, 0.0, 0.0], 1.0, mesh_size=0.1)
        mesh = geom.generate_mesh()

    ref = 4 / 3 * pi
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("occ_ball.vtu")
