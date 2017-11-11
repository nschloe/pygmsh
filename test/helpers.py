# -*- coding: utf-8 -*-
#
import math
import numpy
import voropy


def compute_volume(points, cells):
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
