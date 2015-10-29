#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygmsh as pg
import numpy as np


def generate():

    geom = pg.Geometry()

    X0 = np.array([
        [0.0,   0.0, 0.0],
        [0.5,   0.3, 0.1],
        [-0.5,  0.3, 0.1],
        [0.5,  -0.3, 0.1]
        ])

    R = np.array([0.1, 0.2, 0.1, 0.14])

    holes = []
    for x0, r in zip(X0, R):
        vol, sl = geom.add_ball(x0, r, with_volume=False, lcar=0.2*r)
        holes.append(sl)

    # geom.add_box(
    #         -1, 1,
    #         -1, 1,
    #         -1, 1,
    #         lcar=0.2,
    #         holes=holes
    #         )

    geom.add_ball(
            [0, 0, 0], 1.0,
            lcar=0.2,
            holes=holes
            )

    return geom.get_code()


if __name__ == '__main__':
    print(generate())
