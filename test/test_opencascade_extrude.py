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
    geom = pygmsh.opencascade.Geometry()

    rectangle = geom.add_rectangle(
        [-1.0, -1.0, 0.0], 2.0, 2.0,
        corner_radius=0.2,
        char_length=0.05
        )
    disk1 = geom.add_disk([-1.2, 0.0, 0.0], 0.5)
    disk2 = geom.add_disk([+1.2, 0.0, 0.0], 0.5, 0.3)
    union = geom.boolean_union([rectangle, disk1, disk2])

    disk3 = geom.add_disk([0.0, -0.9, 0.0], 0.5)
    disk4 = geom.add_disk([0.0, +0.9, 0.0], 0.5)
    flat = geom.boolean_difference([union], [disk3, disk4])

    geom.extrude(flat, [0, 0, 0.3])

    ref = 1.1742114942
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('opencascade_extrude.vtu', *test())
