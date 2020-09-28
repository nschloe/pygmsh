"""Create several entities by extrusion, check that the expected
sub-entities are returned and the resulting mesh is correct.
"""
import numpy as np
import pytest

import pygmsh


@pytest.mark.parametrize("kernel", [pygmsh.geo, pygmsh.occ])
def test(kernel):
    with kernel.Geometry() as geom:
        p = geom.add_point([0, 0], 1)
        p_top, _, _ = geom.extrude(p, translation_axis=[1, 0, 0])

        # The mesh should now contain exactly two points, the second one should be where
        # the translation pointed.
        mesh = geom.generate_mesh()
        assert len(mesh.points) == 2
        assert np.array_equal(mesh.points[-1], [1, 0, 0])

        # Check that the top entity (a PointBase) can be extruded correctly again.
        _, _, _ = geom.extrude(p_top, translation_axis=[1, 0, 0])
        mesh = geom.generate_mesh()
        assert len(mesh.points) == 3
        assert np.array_equal(mesh.points[-1], [2, 0, 0])

    # Set up new geometry with one line.
    with kernel.Geometry() as geom:
        p1 = geom.add_point([0, 0], 1.0)
        p2 = geom.add_point([1, 0], 1.0)
        line = geom.add_line(p1, p2)

        l_top, _, _ = geom.extrude(line, [0, 1, 0])
        mesh = geom.generate_mesh()
        assert len(mesh.points) == 5
        assert np.array_equal(mesh.points[-2], [1, 1, 0])

        # Check again for top entity (a LineBase).
        _, _, _ = geom.extrude(l_top, [0, 1, 0])
        mesh = geom.generate_mesh()
        assert len(mesh.points) == 8
        assert np.array_equal(mesh.points[-3], [1, 2, 0])

        # Check that extrusion works on a Polygon
        poly = geom.add_polygon([[5.0, 0.0], [6.0, 0.0], [5.0, 1.0]], mesh_size=1e20)
        a, b, poly_lat = geom.extrude(poly, [0.0, 0.0, 1.0], num_layers=1)
        mesh = geom.generate_mesh()
        assert len(mesh.points) == 8 + 6
        assert len(poly_lat) == 3


if __name__ == "__main__":
    test(pygmsh.geo)
    # test(pygmsh.occ)
