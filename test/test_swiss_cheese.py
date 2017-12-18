#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pygmsh

from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()

    X0 = np.array([
        [+0.0, +0.0, 0.0],
        [+0.5, +0.3, 0.1],
        [-0.5, +0.3, 0.1],
        [+0.5, -0.3, 0.1]
        ])

    R = np.array([0.1, 0.2, 0.1, 0.14])

    holes = [
        geom.add_ball(x0, r, with_volume=False, lcar=0.2*r).surface_loop
        for x0, r in zip(X0, R)
        ]

    # geom.add_box(
    #         -1, 1,
    #         -1, 1,
    #         -1, 1,
    #         lcar=0.2,
    #         holes=holes
    #         )

    geom.add_ball([0, 0, 0], 1.0, lcar=0.2, holes=holes)

    # Fails on travis for some reason. TODO fix
    # geom.add_physical_volume(ball, label='cheese')

    ref = 4.07064892966291
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('swiss_cheese.vtu', *test())
