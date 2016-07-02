#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygmsh as pg


def generate():
    geom = pg.Geometry()

    lcar = 0.1
    p0 = geom.add_point([0.0, 0.0, 0.0], lcar)
    p1 = geom.add_point([2.0, 0.0, 0.0], lcar)
    p2 = geom.add_point([3.0, 1.0, 0.0], lcar)
    p3 = geom.add_point([1.0, 2.0, 0.0], lcar)
    p4 = geom.add_point([0.0, 1.0, 0.0], lcar)

    l0 = geom.add_line(p0, p1)
    l1 = geom.add_line(p1, p2)
    l2 = geom.add_line(p2, p3)
    l3 = geom.add_line(p3, p4)
    l4 = geom.add_line(p4, p0)

    ll = geom.add_line_loop([l0, l1, l2, l3, l4])

    surf = geom.add_plane_surface(ll)

    field0 = geom.add_boundary_layer(
        edges_list=[l0],
        hfar=0.1,
        hwall_n=0.01,
        hwall_t=0.01,
        ratio=1.1,
        thickness=0.2,
        anisomax=100.0
        )

    field1 = geom.add_boundary_layer(
        nodes_list=[p2],
        hfar=0.1,
        hwall_n=0.01,
        hwall_t=0.01,
        ratio=1.1,
        thickness=0.2,
        anisomax=100.0
        )

    geom.add_background_field([field0, field1])

    return geom


if __name__ == '__main__':
    import meshio
    points, cells = pg.generate_mesh(generate())
    meshio.write('boundary_layers.vtu', points, cells)
