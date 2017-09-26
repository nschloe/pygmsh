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
        characteristic_length_min=0.1,
        characteristic_length_max=0.1,
        )
    rectangle = geom.add_rectangle(
            -1.0, -1.0, 0.0,
            2.0, 2.0
            )

    # circle_w = geom.add_circle(
    #         [-1.0, 0.0, 0.0],
    #         0.5,
    #         lcar,
    #         num_sections=4
    #         )

    # circle_e = geom.add_circle(
    #         [1.0, 0.0, 0.0],
    #         0.5,
    #         lcar,
    #         num_sections=4
    #         )

    # geom.boolean_union(
    #     [rectangle.surface],
    #     [circle_w.plane_surface, circle_e.plane_surface]
    #     )

    # rectangle2 = geom.add_rectangle(
    #         2.0, 4.0,
    #         -1.0, 1.0,
    #         0.0,
    #         lcar
    #         )
    # circle2_w = geom.add_circle(
    #         [2.0, 0.0, 0.0],
    #         0.5,
    #         lcar,
    #         num_sections=4
    #         )

    # circle2_e = geom.add_circle(
    #         [4.0, 0.0, 0.0],
    #         0.5,
    #         lcar,
    #         num_sections=4
    #         )

    # geom.boolean_intersection(
    #     [rectangle2.surface],
    #     [circle2_w.plane_surface, circle2_e.plane_surface]
    #     )

    # rectangle3 = geom.add_rectangle(
    #         5.0, 7.0,
    #         -1.0, 1.0,
    #         0.0,
    #         lcar
    #         )
    # circle3_w = geom.add_circle(
    #         [5.0, 0.0, 0.0],
    #         0.5,
    #         lcar,
    #         num_sections=4
    #         )

    # circle3_e = geom.add_circle(
    #         [7.0, 0.0, 0.0],
    #         0.5,
    #         lcar,
    #         num_sections=4
    #         )

    # geom.boolean_difference(
    #     [rectangle3.surface],
    #     [circle3_w.plane_surface, circle3_e.plane_surface]
    #     )

    ref = 4.780361 + 0.7803612 + 3.2196387
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    # assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('boolean.vtu', *test())
