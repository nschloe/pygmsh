#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pygmsh

from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()

    # internal radius of torus
    irad = 0.15
    # external radius of torus
    orad = 0.27

    Z_pos = (irad+orad) * np.concatenate([
        +np.ones(8),
        -np.ones(8),
        +np.ones(8),
        -np.ones(8)
        ])

    Alpha = np.concatenate([
        np.arange(8) * np.pi/4.0,
        np.arange(8) * np.pi/4.0 + np.pi/16.0,
        np.arange(8) * np.pi/4.0,
        np.arange(8) * np.pi/4.0 + np.pi/16.0
        ])

    # pylint: disable=no-member
    A1 = (irad+orad) / np.tan(np.pi/8.0) * \
        np.concatenate([
            1.6*np.ones(8),
            1.6*np.ones(8),
            1.9*np.ones(8),
            1.9*np.ones(8)
            ])

    for alpha, a1, z in zip(Alpha, A1, Z_pos):
        # Rotate torus to the y-z-plane.
        R1 = pygmsh.rotation_matrix([0.0, 1.0, 0.0], 0.5*np.pi)
        R2 = pygmsh.rotation_matrix([0.0, 0.0, 1.0], alpha)
        x0 = np.array([a1, 0.0, 0.0])
        x1 = np.array([0.0, 0.0, z])
        # First rotate to y-z-plane, then move out to a1, rotate by angle
        # alpha, move up by z.
        #
        #    xnew = R2*(R1*x+x0) + x1
        #
        geom.add_torus(
            irad=irad,
            orad=orad,
            lcar=0.1,
            R=np.dot(R2, R1),
            x0=np.dot(R2, x0) + x1
            )

    geom.add_box(
        -1.0, 1.0,
        -1.0, 1.0,
        -1.0, 1.0,
        lcar=0.3
        )

    ref = len(A1) * 2 * np.pi ** 2 * orad * irad ** 2 + 2.0 ** 3
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert np.isclose(compute_volume(points, cells), ref, rtol=2e-2)
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('torus_crowd.vtu', *test())
