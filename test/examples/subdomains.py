#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import pygmsh


def generate():
    geom = pygmsh.Geometry()

    lcar = 0.1

    circle = geom.add_circle([0.5, 0.5, 0.0], 1.0, lcar)
    cll = geom.add_line_loop(circle)
    geom.add_plane_surface(cll)

    triangle, tl, _ = geom.add_polygon([
            [2.0, -0.5, 0.0],
            [4.0, -0.5, 0.0],
            [4.0, 1.5, 0.0],
            ], lcar
            )
    rectangle, rll, _ = geom.add_rectangle(4.75, 6.25, -0.24, 1.25, 0.0, lcar)

    # hold all domain
    ll, _ = geom.add_polygon_loop([
        [-1.0, -1.0, 0.0],
        [+7.0, -1.0, 0.0],
        [+7.0, +2.0, 0.0],
        [-1.0, +2.0, 0.0],
        ], lcar
        )

    geom.add_plane_surface([ll, cll, tl, rll])

    return geom


if __name__ == '__main__':
    import meshio
    points, cells, point_data, cell_data, _ = pygmsh.generate_mesh(generate())
    meshio.write(
            'subdomains.vtu',
            points,
            cells,
            point_data=point_data,
            cell_data=cell_data
            )
