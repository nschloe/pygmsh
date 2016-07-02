#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygmsh as pg


def generate():
    geom = pg.Geometry()

    geom.add_rectangle(
            0.0, 1.0,
            0.0, 1.0,
            0.0,
            0.1
            )

    return geom


if __name__ == '__main__':
    import meshio
    points, cells = pg.generate_mesh(generate())
    meshio.write('rectangle.vtu', points, cells)
