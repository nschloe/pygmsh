#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygmsh as pg
import numpy as np


def generate():
    '''Screw
    '''
    # Form a cross.
    X = np.array([
        [0.0,   0.5, 0.0],
        [-0.1,  0.1, 0.0],
        [-0.5,  0.0, 0.0],
        [-0.1, -0.1, 0.0],
        [0.0,  -0.5, 0.0],
        [0.1,  -0.1, 0.0],
        [0.5,   0.0, 0.0],
        [0.1,   0.1, 0.0]
        ])

    poly = pg.add_polygon(X, lcar=0.05)

    axis = [0, 0, 1]
    # pg.Extrude('Surface{%s}' % poly,
    #             translation_axis = axis
    #             )

    pg.Extrude(
            'Surface{%s}' % poly,
            translation_axis=axis,
            rotation_axis=axis,
            point_on_axis=[0, 0, 0],
            angle=1.0 / 6.0 * np.pi
            )

    return pg.get_code()


if __name__ == '__main__':
    print(generate())
