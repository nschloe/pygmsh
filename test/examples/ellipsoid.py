#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a mesh for an ellipsoid.
'''
import pygmsh as pg


def generate():
    geom = pg.Geometry()
    geom.add_ellipsoid(
        [0.0, 0.0, 0.0],
        [1.0, 0.5, 0.75],
        0.05
        )
    return geom, 13.928122642595467


if __name__ == '__main__':
    import meshio
    out = pg.generate_mesh(generate())
    meshio.write('ellipsoid.vtu', *out)
