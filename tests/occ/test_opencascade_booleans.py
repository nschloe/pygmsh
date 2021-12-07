"""Test module for boolean operations."""
import meshio
import numpy as np
import pytest
from helpers import compute_volume

import pygmsh


def square_loop(geom):
    """Construct square using built in geometry."""
    points = [
        geom.add_point([-0.5, -0.5], 0.05),
        geom.add_point([-0.5, 0.5], 0.05),
        geom.add_point([0.5, 0.5], 0.05),
        geom.add_point([0.5, -0.5], 0.05),
    ]
    lines = [
        geom.add_line(points[0], points[1]),
        geom.add_line(points[1], points[2]),
        geom.add_line(points[2], points[3]),
        geom.add_line(points[3], points[0]),
    ]
    return geom.add_curve_loop(lines)


def circle_loop(geom):
    """construct circle using geo geometry module."""
    points = [
        geom.add_point([+0.0, +0.0], 0.05),
        geom.add_point([+0.0, +0.1], 0.05),
        geom.add_point([-0.1, +0.0], 0.05),
        geom.add_point([+0.0, -0.1], 0.05),
        geom.add_point([+0.1, +0.0], 0.05),
    ]
    quarter_circles = [
        geom.add_circle_arc(points[1], points[0], points[2]),
        geom.add_circle_arc(points[2], points[0], points[3]),
        geom.add_circle_arc(points[3], points[0], points[4]),
        geom.add_circle_arc(points[4], points[0], points[1]),
    ]
    return geom.add_curve_loop(quarter_circles)


def _square_hole_classical(geom):
    """Construct surface using builtin and boolean methods."""
    # construct surface with hole using standard built in
    geom.characteristic_length_min = 0.05
    geom.characteristic_length_max = 0.05
    square = square_loop(geom)
    circle = circle_loop(geom)
    geom.add_plane_surface(square, [circle])


def _square_hole_cad(geom):
    # construct surface using boolean
    geom.characteristic_length_min = 0.05
    geom.characteristic_length_max = 0.05
    square2 = square_loop(geom)
    curve_loop2 = circle_loop(geom)
    surf1 = geom.add_plane_surface(square2)
    surf2 = geom.add_plane_surface(curve_loop2)
    geom.boolean_difference(surf1, surf2)


@pytest.mark.parametrize("fun", [_square_hole_classical, _square_hole_cad])
def test_square_circle_hole(fun):
    """Test planar surface with holes.

    Construct it with boolean operations and verify that it is the same.
    """
    with pygmsh.occ.Geometry() as geom:
        fun(geom)
        mesh = geom.generate_mesh()
    surf = 1 - 0.1 ** 2 * np.pi
    assert np.abs((compute_volume(mesh) - surf) / surf) < 1e-3


@pytest.mark.skip()
def test_square_circle_slice():
    """Test planar surface square with circular hole.

    Also test for surface area of fragments.
    """
    with pygmsh.occ.Geometry() as geom:
        square = square_loop(geom)
        curve_loop = circle_loop(geom)
        surf1 = geom.add_plane_surface(square)
        surf2 = geom.add_plane_surface(curve_loop)
        geom.boolean_fragments(surf1, surf2)
        mesh = geom.generate_mesh()

    ref = 1.0
    val = compute_volume(mesh)
    assert np.abs(val - ref) < 1e-3 * ref

    # Gmsh 4 default format MSH4 doesn't have geometrical entities.
    outer_mask = np.where(mesh.cell_data["gmsh:geometrical"][2] == 13)[0]
    outer_cells = {}
    outer_cells["triangle"] = mesh.cells_dict["triangle"][outer_mask]

    inner_mask = np.where(mesh.cell_data["gmsh:geometrical"][2] == 12)[0]
    inner_cells = {}
    inner_cells["triangle"] = mesh.cells_dict["triangle"][inner_mask]

    ref = 1 - 0.1 ** 2 * np.pi
    value = compute_volume(meshio.Mesh(mesh.points, outer_cells))
    assert np.abs(value - ref) < 1e-2 * ref


@pytest.mark.skip("cell data not working yet")
def test_fragments_diff_union():
    """Test planar surface with holes.

    Construct it with boolean operations and verify that it is the same.
    """
    # construct surface using boolean
    with pygmsh.occ.Geometry() as geom:
        geom.characteristic_length_min = 0.04
        geom.characteristic_length_max = 0.04
        square = square_loop(geom)
        surf1 = geom.add_plane_surface(square)
        curve_loop = circle_loop(geom)
        surf2 = geom.add_plane_surface(curve_loop)

        geom.add_physical([surf1], label="1")
        geom.add_physical([surf2], label="2")
        geom.boolean_difference(surf1, surf2, delete_other=False)
        mesh = geom.generate_mesh()

    ref = 1.0
    assert np.abs(compute_volume(mesh) - ref) < 1e-3 * ref

    surf = 1 - 0.1 ** 2 * np.pi
    outer_mask = np.where(mesh.cell_data_dict["gmsh:geometrical"]["triangle"] == 1)[0]
    outer_cells = {}
    outer_cells["triangle"] = mesh.cells_dict["triangle"][outer_mask]

    inner_mask = np.where(mesh.cell_data_dict["gmsh:geometrical"]["triangle"] == 2)[0]
    inner_cells = {}
    inner_cells["triangle"] = mesh.cells_dict["triangle"][inner_mask]

    value = compute_volume(meshio.Mesh(mesh.points, outer_cells))
    assert np.abs(value - surf) < 1e-2 * surf


@pytest.mark.skip("cell data not working yet")
def test_diff_physical_assignment():
    """construct surface using boolean.

    Ensure that after a difference operation the initial volume physical label
    is kept for the operated geometry.
    """
    with pygmsh.occ.Geometry() as geom:
        geom.characteristic_length_min = 0.05
        geom.characteristic_length_max = 0.05
        square2 = square_loop(geom)
        curve_loop2 = circle_loop(geom)
        surf1 = geom.add_plane_surface(square2)
        surf2 = geom.add_plane_surface(curve_loop2)
        geom.add_physical(surf1, label="1")
        geom.boolean_difference(surf1, surf2)
        mesh = geom.generate_mesh()
    assert np.allclose(
        mesh.cell_data_dict["gmsh:geometrical"]["triangle"],
        np.ones(mesh.cells_dict["triangle"].shape[0]),
    )
    surf = 1 - 0.1 ** 2 * np.pi
    assert np.abs((compute_volume(mesh) - surf) / surf) < 1e-3


def test_polygon_diff():
    with pygmsh.occ.Geometry() as geom:
        poly = geom.add_polygon([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
        disk = geom.add_disk([0, 0, 0], 0.5)
        geom.boolean_difference(poly, disk)


def test_mesh_size_removal():
    with pygmsh.occ.Geometry() as geom:
        box0 = geom.add_box([0.0, 0, 0], [1, 1, 1], mesh_size=0.1)
        box1 = geom.add_box([0.5, 0.5, 1], [0.5, 0.5, 1], mesh_size=0.2)
        geom.boolean_union([box0, box1])
        geom.generate_mesh()


if __name__ == "__main__":
    test_square_circle_slice()
