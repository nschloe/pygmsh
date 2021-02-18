import gmsh
import meshio
import numpy as np


def write(filename: str):
    import gmsh

    gmsh.write(filename)


def rotation_matrix(u, theta):
    """Return matrix that implements the rotation around the vector :math:`u`
    by the angle :math:`\\theta`, cf.
    https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle.

    :param u: rotation vector
    :param theta: rotation angle
    """
    assert np.isclose(np.inner(u, u), 1.0), "the rotation axis must be unitary"

    # Cross-product matrix.
    cpm = np.array([[0.0, -u[2], u[1]], [u[2], 0.0, -u[0]], [-u[1], u[0], 0.0]])
    c = np.cos(theta)
    s = np.sin(theta)
    R = np.eye(3) * c + s * cpm + (1.0 - c) * np.outer(u, u)
    return R


def orient_lines(lines):
    """Given a sequence of unordered and unoriented lines defining a closed polygon,
    returns a reordered list of reoriented lines of that polygon.

    :param lines: a sequence of lines defining a closed polygon
    """
    # Categorise graph edges by their vertex pair ids
    point_pair_ids = np.array(
        [[line.points[0]._id, line.points[1]._id] for line in lines]
    )

    # Indices of reordering
    order = np.arange(len(point_pair_ids), dtype=int)
    # Compute orientations where oriented[j] == False requires edge j to be reversed
    oriented = np.array([True] * len(point_pair_ids), dtype=bool)

    for j in range(1, len(point_pair_ids)):
        out = point_pair_ids[j - 1, 1]  # edge out from vertex
        inn = point_pair_ids[j:, 0]  # candidates for edge into vertices
        wh = np.where(inn == out)[0] + j
        if len(wh) == 0:
            # look for candidates in those which are not correctly oriented
            inn = point_pair_ids[j:, 1]
            wh = np.where(inn == out)[0] + j
            # reorient remaining edges
            point_pair_ids[j:] = np.flip(point_pair_ids[j:], axis=1)
            oriented[j:] ^= True

        # reorder
        point_pair_ids[[j, wh[0]]] = point_pair_ids[[wh[0], j]]
        order[[j, wh[0]]] = order[[wh[0], j]]

    # Reconstruct an ordered and oriented line loop
    lines = [lines[o] for o in order]
    lines = [lines[j] if oriented[j] else -lines[j] for j in range(len(oriented))]

    return lines


def extract_to_meshio():
    # extract point coords
    idx, points, _ = gmsh.model.mesh.getNodes()
    points = np.asarray(points).reshape(-1, 3)
    idx -= 1
    srt = np.argsort(idx)
    assert np.all(idx[srt] == np.arange(len(idx)))
    points = points[srt]

    # extract cells
    elem_types, elem_tags, node_tags = gmsh.model.mesh.getElements()
    cells = []
    for elem_type, node_tags in zip(elem_types, node_tags):
        # `elementName', `dim', `order', `numNodes', `localNodeCoord',
        # `numPrimaryNodes'
        num_nodes_per_cell = gmsh.model.mesh.getElementProperties(elem_type)[3]
        meshio.gmsh.gmsh_to_meshio_type
        cells.append(
            meshio.CellBlock(
                meshio.gmsh.gmsh_to_meshio_type[elem_type],
                np.asarray(node_tags).reshape(-1, num_nodes_per_cell) - 1,
            )
        )

    cell_sets = {}
    for dim, tag in gmsh.model.getPhysicalGroups():
        name = gmsh.model.getPhysicalName(dim, tag)
        cell_sets[name] = [[] for _ in range(len(cells))]
        for e in gmsh.model.getEntitiesForPhysicalGroup(dim, tag):
            # TODO node_tags?
            # elem_types, elem_tags, node_tags
            elem_types, elem_tags, _ = gmsh.model.mesh.getElements(dim, e)
            assert len(elem_types) == len(elem_tags)
            assert len(elem_types) == 1
            elem_type = elem_types[0]
            elem_tags = elem_tags[0]

            meshio_cell_type = meshio.gmsh.gmsh_to_meshio_type[elem_type]
            # make sure that the cell type appears only once in the cell list
            # -- for now
            idx = []
            for k, cell_block in enumerate(cells):
                if cell_block.type == meshio_cell_type:
                    idx.append(k)
            assert len(idx) == 1
            idx = idx[0]
            cell_sets[name][idx].append(elem_tags - 1)

        cell_sets[name] = [
            (None if len(idcs) == 0 else np.concatenate(idcs))
            for idcs in cell_sets[name]
        ]

    # make meshio mesh
    return meshio.Mesh(points, cells, cell_sets=cell_sets)
