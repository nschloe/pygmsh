#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

import pygmsh

from helpers import compute_volume


@pytest.mark.skipif(
    pygmsh.get_gmsh_major_version() < 3,
    reason='requires Gmsh >= 3'
    )
def test():
    geom = pygmsh.opencascade.Geometry(
        characteristic_length_min=2.0,
        characteristic_length_max=2.0,
        )

    rect1 = geom.add_rectangle(
        [10.0, 0.0, 0.0], 20.0, 40.0,
        corner_radius=5.0,
        )
    rect2 = geom.add_rectangle(
        [0.0, 10.0, 0.0], 40.0, 20.0,
        corner_radius=5.0
        )
    disk1 = geom.add_disk([14.5, 35.0, 0.0], 1.85)
    disk2 = geom.add_disk([25.5, 5.0, 0.0], 1.85)

    rect3 = geom.add_rectangle([10.0, 30.0, 0.0], 10.0, 1.0)
    rect4 = geom.add_rectangle([20.0, 9.0, 0.0], 10.0, 1.0)

    r1 = geom.add_rectangle([9.0, 0.0, 0.0], 21.0, 20.5, corner_radius=8.0)
    r2 = geom.add_rectangle([10.0, 00.0, 0.0], 20.0, 19.5, corner_radius=7.0)
    diff1 = geom.boolean_difference([r1], [r2])
    r22 = geom.add_rectangle([9.0, 10.0, 0.0], 11.0, 11.0)
    inter1 = geom.boolean_intersection([diff1, r22])

    r3 = geom.add_rectangle([10.0, 19.5, 0.0], 21.0, 21.0, corner_radius=8.0)
    r4 = geom.add_rectangle([10.0, 20.5, 0.0], 20.0, 20.0, corner_radius=7.0)
    diff2 = geom.boolean_difference([r3], [r4])
    r33 = geom.add_rectangle([20.0, 19.0, 0.0], 11.0, 11.0)
    inter2 = geom.boolean_intersection([diff2, r33])

    geom.boolean_difference(
        [rect1, rect2],
        [disk1, disk2, rect3, rect4, inter1, inter2]
        )

    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    ref = 1082.4470502181903
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    from helpers import plot
    plot('logo.png', *test())
    # import meshio
    # meshio.write('logo.vtu', *test())
