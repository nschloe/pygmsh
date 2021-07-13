from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.geo.Geometry() as geom:
        poly = geom.add_polygon(
            [[0.0, 0.5], [1.0, 0.5], [1.0, 1.0], [0.0, 1.0]],
            mesh_size=0.05,
        )
        cp = geom.copy(poly)
        geom.symmetrize(cp, [0.0, 1.0, 0.0, -0.5])
        mesh = geom.generate_mesh()

    ref = 1.0
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("symmetry.vtk")
