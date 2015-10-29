#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygmsh as pg
import numpy as np


def generate():
    '''Pipe with double-ring enclosure, rotated in space.
    '''
    geom = pg.Geometry()

    R = pg.rotation_matrix([1, 0, 0], np.pi/6.0)

    geom.add_pipe(
            inner_radius=0.3,
            outer_radius=0.4,
            length=1.0,
            R=R,
            lcar=0.04
            )

    # x0 = np.array([0, 0, 0.3])
    # geom.add_torus(
    #         irad=0.05, orad=0.6, lcar=0.1,
    #         R=R,
    #         x0=np.dot(R, x0)
    #         )

    # x0 = np.array([0, 0, -0.3])
    # geom.add_torus(
    #         irad=0.05, orad=0.6, lcar=0.1,
    #         R=R,
    #         x0=np.dot(R, x0)
    #         )

    return geom.get_code()


if __name__ == '__main__':
    print(generate())
