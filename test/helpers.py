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


def plot(filename, points, cells):
    import matplotlib.pyplot as plt
    pts = points[:, :2]
    for e in cells['triangle']:
        for idx in [[0, 1], [1, 2], [2, 0]]:
            X = pts[e[idx]]
            plt.plot(X[:, 0], X[:, 1], '-k')
    plt.gca().set_aspect('equal', 'datalim')
    plt.axis('off')

    # plt.show()
    plt.savefig(filename, transparent=True)
    return
