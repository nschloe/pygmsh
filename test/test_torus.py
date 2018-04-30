#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pygmsh

from helpers import compute_volume


def test():
    '''Torus, rotated in space.
    '''
    geom = pygmsh.built_in.Geometry()

    radii = [0.05, 0.6]
    R = pygmsh.rotation_matrix([1., 0., 0.], np.pi / 2)
    geom.add_torus(
        irad=radii[0], orad=radii[1], lcar=0.03,
        x0=[0.0, 0.0, -1.0],
        R=R
        )

    ref = 2 * np.pi ** 2 * radii[0] ** 2 * radii[1]
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 5.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('torus.vtu', *test())
