#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygmsh
import pytest

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

    rect5 = geom.add_rectangle([9.0, 10.0, 0.0], 1.0, 10.0)
    rect6 = geom.add_rectangle([30.0, 20.0, 0.0], 1.0, 10.0)
    rect7 = geom.add_rectangle([9.0, 19.5, 0.0], 22.0, 1.0)

    geom.boolean_difference(
            [rect1, rect2],
            [disk1, disk2, rect3, rect4, rect5, rect6, rect7]
            )

    points, cells, _, _, _ = pygmsh.generate_mesh(geom, num_lloyd_steps=0)
    ref = 1074.28954128
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('logo.vtu', *test())
