#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygmsh

from helpers import compute_volume

from numpy import array, pi, sin, cos


def test():
    geom = pygmsh.built_in.Geometry()

    theta = pi / array([2., 3., 5])
    R = [array([[1, 0, 0],
                [0, cos(theta[0]), -sin(theta[0])],
                [0, sin(theta[0]), cos(theta[0])]]),
         array([[cos(theta[1]), 0, sin(theta[1])],
                [0, 1, 0],
                [-sin(theta[1]), 0, cos(theta[1])]]),
         array([[cos(theta[2]), -sin(theta[2]), 0],
                [sin(theta[2]), cos(theta[2]), 0],
                [0, 0, 1]])]
                   
    geom.add_circle(
        [7., 11., 13.],
        1.,
        .1,
        R[0] @ R[1] @ R[2])

    ref = 3.1363871677682247
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('circle.vtk', *test())
