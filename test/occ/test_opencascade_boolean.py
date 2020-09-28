import math

from helpers import compute_volume

import pygmsh


def test_union():
    with pygmsh.occ.Geometry() as geom:
        geom.characteristic_length_min = 0.1
        geom.characteristic_length_max = 0.1
        rectangle = geom.add_rectangle([-1.0, -1.0, 0.0], 2.0, 2.0)
        disk_w = geom.add_disk([-1.0, 0.0, 0.0], 0.5)
        disk_e = geom.add_disk([+1.0, 0.0, 0.0], 0.5)
        geom.boolean_union([rectangle, disk_w, disk_e])
        mesh = geom.generate_mesh()

    ref = 4.780361
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


def test_intersection():
    with pygmsh.occ.Geometry() as geom:
        angles = [math.pi * 3 / 6, math.pi * 7 / 6, math.pi * 11 / 6]
        disks = [
            geom.add_disk([math.cos(angles[0]), math.sin(angles[0]), 0.0], 1.5),
            geom.add_disk([math.cos(angles[1]), math.sin(angles[1]), 0.0], 1.5),
            geom.add_disk([math.cos(angles[2]), math.sin(angles[2]), 0.0], 1.5),
        ]
        geom.boolean_intersection(disks)
        mesh = geom.generate_mesh()

    ref = 1.0290109753807914
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


def test_difference():
    with pygmsh.occ.Geometry() as geom:
        geom.characteristic_length_min = 0.1
        geom.characteristic_length_max = 0.1
        rectangle = geom.add_rectangle([-1.0, -1.0, 0.0], 2.0, 2.0)
        disk_w = geom.add_disk([-1.0, 0.0, 0.0], 0.5)
        disk_e = geom.add_disk([+1.0, 0.0, 0.0], 0.5)
        geom.boolean_union([disk_w, disk_e])
        geom.boolean_difference(rectangle, geom.boolean_union([disk_w, disk_e]))
        mesh = geom.generate_mesh()

    ref = 3.2196387
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


def test_all():
    with pygmsh.occ.Geometry() as geom:
        geom.characteristic_length_min = 0.1
        geom.characteristic_length_max = 0.1

        rectangle = geom.add_rectangle([-1.0, -1.0, 0.0], 2.0, 2.0)
        disk1 = geom.add_disk([-1.0, 0.0, 0.0], 0.5)
        disk2 = geom.add_disk([+1.0, 0.0, 0.0], 0.5)
        union = geom.boolean_union([rectangle, disk1, disk2])

        disk3 = geom.add_disk([0.0, -1.0, 0.0], 0.5)
        disk4 = geom.add_disk([0.0, +1.0, 0.0], 0.5)
        geom.boolean_difference(union, geom.boolean_union([disk3, disk4]))
        mesh = geom.generate_mesh()

    ref = 4.0
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test_difference().write("boolean.vtu")
