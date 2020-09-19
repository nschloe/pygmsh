from math import pi

from helpers import compute_volume

import pygmsh


def test():
    geom = pygmsh.opencascade.Geometry()

    geom.add_ball(
        [0.0, 0.0, 0.0], 1.0, x0=-0.9, x1=+0.9, alpha=0.5 * pi, char_length=0.1
    )

    mesh = pygmsh.generate_mesh(geom)
    ref = 0.976088698545
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("opencascade_ball.vtu")
