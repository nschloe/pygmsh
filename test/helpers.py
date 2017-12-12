# -*- coding: utf-8 -*-
#
import math
import numpy
import voropy


def prune_nodes(points, cells):
    # Only points/cells that actually used
    uvertices, uidx = numpy.unique(cells, return_inverse=True)
    cells = uidx.reshape(cells.shape)
    points = points[uvertices]
    return points, cells


def compute_volume(points, cells):
    # is 3D
    is_3d = 'tetra' in cells

    # TODO multiple element types (e.g., triangles + quads)

    if is_3d:
        # tetra
        mesh = voropy.mesh_tetra.MeshTetra(
                *prune_nodes(points, cells['tetra'])
                )
        vol = math.fsum(mesh.cell_volumes)
    else:
        # triangles
        mesh = voropy.mesh_tri.MeshTri(*prune_nodes(points, cells['triangle']))
        vol_tri = math.fsum(mesh.cell_volumes)
        # quad: treat as two triangles
        quads = cells['quad'].T
        split_cells = numpy.column_stack([
            [quads[0], quads[1], quads[2]],
            [quads[0], quads[2], quads[3]],
            ]).T
        mesh = voropy.mesh_tri.MeshTri(*prune_nodes(points, split_cells))
        vol_quad = math.fsum(mesh.cell_volumes)
        vol = vol_tri + vol_quad

    return vol


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
