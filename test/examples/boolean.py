#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygmsh as pg


def generate():
    geom = pg.Geometry()
    lcar = 0.1
    rectangle = geom.add_rectangle(
            -1.0, 1.0,
            -1.0, 1.0,
            0.0,
            lcar
            )

    if geom.get_gmsh_major() == 2:
        # boolean operations are not supported in gmsh 2
        return geom, 4.0

    circle_w = geom.add_circle(
            [-1.0, 0.0, 0.0],
            0.5,
            lcar,
            num_sections=4,
            )

    circle_e = geom.add_circle(
            [1.0, 0.0, 0.0],
            0.5,
            lcar,
            num_sections=4,
            )

    geom.set_factory('OpenCASCADE')
    _ = geom.boolean_difference(
        [rectangle.surface],
        [circle_w.plane_surface, circle_e.plane_surface]
        )

    # New points at intersections do not have a characteristic length set
    # and this creates errors with the OpenCASCADE factory.
    # This is most likely a gmsh bug. There is no way at the moment to
    # retrieve the indices of the intersecting points, as the only returned
    # value from the boolean operation is the new surface
    geom.add_raw_code('Characteristic Length {18, 16, 14, 12} = 0.1;')

    return geom, 3.2196387


if __name__ == '__main__':
    import meshio
    geometry, _ = generate()
    with open('boolean.geo', 'w') as f:
        f.write(geometry.get_code())
    out = pg.generate_mesh(geometry)
    meshio.write('boolean.vtu', *out)
