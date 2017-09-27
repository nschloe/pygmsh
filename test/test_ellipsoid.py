#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a mesh for an ellipsoid.
'''
import pygmsh

from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()
    geom.add_ellipsoid(
        [0.0, 0.0, 0.0],
        [1.0, 0.5, 0.75],
        0.05
        )

    ref = 1.5676038497587947
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('ellipsoid.vtu', *test())
