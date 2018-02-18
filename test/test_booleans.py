"""Test module for boolean operations."""
import numpy as np

import pygmsh

from helpers import compute_volume


def square_loop(geo_object):
    """Construct square using built in geometry."""

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
    """construct circle using built_in geometry module."""
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
    """Construct surface using builtin and boolean methods."""
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
    """Cconstruct surface using boolean fragments."""

    geo_object = pygmsh.opencascade.Geometry(0.05, 0.05)
    geo_object, square = square_loop(geo_object)
    geo_object, line_loop = circle_loop(geo_object)
    surf1 = geo_object.add_plane_surface(square)
    surf2 = geo_object.add_plane_surface(line_loop)

    geo_object.boolean_fragments([surf1], [surf2])
    return geo_object


def test_square_circle_hole():
    """Test planar surface with holes.

    Construct it with boolean operations and verify that it is the same.
    """
    for geo_object in built_in_opencascade_geos():
        points, cells, _, _, _ = pygmsh.generate_mesh(geo_object)
        surf = 1 - 0.1 ** 2 * np.pi
        assert np.abs((compute_volume(points, cells) - surf) / surf) < 1e-3


def test_square_circle_slice():
    """Test planar suface square with circular hole."""
    geo_object = built_in_opencascade_geos_fragments()
    points, cells, _, _, _ = pygmsh.generate_mesh(geo_object)
    assert np.abs((compute_volume(points, cells) - 1) / 1) < 1e-3


if __name__ == '__main__':
    test_square_circle_hole()
    test_square_circle_slice()
