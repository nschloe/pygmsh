"""Test translation for all dimensions."""
import numpy as np
from helpers import compute_volume

import pygmsh

# def test_translation1d():
#     """Translation of a line."""
#     geom = pygmsh.geo.Geometry()
#     points = []
#     for array in [[1, 0, 0], [0, 0, 0], [0, 1, 0]]:
#         points.append(geom.add_point(array, 0.5))
#     circle = geom.add_circle_arc(*points)
#     # mesh = geom.generate_mesh()
#     geom.translate(circle, [1.5, 0, 0])
#     translated_mesh = geom.generate_mesh()
#     points[:, 0] = points[:, 0] + 1.5
#     assert np.allclose(points, translated_mesh.points)


def test_translation2d():
    """Translation of a surface object."""
    with pygmsh.occ.Geometry() as geom:
        geom.characteristic_length_min = 0.05
        geom.characteristic_length_max = 0.05
        disk = geom.add_disk([0, 0, 0], 1)
        disk2 = geom.add_disk([1.5, 0, 0], 1)
        geom.translate(disk, [1.5, 0, 0])
        geom.boolean_union([disk2, disk])
        mesh = geom.generate_mesh()
    surf = np.pi
    assert np.abs(compute_volume(mesh) - surf) < 1e-3 * surf


def test_translation3d():
    """Translation of a volume object."""
    with pygmsh.occ.Geometry() as geom:
        geom.characteristic_length_min = 0.2
        geom.characteristic_length_max = 0.2
        ball = geom.add_ball([0, 0, 0], 1)
        ball2 = geom.add_ball([1.5, 0, 0], 1)
        geom.translate(ball, [1.5, 0, 0])
        geom.boolean_union([ball2, ball])
        mesh = geom.generate_mesh()
    surf = 4 / 3 * np.pi
    assert np.abs(compute_volume(mesh) - surf) < 2e-2 * surf


if __name__ == "__main__":
    # test_translation1d()
    test_translation2d()
    test_translation3d()
