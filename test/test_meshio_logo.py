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
        characteristic_length_min=0.5,
        characteristic_length_max=0.5,
        )

    container = geom.add_rectangle([0.0, 0.0, 0.0], 10.0, 10.0)

    letter_i = geom.add_rectangle([2.0, 2.0, 0.0], 1.0, 4.5)
    i_dot = geom.add_disk([2.5, 7.5, 0.0], 0.6)

    disk1 = geom.add_disk([6.25, 4.5, 0.0], 2.5)
    disk2 = geom.add_disk([6.25, 4.5, 0.0], 1.5)
    letter_o = geom.boolean_difference([disk1], [disk2])

    geom.boolean_difference([container], [letter_i, i_dot, letter_o])

    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    ref = 81.9131851877
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    # import meshio
    # meshio.write('m.vtu', *test())
    from helpers import plot
    plot('meshio_logo.png', *test())
