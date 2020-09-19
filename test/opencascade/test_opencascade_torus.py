from math import pi

from helpers import compute_volume

import pygmsh


def test():
    geom = pygmsh.opencascade.Geometry()

    geom.add_torus([0.0, 0.0, 0.0], 1.0, 0.3, 1.25 * pi, char_length=0.1)

    ref = 1.09994740709
    mesh = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("opencascade_torus.vtu")
