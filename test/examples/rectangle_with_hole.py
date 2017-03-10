#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a mesh for a square with a round hole.
'''
import pygmsh as pg


def generate():
    geom = pg.Geometry()

    circle = geom.add_circle(
            x0=[0.5, 0.5, 0.0],
            radius=0.25,
            lcar=0.1,
            num_sections=4,
            make_surface=False
            )

    geom.add_rectangle(
            0.0, 1.0,
            0.0, 1.0,
            0.0,
            lcar=0.1,
            holes=[circle.line_loop]
            )

    return geom


if __name__ == '__main__':
    import meshio
    points, cells, _, _, _ = pg.generate_mesh(generate())
    meshio.write('rectangle_with_hole.vtu', points, cells)
