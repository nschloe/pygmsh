from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.occ.Geometry() as geom:
        container = geom.add_rectangle([0.0, 0.0, 0.0], 10.0, 10.0)

        letter_i = geom.add_rectangle([2.0, 2.0, 0.0], 1.0, 4.5)
        i_dot = geom.add_disk([2.5, 7.5, 0.0], 0.6)

        disk1 = geom.add_disk([6.25, 4.5, 0.0], 2.5)
        disk2 = geom.add_disk([6.25, 4.5, 0.0], 1.5)
        letter_o = geom.boolean_difference(disk1, disk2)

        geom.boolean_difference(
            container, geom.boolean_union([letter_i, i_dot, letter_o])
        )

        mesh = geom.generate_mesh()

    ref = 81.9131851877
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    # import meshio
    # meshio.write_points_cells('m.vtu', *test())
    from helpers import plot

    mesh = test()
    plot("meshio_logo.png", mesh.points, mesh.get_cells_type("triangle"))
