from helpers import compute_volume

import pygmsh


def test():
    geom = pygmsh.opencascade.Geometry()

    geom.add_box([0.0, 0.0, 0.0], [1, 2, 3], char_length=0.1)

    ref = 6
    mesh = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("opencascade_box.vtu")
