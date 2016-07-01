#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygmsh as pg
import numpy as np


def generate():
    '''Torus, rotated in space.
    '''
    geom = pg.Geometry()

    geom.add_torus(
            irad=0.05, orad=0.6, lcar=0.03
            )

    return geom


if __name__ == '__main__':
    import meshio
    points, cells = pg.generate_mesh(generate())
    meshio.write('torus.vtu', points, cells)
