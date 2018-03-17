#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import pygmsh

from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()

    lcar = 0.1

    circle = geom.add_circle([0.5, 0.5, 0.0], 1.0, lcar)

    triangle = geom.add_polygon(
        [
            [2.0, -0.5, 0.0],
            [4.0, -0.5, 0.0],
            [4.0, 1.5, 0.0],
        ], lcar
        )
    rectangle = geom.add_rectangle(4.75, 6.25, -0.24, 1.25, 0.0, lcar)

    # hold all domain
    geom.add_polygon(
        [
            [-1.0, -1.0, 0.0],
            [+7.0, -1.0, 0.0],
            [+7.0, +2.0, 0.0],
            [-1.0, +2.0, 0.0],
        ], lcar,
        holes=[circle.line_loop, triangle.line_loop, rectangle.line_loop]
        )

    ref = 24.0
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('subdomains.vtu', *test())
