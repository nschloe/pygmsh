import pytest
from helpers import compute_volume

import pygmsh


def test_in_surface():
    with pygmsh.geo.Geometry() as geom:
        poly = geom.add_polygon(
            [
                [0, 0.3],
                [0, 1.1],
                [0.9, 1.1],
                [0.9, 0.3],
                [0.6, 0.7],
                [0.3, 0.7],
                [0.2, 0.4],
            ],
            mesh_size=[0.2, 0.2, 0.2, 0.2, 0.03, 0.03, 0.01],
        )
        geom.in_surface(poly.lines[4], poly)
        geom.in_surface(poly.points[6], poly)
        mesh = geom.generate_mesh()

    ref = 0.505
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


# Exception: PLC Error:  A segment and a facet intersect at point
@pytest.mark.skip
def test_in_volume():
    with pygmsh.geo.Geometry() as geom:
        box = geom.add_box(-1, 2, -1, 2, 0, 1, mesh_size=0.5)
        poly = geom.add_polygon(
            [
                [0.0, 0.3],
                [0.0, 1.1],
                [0.9, 1.1],
                [0.9, 0.3],
                [0.6, 0.7],
                [0.3, 0.7],
                [0.2, 0.4],
            ],
            mesh_size=[0.2, 0.2, 0.2, 0.2, 0.03, 0.03, 0.01],
        )
        geom.in_volume(poly.lines[4], box.volume)
        geom.in_volume(poly.points[6], box.volume)
        geom.in_volume(poly, box.volume)

        mesh = geom.generate_mesh()
    ref = 30.505
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test_in_surface().write("test.vtk")
