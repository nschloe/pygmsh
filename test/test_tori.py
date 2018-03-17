#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pygmsh

from helpers import compute_volume


def test():
    '''Torus, rotated in space.
    '''
    geom = pygmsh.built_in.Geometry()

    R = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0]
        ])
    geom.add_torus(
        irad=0.05, orad=0.6, lcar=0.03,
        x0=[0.0, 0.0, -1.0],
        R=R
        )

    R = np.array([
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0]
        ])
    geom.add_torus(
        irad=0.05, orad=0.6, lcar=0.03,
        x0=[0.0, 0.0, 1.0],
        variant='extrude_circle'
        )

    ref = 0.06604540601899624
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('torus.vtu', *test())
