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
            print(line.decode('utf-8'), end='')

    p.communicate()[0]
    if p.returncode != 0:
        raise RuntimeError(
            'Gmsh exited with error (return code %d).' %
            p.returncode
            )

    X, cells, pt_data, cell_data, field_data = meshio.read(outname)

    # Lloyd smoothing
    if (abs(X[:, 2]) > 1.0e-15).any():
        print('Not performing Lloyd smoothing (only works for 2D meshes).')
        return X, cells, pt_data, cell_data, field_data
    print('Lloyd smoothing...')
    # find submeshes
    a = cell_data['triangle']['geometrical']
    # http://stackoverflow.com/q/42740483/353337
    submesh_bools = {v: v == a for v in numpy.unique(a)}

    cells['triangle'].sort(axis=1)
    cells['triangle'] = cells['triangle'][cells['triangle'][:, 0].argsort()]
    is_used = numpy.zeros(len(nodes), dtype=bool)
    is_used[cells['triangle'].flat] = True

    X, cells['triangle'] = voropy.smoothing.lloyd_submesh(
            X, cells['triangle'], submesh_bools,
            tol=0.0, max_steps=num_lloyd_steps,
            verbose=False
            )

    return X, cells, pt_data, cell_data, field_data
