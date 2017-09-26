#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygmsh as pg


def generate():
    lcar = 0.1

    if pg.get_gmsh_major_version() == 2:
        geom = pg.Geometry()
        rectangle = geom.add_rectangle(
                -1.0, 1.0,
                -1.0, 1.0,
                0.0,
                lcar
                )
        return geom, 4.0

    # boolean operations are only supported with OpenCASCADE
    geom = pg.Geometry(factory_type='OpenCASCADE')
    rectangle = geom.add_rectangle(
            -1.0, 1.0,
            -1.0, 1.0,
            0.0,
            lcar
            )

    circle_w = geom.add_circle(
            [-1.0, 0.0, 0.0],
            0.5,
            lcar,
            num_sections=4
            )

    circle_e = geom.add_circle(
            [1.0, 0.0, 0.0],
            0.5,
            lcar,
            num_sections=4
            )

    geom.boolean_union(
        [rectangle.surface],
        [circle_w.plane_surface, circle_e.plane_surface]
        )

    rectangle2 = geom.add_rectangle(
            2.0, 4.0,
            -1.0, 1.0,
            0.0,
            lcar
            )
    circle2_w = geom.add_circle(
            [2.0, 0.0, 0.0],
            0.5,
            lcar,
            num_sections=4
            )

    circle2_e = geom.add_circle(
            [4.0, 0.0, 0.0],
            0.5,
            lcar,
            num_sections=4
            )

    geom.boolean_intersection(
        [rectangle2.surface],
        [circle2_w.plane_surface, circle2_e.plane_surface]
        )

    rectangle3 = geom.add_rectangle(
            5.0, 7.0,
            -1.0, 1.0,
            0.0,
            lcar
            )
    circle3_w = geom.add_circle(
            [5.0, 0.0, 0.0],
            0.5,
            lcar,
            num_sections=4
            )

    circle3_e = geom.add_circle(
            [7.0, 0.0, 0.0],
            0.5,
            lcar,
            num_sections=4
            )

    geom.boolean_difference(
        [rectangle3.surface],
        [circle3_w.plane_surface, circle3_e.plane_surface]
        )

    return geom, 4.780361 + 0.7803612 + 3.2196387


if __name__ == '__main__':
    import meshio
    geometry, _ = generate()
    with open('boolean.geo', 'w') as f:
        f.write(geometry.get_code())
    out = pg.generate_mesh(geometry)
    meshio.write('boolean.vtu', *out)
