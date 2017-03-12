# -*- coding: utf-8 -*-
#
from __future__ import print_function
import numpy
import voropy
import sys

if sys.platform == 'darwin':
    # likely there.
    gmsh_executable = '/Applications/Gmsh.app/Contents/MacOS/gmsh'
else:
    gmsh_executable = 'gmsh'


def rotation_matrix(u, theta):
    '''Return matrix that implements the rotation around the vector :math:`u`
    by the angle :math:`\\theta`, cf.
    https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle.

    :param u: rotation vector
    :param theta: rotation angle
    '''
    # Cross-product matrix.
    cpm = numpy.array([
        [0.0,   -u[2],  u[1]],
        [u[2],    0.0, -u[0]],
        [-u[1],  u[0],  0.0]
        ])
    c = numpy.cos(theta)
    s = numpy.sin(theta)
    R = numpy.eye(3) * c \
        + s * cpm \
        + (1.0 - c) * numpy.outer(u, u)
    return R


def lloyd(X, cells, cell_data, num_lloyd_steps):

    if (abs(X[:, 2]) > 1.0e-15).any():
        print('Not performing Lloyd smoothing (only works for 2D meshes).')
        return X, cells

    # filter only the nodes used by the triangle cells
    uvertices, uidx = numpy.unique(cells['triangle'], return_inverse=True)
    cells = uidx.reshape(cells['triangle'].shape)
    X = X[uvertices]

    # find submeshes
    a = cell_data['triangle']['geometrical']
    # http://stackoverflow.com/q/42740483/353337
    submesh_dict = {v: numpy.where(v == a)[0] for v in set(a)}

    # perform lloyd on each submesh separately
    fcc_type = 'full'
    print('Lloyd smoothing...')
    for submesh_id, cell_ids in submesh_dict.items():
        print('    Subdomain %d...' % submesh_id)
        # Build submesh mesh.
        # Get cells
        submesh_cells = cells[cell_ids]
        # Get the vertices
        submesh_verts, uidx = \
            numpy.unique(submesh_cells, return_inverse=True)
        submesh_X = X[submesh_verts]
        #
        submesh_cells = uidx.reshape(submesh_cells.shape)

        submesh = voropy.mesh_tri.MeshTri(
            submesh_X, submesh_cells, flat_cell_correction=fcc_type
            )

        # Since we don't have access to the density field here, voropy's Lloyd
        # smoothing will always make all cells roughly equally large. This is
        # inappropriate if the mesh is meant to be inhomegenous, e.g., if there
        # are boundary layers. As a heuristic for inhomogenous meshes, check
        # the lengths of the longest and the shortest boundary edge. If they
        # are roughtly equal, perform Lloyd smoothing.
        submesh.create_edges()
        x = submesh_X[submesh.edges['nodes'][submesh.is_boundary_edge]]
        e = x[:, 0] - x[:, 1]
        edge_lengths2 = numpy.einsum('ij, ij->i', e, e)
        ratio = numpy.sqrt(max(edge_lengths2) / min(edge_lengths2))
        if ratio > 1.5:
            print((
                4*' ' + 'Subdomain boundary inhomogeneous ' +
                '(edge length ratio %1.3f). Skipping.'
                ) % ratio
                )
            continue

        mesh = voropy.smoothing.lloyd(
            submesh,
            tol=0.0,
            max_steps=num_lloyd_steps,
            flip_frequency=1,
            verbose=False,
            fcc_type=fcc_type,
            )
        # write the points and cells back
        X[submesh_verts] = mesh.node_coords
        cells[cell_ids] = submesh_verts[mesh.cells['nodes']]

    return X, {'triangle': cells}


def generate_mesh(
        geo_object,
        optimize=True,
        num_quad_lloyd_steps=10,
        num_lloyd_steps=1000,
        verbose=True
        ):
    import meshio
    import os
    import subprocess
    import tempfile

    handle, filename = tempfile.mkstemp(suffix='.geo')
    os.write(handle, geo_object.get_code().encode())
    os.close(handle)

    handle, outname = tempfile.mkstemp(suffix='.msh')

    cmd = [gmsh_executable, '-3', filename, '-o', outname]
    if optimize:
        cmd += ['-optimize']
    if num_quad_lloyd_steps > 0:
        cmd += ['-optimize_lloyd', str(num_quad_lloyd_steps)]

    # http://stackoverflow.com/a/803421/353337
    p = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
    if verbose:
        while True:
            line = p.stdout.readline()
            if not line:
                break
            print(line, end='')

    p.communicate()[0]
    if p.returncode != 0:
        raise RuntimeError(
            'Gmsh exited with error (return code %d).' %
            p.returncode
            )

    pts, cells, pt_data, cell_data, field_data = meshio.read(outname)
    pts, cells = lloyd(pts, cells, cell_data, num_lloyd_steps)

    return pts, cells, pt_data, cell_data, field_data
