#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygmsh as pg
import numpy as np


def generate(lcar=0.3):
    geom = pg.Geometry()

    r = 1.25 * 3.4
    p1 = geom.add(pg.Point([0.0, 0.0, 0.0], lcar))
    # p2 = geom.add_point([+r, 0.0, 0.0], lcar)
    p3 = geom.add(pg.Point([-r, 0.0, 0.0], lcar))
    p4 = geom.add(pg.Point([0.0, +r, 0.0], lcar))
    p5 = geom.add(pg.Point([0.0, -r, 0.0], lcar))
    p6 = geom.add(pg.Point(
            [r*np.cos(+np.pi/12.0), r*np.sin(+np.pi/12.0), 0.0],
            lcar
            ))
    p7 = geom.add(pg.Point(
            [r*np.cos(-np.pi/12.0), r*np.sin(-np.pi/12.0), 0.0],
            lcar
            ))
    p8 = geom.add(pg.Point([0.5*r, 0.0, 0.0], lcar))

    c0 = geom.add(pg.CircleArc([p6, p1, p4]))
    c1 = geom.add(pg.CircleArc([p4, p1, p3]))
    c2 = geom.add(pg.CircleArc([p3, p1, p5]))
    c3 = geom.add(pg.CircleArc([p5, p1, p7]))
    l1 = geom.add(pg.Line(p7, p8))
    l2 = geom.add(pg.Line(p8, p6))
    ll = geom.add(pg.LineLoop([c0, c1, c2, c3, l1, l2]))

    geom.add(pg.PlaneSurface(ll))

    # Fails on travis for some reason. TODO fix
    # test setting physical groups
    # geom.add_physical_point(p1, label='cut')
    # geom.add_physical_line(c0, label='arc')
    # geom.add_physical_surface(pacman, label='pacman')
    # test adding raw code
    # geom.add_raw_code('// test comment')
    # geom.add_raw_code(['// test comment'])

    return geom


if __name__ == '__main__':
    import meshio
    points, cells = pg.generate_mesh(generate())
    meshio.write('pacman.vtu', points, cells)
