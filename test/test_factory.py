#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Check factory setup.
'''
import pygmsh

from helpers import compute_volume


def test():
    if pygmsh.get_gmsh_major_version() == 3:
        # factories are supported only in gmsh 3
        geom = pygmsh.Geometry(factory_type='OpenCASCADE')
    else:
        geom = pygmsh.Geometry()

    ref = 1.0
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('factory.vtu', *test())
