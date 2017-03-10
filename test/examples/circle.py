#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygmsh as pg


def generate():
    geom = pg.Geometry()
    geom.add_circle(
            [0.0, 0.0, 0.0],
            1.0,
            0.1,
            num_sections=4,
            # If compound==False, the section borders have to be points of the
            # discretization. If using a compound circle, they don't; gmsh can
            # choose by itself where to point the circle points.
            compound=True
            )
    return geom


if __name__ == '__main__':
    import meshio
    out = pg.generate_mesh(generate())
    meshio.write('circle.vtu', *out)
