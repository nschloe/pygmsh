#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygmsh

from helpers import compute_volume


def test():
    geom = pygmsh.opencascade.Geometry(
        characteristic_length_min=1.0,
        characteristic_length_max=1.0,
        )

    lcar = 1
    h = 25
    w = 10
    l = 100
    x_fin = -0.5*l
    cr = 1

    f = 0.5*w
    y = [-f, -f+cr, +f-cr, +f]
    z = [0.0, h-cr, h]
    f = 0.5 * cr
    x = [-f, f]
    points = []
    points.append(geom.add_point((x[0], y[0], z[0]), lcar=lcar))
    points.append(geom.add_point((x[0], y[0], z[1]), lcar=lcar))
    points.append(geom.add_point((x[0], y[1], z[1]), lcar=lcar))
    points.append(geom.add_point((x[0], y[1], z[2]), lcar=lcar))
    points.append(geom.add_point((x[0], y[2], z[2]), lcar=lcar))
    points.append(geom.add_point((x[0], y[2], z[1]), lcar=lcar))
    points.append(geom.add_point((x[0], y[3], z[1]), lcar=lcar))
    points.append(geom.add_point((x[0], y[3], z[0]), lcar=lcar))

    lines = []
    lines.append(geom.add_line(points[0], points[1]))
    lines.append(geom.add_circle_arc(points[1], points[2], points[3]))

    lines.append(geom.add_line(points[3], points[4]))
    lines.append(geom.add_circle_arc(points[4], points[5], points[6]))
    lines.append(geom.add_line(points[6], points[7]))
    lines.append(geom.add_line(points[7], points[0]))

    line_loop = geom.add_line_loop(lines)
    surface = geom.add_plane_surface(line_loop)
    vol = geom.extrude(surface, translation_axis=[l, 0, 0])

    points, cells, _, _, _ = pygmsh.generate_mesh(geom)

    ref = 24941.503891355664
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('opencascade_extrude2.vtu', *test())
