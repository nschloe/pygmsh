#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygmsh as pg
import numpy as np


def generate(lcar=0.05):
    geom = pg.Geometry()

    # Draw a cross with a circular hole
    circ = geom.add_circle([0.0, 0.0, 0.0], 0.1, lcar=lcar)
    poly = geom.add_polygon([
        [+0.0, +0.5, 0.0],
        [-0.1, +0.1, 0.0],
        [-0.5, +0.0, 0.0],
        [-0.1, -0.1, 0.0],
        [+0.0, -0.5, 0.0],
        [+0.1, -0.1, 0.0],
        [+0.5, +0.0, 0.0],
        [+0.1, +0.1, 0.0]
        ],
        lcar=lcar,
        holes=[circ]
        )

    axis = [0, 0, 1.0]

    geom.extrude(
        poly,
        translation_axis=axis,
        rotation_axis=axis,
        point_on_axis=[0, 0, 0],
        angle=2.0 / 6.0 * np.pi
        )

    return geom, 0.16951514066385628


if __name__ == '__main__':
    import meshio
    geom_, _ = generate()
    out = pg.generate_mesh(geom_)
    meshio.write('screw.vtu', *out)
