import numpy


def rotation_matrix(u, theta):
    """Return matrix that implements the rotation around the vector :math:`u`
    by the angle :math:`\\theta`, cf.
    https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle.

    :param u: rotation vector
    :param theta: rotation angle
    """
    assert numpy.isclose(numpy.inner(u, u), 1.0), "the rotation axis must be unitary"

    # Cross-product matrix.
    cpm = numpy.array([[0.0, -u[2], u[1]], [u[2], 0.0, -u[0]], [-u[1], u[0], 0.0]])
    c = numpy.cos(theta)
    s = numpy.sin(theta)
    R = numpy.eye(3) * c + s * cpm + (1.0 - c) * numpy.outer(u, u)
    return R


def orient_lines(lines):
    """Given a sequence of unordered and unoriented lines defining a closed polygon,
    returns a reordered list of reoriented lines of that polygon.

    :param lines: a sequence of lines defining a closed polygon
    """
    # Categorise graph edges by their vertex pair ids
    point_pair_ids = numpy.array(
        [[line.points[0]._ID, line.points[1]._ID] for line in lines]
    )

    # Indices of reordering
    order = numpy.arange(len(point_pair_ids), dtype=int)
    # Compute orientations where oriented[j] == False requires edge j to be reversed
    oriented = numpy.array([True] * len(point_pair_ids), dtype=numpy.bool)

    for j in range(1, len(point_pair_ids)):
        out = point_pair_ids[j - 1, 1]  # edge out from vertex
        inn = point_pair_ids[j:, 0]  # candidates for edge into vertices
        wh = numpy.where(inn == out)[0] + j
        if len(wh) == 0:
            # look for candidates in those which are not correctly oriented
            inn = point_pair_ids[j:, 1]
            wh = numpy.where(inn == out)[0] + j
            # reorient remaining edges
            point_pair_ids[j:] = numpy.flip(point_pair_ids[j:], axis=1)
            oriented[j:] ^= True

        # reorder
        point_pair_ids[[j, wh[0]]] = point_pair_ids[[wh[0], j]]
        order[[j, wh[0]]] = order[[wh[0], j]]

    # Reconstruct an ordered and oriented line loop
    lines = [lines[o] for o in order]
    lines = [lines[j] if oriented[j] else -lines[j] for j in range(len(oriented))]

    return lines
