#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import permutations

import pygmsh

from helpers import compute_volume


def test(lcar=1.):
    lbw = [2, 3, 5]
    geom = pygmsh.built_in.Geometry()
    points = [geom.add_point([x, 0., 0.], lcar) for x in [0., lbw[0]]]
    line = geom.add_line(*points)

    _, rectangle, _ = geom.extrude(line,
                                   translation_axis=[0., lbw[1], 0.],
                                   num_layers=lbw[1],
                                   recombine=True)
    geom.extrude(rectangle,
                 translation_axis=[0., 0., lbw[2]],
                 num_layers=lbw[2],
                 recombine=True)

    # compute_volume only supports 3D for tetras, but does return
    # surface area for quads

    ref = sum(l * w for l, w in permutations(lbw, 2))  # surface area
    points, cells, _, _, _ = pygmsh.generate_mesh(geom, prune_vertices=False)
    # TODO compute hex volumes
    assert abs(
        compute_volume(points, {'quad': cells['quad']}) - ref
        ) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('hex.vtu', *test())
