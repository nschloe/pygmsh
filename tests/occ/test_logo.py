from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.occ.Geometry() as geom:
        # test setters, getters
        print(geom.characteristic_length_min)
        print(geom.characteristic_length_max)
        geom.characteristic_length_min = 2.0
        geom.characteristic_length_max = 2.0

        rect1 = geom.add_rectangle([10.0, 0.0, 0.0], 20.0, 40.0, corner_radius=5.0)
        rect2 = geom.add_rectangle([0.0, 10.0, 0.0], 40.0, 20.0, corner_radius=5.0)
        disk1 = geom.add_disk([14.5, 35.0, 0.0], 1.85)
        disk2 = geom.add_disk([25.5, 5.0, 0.0], 1.85)

        rect3 = geom.add_rectangle([10.0, 30.0, 0.0], 10.0, 1.0)
        rect4 = geom.add_rectangle([20.0, 9.0, 0.0], 10.0, 1.0)

        r1 = geom.add_rectangle([9.0, 0.0, 0.0], 21.0, 20.5, corner_radius=8.0)
        r2 = geom.add_rectangle([10.0, 00.0, 0.0], 20.0, 19.5, corner_radius=7.0)
        diff1 = geom.boolean_difference(r1, r2)
        r22 = geom.add_rectangle([9.0, 10.0, 0.0], 11.0, 11.0)
        inter1 = geom.boolean_intersection([diff1, r22])

        r3 = geom.add_rectangle([10.0, 19.5, 0.0], 21.0, 21.0, corner_radius=8.0)
        r4 = geom.add_rectangle([10.0, 20.5, 0.0], 20.0, 20.0, corner_radius=7.0)
        diff2 = geom.boolean_difference(r3, r4)
        r33 = geom.add_rectangle([20.0, 19.0, 0.0], 11.0, 11.0)
        inter2 = geom.boolean_intersection([diff2, r33])

        geom.boolean_difference(
            geom.boolean_union([rect1, rect2]),
            geom.boolean_union([disk1, disk2, rect3, rect4, inter1, inter2]),
        )

        mesh = geom.generate_mesh()
    ref = 1082.4470502181903
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    mesh = test()
    points = mesh.points
    cells = mesh.get_cells_type("triangle")

    # import optimesh

    # # points, cells = optimesh.cvt.quasi_newton_uniform_lloyd(
    # #     points, cells, 1.0e-5, 1000, omega=2.0, verbose=True
    # # )
    # # points, cells = optimesh.cvt.quasi_newton_uniform_blocks(
    # #     points, cells, 1.0e-5, 1000, verbose=True
    # # )
    # points, cells = optimesh.cvt.quasi_newton_uniform_full(
    #     points, cells, 1.0e-5, 1000, verbose=True
    # )

    # # from helpers import plot
    # # plot("logo.png", points, {"triangle": cells})
    import meshio

    # meshio.write_points_cells("logo.vtu", points, {"triangle": cells})
    mesh = meshio.Mesh(points, {"triangle": cells})
    meshio.svg.write(
        "logo.svg", mesh, float_fmt=".3f", stroke_width="1", force_width=300
    )
