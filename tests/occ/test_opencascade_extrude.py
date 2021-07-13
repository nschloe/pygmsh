from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.occ.Geometry() as geom:
        geom.characteristic_length_max = 0.05

        rectangle = geom.add_rectangle([-1.0, -1.0, 0.0], 2.0, 2.0, corner_radius=0.2)
        disk1 = geom.add_disk([-1.2, 0.0, 0.0], 0.5)
        disk2 = geom.add_disk([+1.2, 0.0, 0.0], 0.5, 0.3)

        disk3 = geom.add_disk([0.0, -0.9, 0.0], 0.5)
        disk4 = geom.add_disk([0.0, +0.9, 0.0], 0.5)
        flat = geom.boolean_difference(
            geom.boolean_union([rectangle, disk1, disk2]),
            geom.boolean_union([disk3, disk4]),
        )
        geom.extrude(flat, [0, 0, 0.3])
        mesh = geom.generate_mesh()

    ref = 1.1742114942
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


def test2():
    with pygmsh.occ.Geometry() as geom:
        geom.characteristic_length_max = 1.0

        mesh_size = 1
        h = 25
        w = 10
        length = 100
        # x_fin = -0.5 * length
        cr = 1

        f = 0.5 * w
        y = [-f, -f + cr, +f - cr, +f]
        z = [0.0, h - cr, h]
        f = 0.5 * cr
        x = [-f, f]
        points = [
            geom.add_point((x[0], y[0], z[0]), mesh_size=mesh_size),
            geom.add_point((x[0], y[0], z[1]), mesh_size=mesh_size),
            geom.add_point((x[0], y[1], z[1]), mesh_size=mesh_size),
            geom.add_point((x[0], y[1], z[2]), mesh_size=mesh_size),
            geom.add_point((x[0], y[2], z[2]), mesh_size=mesh_size),
            geom.add_point((x[0], y[2], z[1]), mesh_size=mesh_size),
            geom.add_point((x[0], y[3], z[1]), mesh_size=mesh_size),
            geom.add_point((x[0], y[3], z[0]), mesh_size=mesh_size),
        ]

        lines = [
            geom.add_line(points[0], points[1]),
            geom.add_circle_arc(points[1], points[2], points[3]),
            geom.add_line(points[3], points[4]),
            geom.add_circle_arc(points[4], points[5], points[6]),
            geom.add_line(points[6], points[7]),
            geom.add_line(points[7], points[0]),
        ]

        curve_loop = geom.add_curve_loop(lines)
        surface = geom.add_plane_surface(curve_loop)
        geom.extrude(surface, translation_axis=[length, 0, 0])

        mesh = geom.generate_mesh()

    ref = 24941.503891355664
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("occ_extrude.vtu")
