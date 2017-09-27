#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Creates a mesh on a cube.
'''
import pygmsh

from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()
    geom.add_box(0, 1, 0, 1, 0, 1, 1.0)

    ref = 1.0
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('cube.vtu', *test())
