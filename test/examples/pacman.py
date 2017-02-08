#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygmsh as pg
import numpy as np


def generate(lcar=0.3):
    geom = pg.Geometry()

    r = 1.25 * 3.4
    p1 = geom.add_point([0.0, 0.0, 0.0], lcar)
    p2 = geom.add_point([+r, 0.0, 0.0], lcar)
    p3 = geom.add_point([-r, 0.0, 0.0], lcar)
    p4 = geom.add_point([0.0, +r, 0.0], lcar)
    p5 = geom.add_point([0.0, -r, 0.0], lcar)
    p6 = geom.add_point([r*np.cos(+np.pi/12.0), r*np.sin(+np.pi/12.0), 0.0],
            lcar)
    p7 = geom.add_point([r*np.cos(-np.pi/12.0), r*np.sin(-np.pi/12.0), 0.0],
            lcar)
    p8 = geom.add_point([0.5*r, 0.0, 0.0], lcar)

    c0 = geom.add_circle_sector([p6, p1, p4])
    c1 = geom.add_circle_sector([p4, p1, p3])
    c2 = geom.add_circle_sector([p3, p1, p5])
    c3 = geom.add_circle_sector([p5, p1, p7])
    l1 = geom.add_line(p7, p8)
    l2 = geom.add_line(p8, p6)
    ll = geom.add_line_loop([c0, c1, c2, c3, l1, l2])

    geom.add_plane_surface(ll)

    return geom


if __name__ == '__main__':
    import meshio
    points, cells = pg.generate_mesh(generate())
    meshio.write('pacman.vtu', points, cells)
