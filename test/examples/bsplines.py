#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygmsh as pg


def generate():
    geom = pg.Geometry()

    lcar = 0.1
    p1 = geom.add(pg.Point([0.0, 0.0, 0.0], lcar))
    p2 = geom.add(pg.Point([1.0, 0.0, 0.0], lcar))
    p3 = geom.add(pg.Point([1.0, 0.5, 0.0], lcar))
    p4 = geom.add(pg.Point([1.0, 1.0, 0.0], lcar))
    s1 = geom.add(pg.Bspline([p1, p2, p3, p4]))

    p2 = geom.add(pg.Point([0.0, 1.0, 0.0], lcar))
    p3 = geom.add(pg.Point([0.5, 1.0, 0.0], lcar))
    s2 = geom.add(pg.Bspline([p4, p3, p2, p1]))

    ll = geom.add(pg.LineLoop([s1, s2]))
    geom.add(pg.PlaneSurface(ll))

    return geom


if __name__ == '__main__':
    import meshio
    points, cells = pg.generate_mesh(generate())
    meshio.write('bsplines.vtu', points, cells)
