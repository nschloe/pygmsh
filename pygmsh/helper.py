# -*- coding: utf-8 -*-
#
import numpy

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


def generate_mesh(geo_object, optimize=True):
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
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    print(out.decode())

    points, cells, _, _, _ = meshio.read(outname)

    return points, cells
