#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygmsh as pg
import numpy as np


def generate():
    '''Torus, rotated in space.
    '''
    geom = pg.Geometry()

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

    return geom, 2.762585439629634


if __name__ == '__main__':
    import meshio
    out = pg.generate_mesh(generate())
    meshio.write('torus.vtu', *out)
