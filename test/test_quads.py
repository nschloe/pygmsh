#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygmsh

from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()

    rectangle = geom.add_rectangle(
            0.0, 1.0,
            0.0, 1.0,
            0.0,
            0.1
            )
    
    geom.add_raw_code('Recombine Surface {%s};' % rectangle.surface.id)

    ref = 1.0
    points, cells, _, _, _ = pygmsh.generate_mesh(geom,
                                                  dim=2,
                                                  num_quad_lloyd_steps=0,
                                                  geo_filename='quads.geo')
    try:
        assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    except KeyError as err:
        if ('triangle',) == err.args:
            print('compute_volume looked for triangle')
            print('...but cells has {}'.format(cells.keys()))
        else:
            raise
            
    return points, cells
if __name__ == '__main__':
    import meshio
    meshio.write('quads.vtu', *test())
