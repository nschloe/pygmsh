# -*- coding: utf-8 -*-
#
from __future__ import print_function

import os
import subprocess
import tempfile

import meshio
import numpy
import voropy


def rotation_matrix(u, theta):
    '''Return matrix that implements the rotation around the vector :math:`u`
    by the angle :math:`\\theta`, cf.
    https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle.

    :param u: rotation vector
    :param theta: rotation angle
    '''
    # Cross-product matrix.
    cpm = numpy.array([
        [0.0, -u[2], u[1]],
        [u[2], 0.0, -u[0]],
        [-u[1], u[0], 0.0]
        ])
    c = numpy.cos(theta)
    s = numpy.sin(theta)
    R = numpy.eye(3) * c \
        + s * cpm \
        + (1.0 - c) * numpy.outer(u, u)
    return R


def _is_string(obj):
    try:
        # Python 2
        return isinstance(obj, basestring)
    except NameError:
        # Python 3
        return isinstance(obj, str)


def _is_flat(X, tol=1.0e-15):
    '''Checks if all points X sit in a plane.
    '''
    # find three points that don't sit on a line
    found = False
    for x2 in X:
        orth = numpy.cross(X[1] - X[0], x2 - X[0])
        orth_dot_orth = numpy.dot(orth, orth)
        if orth_dot_orth > tol:
            found = True
            break
    if not found:
        # All points even sit on a line
        return True
    norm_orth = numpy.sqrt(orth_dot_orth)
    norm_x_min_x0 = numpy.sqrt(numpy.einsum('ij, ij->i', X - X[0], X - X[0]))
    return (
        abs(numpy.dot(X - X[0], orth)) < tol * (1.0 + norm_orth*norm_x_min_x0)
        ).all()


def _get_gmsh_exe():
    macos_gmsh_location = '/Applications/Gmsh.app/Contents/MacOS/gmsh'
    if os.path.isfile(macos_gmsh_location):
        gmsh_executable = macos_gmsh_location
    else:
        gmsh_executable = 'gmsh'
    return gmsh_executable


def _get_gmsh_major_version():
    gmsh_exe = _get_gmsh_exe()
    out = subprocess.check_output(
            [gmsh_exe, '--version'],
            stderr=subprocess.STDOUT
            ).strip().decode('utf8')
    ex = out.split('.')
    return int(ex[0])


def generate_mesh(
        geo_object,
        optimize=True,
        num_quad_lloyd_steps=10,
        num_lloyd_steps=1000,
        verbose=True,
        dim=3,
        prune_vertices=True
        ):
    handle, geo_filename = tempfile.mkstemp(suffix='.geo')
    os.write(handle, geo_object.get_code().encode())
    os.close(handle)

    handle, msh_filename = tempfile.mkstemp(suffix='.msh')

    gmsh_executable = _get_gmsh_exe()

    cmd = [
        gmsh_executable,
        '-{}'.format(dim), '-bin', geo_filename, '-o', msh_filename
        ]

    gmsh_major_version = _get_gmsh_major_version()
    if gmsh_major_version < 3 and optimize:
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

    p.communicate()
    assert p.returncode == 0,\
        'Gmsh exited with error (return code {}).'.format(p.returncode)

    X, cells, pt_data, cell_data, field_data = meshio.read(msh_filename)

    # clean up
    os.remove(geo_filename)
    os.remove(msh_filename)

    # Lloyd smoothing
    if not _is_flat(X) or 'triangle' not in cells:
        if verbose:
            print(
                'Not performing Lloyd smoothing '
                '(only works for flat triangular meshes).'
                )
        return X, cells, pt_data, cell_data, field_data
    if verbose:
        print('Lloyd smoothing...')
    # find submeshes
    a = cell_data['triangle']['geometrical']
    # http://stackoverflow.com/q/42740483/353337
    submesh_bools = {v: v == a for v in numpy.unique(a)}

    X, cells['triangle'] = voropy.smoothing.lloyd_submesh(
            X, cells['triangle'], submesh_bools,
            tol=0.0, max_steps=num_lloyd_steps,
            verbose=False
            )

    if prune_vertices:
        # Make sure to include only those vertices which belong to a triangle.
        uvertices, uidx = numpy.unique(cells['triangle'], return_inverse=True)
        cells = {'triangle': uidx.reshape(cells['triangle'].shape)}
        cell_data = {'triangle': cell_data['triangle']}
        X = X[uvertices]
        for key in pt_data:
            pt_data[key] = pt_data[key][uvertices]

    return X, cells, pt_data, cell_data, field_data
