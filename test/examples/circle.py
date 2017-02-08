#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygmsh as pg


def generate():
    geom = pg.Geometry()

    circle = geom.add_circle(
            [0.0, 0.0, 0.0],
            1.0,
            0.3,
            num_sections=4,
            # If compound==False, the section borders have to be points of the
            # discretization. If using a compound circle, they don't; gmsh can
            # choose by itself where to point the circle points.
            compound=True
            )

    ll = geom.add_line_loop(circle)
    geom.add_plane_surface(ll)

    return geom


if __name__ == '__main__':
    import meshio
    points, cells = pg.generate_mesh(generate())
    meshio.write('circle.vtu', points, cells)
