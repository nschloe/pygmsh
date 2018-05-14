'''Test module for boolean operations.'''
import numpy as np

import pygmsh

from helpers import compute_volume


def square_loop(geo_object):
    '''Construct square using built in geometry.'''

    p_arrays = [np.array([-0.5, -0.5, 0]), np.array([-0.5, 0.5, 0]),
                np.array([0.5, 0.5, 0]), np.array([0.5, -0.5, 0])]
    points = []
    for point in p_arrays:
        new_point = geo_object.add_point(point, 0.05)
        points.append(new_point)
    points = points + [points[0]]
    lines = []
    for point1, point2 in zip(points[:-1], points[1:]):
        line = geo_object.add_line(point1, point2)
        lines.append(line)
    line_loop = geo_object.add_line_loop(lines)
    return geo_object, line_loop


def circle_loop(geo_object):
    '''construct circle using built_in geometry module.'''
    points = [geo_object.add_point(point, 0.05) for point in
              [np.array([0., 0.1, 0.]),
               np.array([-0.1, 0, 0]),
               np.array([0, -0.1, 0]),
               np.array([0.1, 0, 0])]]
    points = points + [points[0]]
    quarter_circles = [geo_object.add_circle_arc(point1,
                                                 geo_object.add_point(
                                                     [0, 0, 0],
                                                     0.05),
                                                 point2) for
                       point1, point2 in zip(points[:-1], points[1:])]
    line_loop = geo_object.add_line_loop(quarter_circles)
    return geo_object, line_loop


def built_in_opencascade_geos():
    '''Construct surface using builtin and boolean methods.'''
    # construct surface with hole using standard built in
    geo_object = pygmsh.opencascade.Geometry(0.05, 0.05)
    geo_object, square = square_loop(geo_object)
    geo_object, circle = circle_loop(geo_object)
    geo_object.add_plane_surface(square, [circle])

    # construct surface using boolean
    geo_object2 = pygmsh.opencascade.Geometry(0.05, 0.05)
    geo_object2, square2 = square_loop(geo_object2)
    geo_object2, line_loop2 = circle_loop(geo_object2)
    surf1 = geo_object2.add_plane_surface(square2)
    surf2 = geo_object2.add_plane_surface(line_loop2)
    geo_object2.boolean_difference([surf1], [surf2])

    return geo_object, geo_object2


def built_in_opencascade_geos_fragments():
    '''Cconstruct surface using boolean fragments.'''

    geo_object = pygmsh.opencascade.Geometry(0.04, 0.04)
    geo_object, square = square_loop(geo_object)
    geo_object, line_loop = circle_loop(geo_object)
    surf1 = geo_object.add_plane_surface(square)
    surf2 = geo_object.add_plane_surface(line_loop)

    geo_object.boolean_fragments([surf1], [surf2])
    return geo_object


def test_square_circle_hole():
    '''Test planar surface with holes.

    Construct it with boolean operations and verify that it is the same.
    '''
    for geo_object in built_in_opencascade_geos():
        points, cells, _, _, _ = pygmsh.generate_mesh(geo_object)
        surf = 1 - 0.1 ** 2 * np.pi
        assert np.abs((compute_volume(points, cells) - surf) / surf) < 1e-3
    return


def test_square_circle_slice():
    '''Test planar suface square with circular hole.

    Also test for surface area of fragments.
    '''
    geo_object = built_in_opencascade_geos_fragments()
    points, cells, _, cell_data, _ = pygmsh.generate_mesh(geo_object)
    ref = 1
    val = compute_volume(points, cells)
    assert np.abs(val - ref) < 1e-3 * ref

    print(cell_data['triangle'])
    outer_mask = np.where(cell_data['triangle']['gmsh:geometrical'] == 13)[0]
    outer_cells = {}
    outer_cells['triangle'] = cells['triangle'][outer_mask]

    inner_mask = np.where(cell_data['triangle']['gmsh:geometrical'] == 12)[0]
    inner_cells = {}
    inner_cells['triangle'] = cells['triangle'][inner_mask]

    ref = 1 - 0.1 ** 2 * np.pi
    value = compute_volume(points, outer_cells)
    assert np.abs(value - ref) < 1e-2 * ref
    return


def test_fragments_diff_union():
    '''Test planar surface with holes.

    Construct it with boolean operations and verify that it is the same.
    '''
    # construct surface using boolean
    geo_object = pygmsh.opencascade.Geometry(0.04, 0.04)
    geo_object, square = square_loop(geo_object)
    geo_object, line_loop = circle_loop(geo_object)
    surf1 = geo_object.add_plane_surface(square)
    surf2 = geo_object.add_plane_surface(line_loop)

    geo_object.add_physical_surface([surf1], label=1)
    geo_object.add_physical_surface([surf2], label=2)
    surf_diff = geo_object.boolean_difference([surf1], [surf2], delete_other=False)
    geo_object.boolean_union([surf_diff, surf2])
    points, cells, _, cell_data, _ = pygmsh.generate_mesh(geo_object)
    assert np.abs((compute_volume(points, cells) - 1) / 1) < 1e-3
    surf = 1 - 0.1 ** 2 * np.pi
    outer_mask = np.where(cell_data['triangle']['gmsh:physical'] == 1)[0]
    outer_cells = {}
    outer_cells['triangle'] = cells['triangle'][outer_mask]

    inner_mask = np.where(cell_data['triangle']['gmsh:physical'] == 2)[0]
    inner_cells = {}
    inner_cells['triangle'] = cells['triangle'][inner_mask]
    assert np.abs((compute_volume(points, outer_cells) - surf) / surf) < 1e-2
    return


def test_diff_physical_assignment():
    ''' construct surface using boolean.

    Ensure that after a difference operation the initial volume physical label
    is kept for the operated geometry.
    '''
    geo_object2 = pygmsh.opencascade.Geometry(0.05, 0.05)
    geo_object2, square2 = square_loop(geo_object2)
    geo_object2, line_loop2 = circle_loop(geo_object2)
    surf1 = geo_object2.add_plane_surface(square2)
    surf2 = geo_object2.add_plane_surface(line_loop2)
    geo_object2.add_physical_surface([surf1], label=1)
    geo_object2.boolean_difference([surf1], [surf2])
    points, cells, _, cell_data, _ = pygmsh.generate_mesh(geo_object2)
    assert np.allclose(cell_data['triangle']['gmsh:physical'], np.ones(cells['triangle'].shape[0]))
    surf = 1 - 0.1 ** 2 * np.pi
    assert np.abs((compute_volume(points, cells) - surf) / surf) < 1e-3
    return


if __name__ == '__main__':
    test_square_circle_hole()
    test_square_circle_slice()
    test_fragments_diff_union()
    test_diff_physical_assignment()
