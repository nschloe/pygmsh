from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.built_in.Geometry() as geom:
        poly = geom.add_polygon(
            [[0.0, 0.5, 0.0], [1.0, 0.5, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]],
            mesh_size=0.05,
        )
        cp = geom.copy(poly.surface)
        geom.symmetrize(cp, [0.0, 1.0, 0.0, -0.5])
        mesh = pygmsh.generate_mesh(geom)

    ref = 1.0
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("symmetry.vtk")
