#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Simple example of use of pygmsh's geom.extrude translation method

:author: S.G. Mallinson <samuel>

:created: 2017-08-02

'''

from __future__ import absolute_import, division, print_function

from numpy import isclose, array, linalg, hstack, ones, sqrt, pi

from pygmsh import Geometry

from pandas import read_csv

tol = 1.0e-6


def close_by(x, y, tol):

    # check if two values are close to each other, within tol(erance)

    return isclose(x, y, rtol=0, atol=tol)


def centre_and_radius(start, middle, end):
    '''return the centre and radius of the circumcircle

    See Jones (1912, p. 129)

    '''
    print(start, middle, end)
    x = array([start[:2], middle[:2], end[:2]])  # points on yz-plane
    print(x)

    cr = linalg.solve(hstack([2 * x,
                              ones([3, 1])]), (x**2).sum(1))

    centre = cr[:2]
    radius = sqrt(sum(centre**2) + cr[2])

    return centre, radius


def generate(filename):

    data = read_csv(filename, sep=',',
                    names=['x', 'y', 'z', 'label', 'size'])

    geom = Geometry()

    points = map(lambda v: geom.add_point([v[1]['x'], v[1]['y'], v[1]['z']],
                 v[1]['size']), data.iterrows())

    edges = []

    curves = ['line', 'arc', 'line', 'line', 'line',
              'arc', 'line', 'line']

    ic = 0
    for curve in curves:
        if curve == 'line':
            terminus = (ic + 1) % len(points)
            edges.append(geom.add_line(points[ic], points[terminus]))
            ic = terminus
        elif curve == 'arc':
            terminus = (ic + 2) % len(points)
            centre, radius = centre_and_radius(points[ic].x,
                                               points[ic + 1].x,
                                               points[terminus].x)
            print (centre, radius)
            c = geom.add_point([centre[0], centre[1], 0], 1.0)
            edges.append(geom.add_circle_arc(points[ic],
                                             c,
                                             points[terminus]))
            ic = terminus

    line_loop = geom.add_line_loop(edges)
    surface = geom.add_plane_surface(line_loop)
    physical_surface = geom.add_physical_surface(surface, 'front')
    print(physical_surface)

    axis = [0, 0, 1]

    top, volume, lat = geom.extrude(surface, translation_axis=axis,
                                    layers=1, recombine=True)

    physical_volume = geom.add_physical_volume(volume)
    print(physical_volume)

    with open(filename[:-4] + '.geo', 'w') as fout:
        fout.write(geom.get_code())
        fout.write('\nRecombine Surface{s0};')
        fout.write('\nMesh.RecombineAll=1;')

    return geom, (16.0 + 2.0 * pi)

if __name__ == '__main__':

    from sys import argv

    geometry, area = generate(argv[1])
