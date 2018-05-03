#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygmsh

from helpers import compute_volume


def test():
    geom = pygmsh.opencascade.Geometry(
        characteristic_length_min=0.1,
        characteristic_length_max=0.1,
        )

    p0 = geom.add_point([-0.5, -0.5, 0], 0.01)
    p1 = geom.add_point([+0.5, -0.5, 0], 0.01)
    p2 = geom.add_point([+0.5, +0.5, 0], 0.01)
    p3 = geom.add_point([-0.5, +0.5, 0], 0.01)
    l0 = geom.add_line(p0, p1)
    l1 = geom.add_line(p1, p2)
    l2 = geom.add_line(p2, p3)
    l3 = geom.add_line(p3, p0)
    ll0 = geom.add_line_loop([l0, l1, l2, l3])
    square_builtin = geom.add_plane_surface(ll0)
    square_opencascade = geom.add_rectangle([0, 0, 0], 1.0, 1.0)
    geom.boolean_difference([square_opencascade], [square_builtin])

    ref = 0.75
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    out = test()
    meshio.write('mix.vtu', *out)
