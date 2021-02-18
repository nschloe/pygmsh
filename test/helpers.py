import math

import numpy as np


def prune_nodes(points, cells):
    # Only points/cells that actually used
    uvertices, uidx = np.unique(cells, return_inverse=True)
    cells = uidx.reshape(cells.shape)
    points = points[uvertices]
    return points, cells


def get_triangle_volumes(pts, cells):
    # Works in any dimension; taken from voropy
    local_idx = np.array([[1, 2], [2, 0], [0, 1]]).T
    idx_hierarchy = cells.T[local_idx]

    half_edge_coords = pts[idx_hierarchy[1]] - pts[idx_hierarchy[0]]
    ei_dot_ej = np.einsum(
        "ijk, ijk->ij", half_edge_coords[[1, 2, 0]], half_edge_coords[[2, 0, 1]]
    )

    vols = 0.5 * np.sqrt(
        +ei_dot_ej[2] * ei_dot_ej[0]
        + ei_dot_ej[0] * ei_dot_ej[1]
        + ei_dot_ej[1] * ei_dot_ej[2]
    )
    return vols


def get_simplex_volumes(pts, cells):
    """Signed volume of a simplex in nD. Note that signing only makes sense for
    n-simplices in R^n.
    """
    n = pts.shape[1]
    assert cells.shape[1] == n + 1

    p = pts[cells]
    p = np.concatenate([p, np.ones(list(p.shape[:2]) + [1])], axis=-1)
    return np.abs(np.linalg.det(p) / math.factorial(n))


def compute_volume(mesh):
    if "tetra" in mesh.cells_dict:
        vol = math.fsum(
            get_simplex_volumes(*prune_nodes(mesh.points, mesh.cells_dict["tetra"]))
        )
    elif "triangle" in mesh.cells_dict or "quad" in mesh.cells_dict:
        vol = 0.0
        if "triangle" in mesh.cells_dict:
            # triangles
            vol += math.fsum(
                get_triangle_volumes(
                    *prune_nodes(mesh.points, mesh.cells_dict["triangle"])
                )
            )
        if "quad" in mesh.cells_dict:
            # quad: treat as two triangles
            quads = mesh.cells_dict["quad"].T
            split_cells = np.column_stack(
                [[quads[0], quads[1], quads[2]], [quads[0], quads[2], quads[3]]]
            ).T
            vol += math.fsum(
                get_triangle_volumes(*prune_nodes(mesh.points, split_cells))
            )
    else:
        assert "line" in mesh.cells_dict
        segs = np.diff(mesh.points[mesh.cells_dict["line"]], axis=1).squeeze()
        vol = np.sum(np.sqrt(np.einsum("...j, ...j", segs, segs)))

    return vol


def plot(filename, points, triangles):
    from matplotlib import pyplot as plt

    pts = points[:, :2]
    for e in triangles:
        for idx in [[0, 1], [1, 2], [2, 0]]:
            X = pts[e[idx]]
            plt.plot(X[:, 0], X[:, 1], "-k")
    plt.gca().set_aspect("equal", "datalim")
    plt.axis("off")

    # plt.show()
    plt.savefig(filename, transparent=True)
