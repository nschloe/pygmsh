from helpers import compute_volume

import pygmsh


def test():
    geom = pygmsh.built_in.Geometry()

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
    geom.set_background_mesh([field0, field1])

    ref = 4.0
    mesh = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("boundary_layers.vtu")
