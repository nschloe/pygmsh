#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a mesh for a square with a round hole.
'''
import pygmsh

from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()

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

    ref = 0.8086582838174551
    points, cells, _, _, _ = pygmsh.generate_mesh(geom, geo_filename='h.geo')
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('rectangle_with_hole.vtu', *test())
