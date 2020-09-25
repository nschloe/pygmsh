from helpers import compute_volume

import pygmsh


def test_in_surface():
    with pygmsh.built_in.Geometry() as geom:
        poly = geom.add_polygon(
            [
                [0, 0.3, 0],
                [0, 1.1, 0],
                [0.9, 1.1, 0],
                [0.9, 0.3, 0],
                [0.6, 0.7, 0],
                [0.3, 0.7, 0],
                [0.2, 0.4, 0],
            ],
            mesh_size=[0.2, 0.2, 0.2, 0.2, 0.03, 0.03, 0.01],
        )
        geom.in_surface(poly.lines[4], poly)
        geom.in_surface(poly.points[6], poly)
        mesh = pygmsh.generate_mesh(geom, prune_z_0=True)

    ref = 0.505
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


def test_in_volume():
    with pygmsh.built_in.Geometry() as geom:
        box = geom.add_box(-1, 2, -1, 2, 0, 1, mesh_size=0.5)
        poly = geom.add_polygon(
            [
                [0.0, 0.3, 0],
                [0.0, 1.1, 0],
                [0.9, 1.1, 0],
                [0.9, 0.3, 0],
                [0.6, 0.7, 0],
                [0.3, 0.7, 0],
                [0.2, 0.4, 0],
            ],
            mesh_size=[0.2, 0.2, 0.2, 0.2, 0.03, 0.03, 0.01],
        )
        geom.in_volume(poly.lines[4], box.volume)
        geom.in_volume(poly.points[6], box.volume)
        geom.in_volume(poly, box.volume)

        mesh = pygmsh.generate_mesh(geom)
    ref = 30.505
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test_in_surface().write("test.vtk")
