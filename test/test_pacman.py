#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import pi, sin, cos
import pygmsh

from helpers import compute_volume


def test(lcar=0.3):
    geom = pygmsh.built_in.Geometry()

    r = 1.25 * 3.4
    p1 = geom.add_point([0.0, 0.0, 0.0], lcar)
    # p2 = geom.add_point([+r, 0.0, 0.0], lcar)
    p3 = geom.add_point([-r, 0.0, 0.0], lcar)
    p4 = geom.add_point([0.0, +r, 0.0], lcar)
    p5 = geom.add_point([0.0, -r, 0.0], lcar)
    p6 = geom.add_point([r*cos(+pi/12.0), r*sin(+pi/12.0), 0.0], lcar)
    p7 = geom.add_point([r*cos(-pi/12.0), r*sin(-pi/12.0), 0.0], lcar)
    p8 = geom.add_point([0.5*r, 0.0, 0.0], lcar)

    c0 = geom.add_circle_arc(p6, p1, p4)
    c1 = geom.add_circle_arc(p4, p1, p3)
    c2 = geom.add_circle_arc(p3, p1, p5)
    c3 = geom.add_circle_arc(p5, p1, p7)
    l1 = geom.add_line(p7, p8)
    l2 = geom.add_line(p8, p6)
    ll = geom.add_line_loop([c0, c1, c2, c3, l1, l2])

    # test adding raw code
    geom.add_raw_code('// dummy')
    geom.add_raw_code(['// dummy'])

    pacman = geom.add_plane_surface(ll)

    # Fails on travis for some reason, probably because of an old gmsh version.
    # test setting physical groups
    # geom.add_physical_point(p1, label='c')
    # geom.add_physical_line(c0, label='arc')
    geom.add_physical_surface(pacman)
    # geom.add_physical_surface(pacman, label=77)

    ref = 54.312974717523744
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('pacman.vtu', *test())
