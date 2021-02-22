from helpers import compute_volume

import pygmsh


def test_geo():
    with pygmsh.geo.Geometry() as geom:
        poly = geom.add_polygon(
            [
                [0.0, 0.0, 0.0],
                [2.0, 0.0, 0.0],
                [3.0, 1.0, 0.0],
                [1.0, 2.0, 0.0],
                [0.0, 1.0, 0.0],
            ],
            mesh_size=0.1,
        )

        field0 = geom.add_boundary_layer(
            edges_list=[poly.curve_loop.curves[0]],
            lcmin=0.01,
            lcmax=0.1,
            distmin=0.0,
            distmax=0.2,
        )
        field1 = geom.add_boundary_layer(
            nodes_list=[poly.curve_loop.curves[1].points[1]],
            lcmin=0.01,
            lcmax=0.1,
            distmin=0.0,
            distmax=0.2,
        )
        geom.set_background_mesh([field0, field1], operator="Min")

        ref = 4.0
        mesh = geom.generate_mesh()
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref

    return mesh


def test_occ():
    with pygmsh.occ.Geometry() as geom:
        geom.add_rectangle([0.0, 0.5, 0.0], 5.0, 0.5)

        edge1 = pygmsh.occ.dummy.Dummy(dim=1, id0=1)
        point1 = pygmsh.occ.dummy.Dummy(dim=0, id0=3)

        field0 = geom.add_boundary_layer(
            edges_list=[edge1],
            lcmin=0.01,
            lcmax=0.1,
            distmin=0.0,
            distmax=0.2,
            num_points_per_curve=50,
        )
        field1 = geom.add_boundary_layer(
            nodes_list=[point1],
            lcmin=0.01,
            lcmax=0.1,
            distmin=0.0,
            distmax=0.2,
            num_points_per_curve=50,
        )
        geom.set_background_mesh([field0, field1], operator="Min")

        ref = 2.5
        mesh = geom.generate_mesh()
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test_geo().write("boundary_layers_geo.vtu")
    test_occ().write("boundary_layers_occ.vtu")
