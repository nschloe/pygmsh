#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import pi
import pygmsh

from helpers import compute_volume


def test(lcar=0.05):
    geom = pygmsh.built_in.Geometry()

    # Draw a square
    poly = geom.add_polygon(
        [
            [+0.5, +0.0, 0.0],
            [+0.0, +0.5, 0.0],
            [-0.5, +0.0, 0.0],
            [+0.0, -0.5, 0.0],
        ],
        lcar=lcar,
        )

    axis = [0, 0, 1.0]

    geom.extrude(
        poly,
        translation_axis=axis,
        rotation_axis=axis,
        point_on_axis=[0.0, 0.0, 0.0],
        angle=0.5*pi,
        num_layers=5,
        recombine=True
        )

    ref = 3.98156496566
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('rotated_layers.vtu', *test())
