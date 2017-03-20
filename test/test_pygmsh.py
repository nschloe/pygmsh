# -*- coding: utf-8 -*-
#
import pygmsh
import examples

from importlib import import_module
import math
import numpy
import pytest
import voropy


def _get_volume(points, cells):
    cells = \
        cells['tetra'] if 'tetra' in cells \
        else cells['triangle']

    # Only points/cells that actually used
    uvertices, uidx = numpy.unique(cells, return_inverse=True)
    cells = uidx.reshape(cells.shape)
    points = points[uvertices]

    if cells.shape[1] == 4:
        mesh = voropy.mesh_tetra.MeshTetra(points, cells)
    else:
        assert cells.shape[1] == 3
        mesh = voropy.mesh_tri.MeshTri(points, cells)
    return math.fsum(mesh.cell_volumes)


@pytest.mark.parametrize('name', examples.__all__)
def test_check_output(name):
    test = import_module('examples.' + name)
    geom, vol = test.generate()
    points, cells, point_data, cell_data, _ = pygmsh.generate_mesh(geom)

    vol2 = _get_volume(points, cells)
    assert abs(vol - vol2) < 1.0e-3 * vol
    return
