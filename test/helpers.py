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
    if 'tetra' in cells:
        # 3D: only tetras supported
        mesh = voropy.mesh_tetra.MeshTetra(
            *prune_nodes(points, cells['tetra'])
            )
        vol = math.fsum(mesh.cell_volumes)
    elif 'triangle' in cells or 'quad' in cells:
        vol = 0.0
        if 'triangle' in cells:
            # triangles
            mesh = voropy.mesh_tri.MeshTri(
                *prune_nodes(points, cells['triangle'])
                )
            vol += math.fsum(mesh.cell_volumes)
        if 'quad' in cells:
            # quad: treat as two triangles
            quads = cells['quad'].T
            split_cells = numpy.column_stack([
                [quads[0], quads[1], quads[2]],
                [quads[0], quads[2], quads[3]],
                ]).T
            mesh = voropy.mesh_tri.MeshTri(*prune_nodes(points, split_cells))
            vol += math.fsum(mesh.cell_volumes)
    else:
        assert 'line' in cells
        segs = numpy.diff(points[cells['line']], axis=1).squeeze()
        vol = numpy.sum(numpy.sqrt(numpy.einsum('...j, ...j', segs, segs)))

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
