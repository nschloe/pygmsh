import pytest

import pygmsh
from helpers import compute_volume


@pytest.mark.skipif(pygmsh.get_gmsh_major_version() < 3, reason="requires Gmsh >= 3")
def test_union():
    geom = pygmsh.opencascade.Geometry(
        characteristic_length_min=0.1, characteristic_length_max=0.1
    )

    rectangle = geom.add_rectangle([-1.0, -1.0, 0.0], 2.0, 2.0)
    disk_w = geom.add_disk([-1.0, 0.0, 0.0], 0.5)
    disk_e = geom.add_disk([+1.0, 0.0, 0.0], 0.5)
    geom.boolean_union([rectangle, disk_w, disk_e])

    ref = 4.780361
    mesh = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


@pytest.mark.skipif(pygmsh.get_gmsh_major_version() < 3, reason="requires Gmsh >= 3")
def test_intersection():
    geom = pygmsh.opencascade.Geometry(
        characteristic_length_min=0.1, characteristic_length_max=0.1
    )

    rectangle = geom.add_rectangle([-1.0, -1.0, 0.0], 2.0, 2.0)
    disk_w = geom.add_disk([-1.0, 0.0, 0.0], 0.5)
    disk_e = geom.add_disk([+1.0, 0.0, 0.0], 0.5)
    geom.boolean_intersection([rectangle, disk_w, disk_e])

    ref = 0.7803612
    mesh = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


@pytest.mark.skipif(pygmsh.get_gmsh_major_version() < 3, reason="requires Gmsh >= 3")
def test_difference():
    geom = pygmsh.opencascade.Geometry(
        characteristic_length_min=0.1, characteristic_length_max=0.1
    )

    rectangle = geom.add_rectangle([-1.0, -1.0, 0.0], 2.0, 2.0)
    disk_w = geom.add_disk([-1.0, 0.0, 0.0], 0.5)
    disk_e = geom.add_disk([+1.0, 0.0, 0.0], 0.5)
    geom.boolean_difference([rectangle], [disk_w, disk_e])

    ref = 3.2196387
    mesh = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


@pytest.mark.skipif(pygmsh.get_gmsh_major_version() < 3, reason="requires Gmsh >= 3")
def test_all():
    geom = pygmsh.opencascade.Geometry(
        characteristic_length_min=0.1, characteristic_length_max=0.1
    )

    rectangle = geom.add_rectangle([-1.0, -1.0, 0.0], 2.0, 2.0)
    disk1 = geom.add_disk([-1.0, 0.0, 0.0], 0.5)
    disk2 = geom.add_disk([+1.0, 0.0, 0.0], 0.5)
    union = geom.boolean_union([rectangle, disk1, disk2])

    disk3 = geom.add_disk([0.0, -1.0, 0.0], 0.5)
    disk4 = geom.add_disk([0.0, +1.0, 0.0], 0.5)
    geom.boolean_difference([union], [disk3, disk4])

    ref = 4.0
    mesh = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("boolean.vtu", test_all())
