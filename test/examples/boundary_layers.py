#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygmsh as pg


def generate():
    geom = pg.Geometry()

    poly = geom.add_polygon([
        [0.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [3.0, 1.0, 0.0],
        [1.0, 2.0, 0.0],
        [0.0, 1.0, 0.0],
        ],
        lcar=0.1
        )

    field0 = geom.add_boundary_layer(
        edges_list=[poly.line_loop.lines[0]],
        hfar=0.1,
        hwall_n=0.01,
        hwall_t=0.01,
        ratio=1.1,
        thickness=0.2,
        anisomax=100.0
        )

    field1 = geom.add_boundary_layer(
        nodes_list=[poly.line_loop.lines[1].points[1]],
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
