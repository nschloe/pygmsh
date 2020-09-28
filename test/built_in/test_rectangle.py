from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.geo.Geometry() as geom:
        geom.add_rectangle(0.0, 1.0, 0.0, 1.0, 0.0, 0.1)
        mesh = geom.generate_mesh()

    ref = 1.0
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("rectangle.vtu")
