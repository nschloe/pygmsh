#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygmsh as pg
import numpy as np


def generate(lcar=0.05):
    geom = pg.Geometry()

    # Draw a cross with a circular hole
    circ = geom.add_circle([0.0, 0.0, 0.0], 0.1, lcar=lcar)
    poly = geom.add_polygon([
        [0.0,   0.5, 0.0],
        [-0.1,  0.1, 0.0],
        [-0.5,  0.0, 0.0],
        [-0.1, -0.1, 0.0],
        [0.0,  -0.5, 0.0],
        [0.1,  -0.1, 0.0],
        [0.5,   0.0, 0.0],
        [0.1,   0.1, 0.0]
        ],
        lcar=lcar,
        holes=[circ]
        )

    axis = [0, 0, 1]

    geom.extrude(
        poly,
        translation_axis=axis,
        rotation_axis=axis,
        point_on_axis=[0, 0, 0],
        angle=2.0 / 6.0 * np.pi
        )

    return geom


if __name__ == '__main__':
    import meshio
    points, cells, _, _, _ = pg.generate_mesh(generate())
    meshio.write('screw.vtu', points, cells)
