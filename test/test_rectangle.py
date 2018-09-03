# -*- coding: utf-8 -*-
import pygmsh

from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()

    geom.add_rectangle(0.0, 1.0, 0.0, 1.0, 0.0, 0.1)

    ref = 1.0
    points, cells, _, _, _ = pygmsh.generate_mesh(geom, mesh_file_type="vtk")
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == "__main__":
    import meshio

    meshio.write_points_cells("rectangle.vtu", *test())
