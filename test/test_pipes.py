#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pygmsh

from helpers import compute_volume


def test():
    '''Pipe with double-ring enclosure, rotated in space.
    '''
    geom = pygmsh.built_in.Geometry()

    sqrt2on2 = 0.5*np.sqrt(2.)
    R = pygmsh.rotation_matrix([sqrt2on2, sqrt2on2, 0], np.pi/6.0)
    geom.add_pipe(
        inner_radius=0.3,
        outer_radius=0.4,
        length=1.0,
        R=R,
        lcar=0.04
        )

    R = np.array([
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0]
        ])
    geom.add_pipe(
        inner_radius=0.3,
        outer_radius=0.4,
        length=1.0,
        lcar=0.04,
        R=R,
        variant='circle_extrusion'
        )

    ref = 0.43988203517453256
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('pipes.vtu', *test())
