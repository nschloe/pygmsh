#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygmsh


def test(lcar=1.):
    geom = pygmsh.built_in.Geometry()
    poly = geom.add_polygon([
        [0., 0., 0.],
        [1., 0., 0.],
        [1., 1., 0.],
        [0., 1., 0.]],
        lcar
        )

    geom.set_transfinite_surface(poly.surface, size=[11, 9])

    points, cells, _, _, _ = pygmsh.generate_mesh(
        geom,
        geo_filename='transfinite.geo'
        )
    assert len(cells['triangle']) == 10*8*2
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('transfinite.vtu', *test())
