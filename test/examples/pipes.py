#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygmsh as pg
import numpy as np


def generate():
    '''Pipe with double-ring enclosure, rotated in space.
    '''
    geom = pg.Geometry()

    R = pg.rotation_matrix([1, 1, 0], np.pi/6.0)
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

    return geom


if __name__ == '__main__':
    import meshio
    out = pg.generate_mesh(generate())
    meshio.write('pipes.vtu', *out)
