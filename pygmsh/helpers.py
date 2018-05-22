# -*- coding: utf-8 -*-
#
from __future__ import print_function

import os
import subprocess
import tempfile

import numpy

import meshio


def rotation_matrix(u, theta):
    '''Return matrix that implements the rotation around the vector :math:`u`
    by the angle :math:`\\theta`, cf.
    https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle.

    :param u: rotation vector
    :param theta: rotation angle
    '''
    assert numpy.isclose(numpy.inner(u, u), 1.), \
        'the rotation axis must be unitary'

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
    return (
        macos_gmsh_location if os.path.isfile(macos_gmsh_location)
        else 'gmsh'
        )


def get_gmsh_major_version(gmsh_exe=_get_gmsh_exe()):
    out = subprocess.check_output(
            [gmsh_exe, '--version'],
            stderr=subprocess.STDOUT
            ).strip().decode('utf8')
    ex = out.split('.')
    return int(ex[0])


# pylint: disable=too-many-branches, too-many-statements
def generate_mesh(
        geo_object,
        verbose=True,
        dim=3,
        prune_vertices=True,
        remove_faces=False,
        gmsh_path=None,
        extra_gmsh_arguments=None,
        # for debugging purposes:
        geo_filename=None,
        fast_conversion=False,
        ):
    if extra_gmsh_arguments is None:
        extra_gmsh_arguments = []

    preserve_geo = geo_filename is not None
    if geo_filename is None:
        with tempfile.NamedTemporaryFile(suffix='.geo') as f:
            geo_filename = f.name

    with open(geo_filename, 'w') as f:
        f.write(geo_object.get_code())

    # Gmsh's native file format `msh` it not well suited for fast i/o. This can
    # greatly reduce the performance of pygmsh. As a workaround, use the VTK
    # format. Unfortunately, gmsh doesn't support physical and geoemtrical tags
    # for VTK yet. <https://gitlab.onelab.info/gmsh/gmsh/issues/389>
    if fast_conversion:
        filetype = 'vtk'
        suffix = '.vtk'
    else:
        filetype = 'msh'
        suffix = '.msh'

    with tempfile.NamedTemporaryFile(suffix=suffix) as handle:
        msh_filename = handle.name

    gmsh_executable = gmsh_path if gmsh_path is not None else _get_gmsh_exe()

    args = [
        '-{}'.format(dim), geo_filename,
        # Don't use the native msh format. It's not very well suited for
        # efficient reading as every cell has to be read individually.
        '-format', filetype,
        '-bin',
        '-o', msh_filename,
        ] + extra_gmsh_arguments

    # https://stackoverflow.com/a/803421/353337
    p = subprocess.Popen(
        [gmsh_executable] + args,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
    if verbose:
        while True:
            line = p.stdout.readline()
            if not line:
                break
            print(line.decode('utf-8'), end='')

    p.communicate()
    assert p.returncode == 0, \
        'Gmsh exited with error (return code {}).'.format(p.returncode)

    X, cells, pt_data, cell_data, field_data = meshio.read(msh_filename)

    if remove_faces:
        # Only keep the cells of highest topological dimension; discard faces
        # and such.
        two_d_cells = set(['triangle', 'quad'])
        three_d_cells = set([
            'tetra', 'hexahedron', 'wedge', 'pyramid', 'penta_prism',
            'hexa_prism'
            ])
        if any(k in cells for k in three_d_cells):
            keep_keys = three_d_cells.intersection(cells.keys())
        elif any(k in cells for k in two_d_cells):
            keep_keys = two_d_cells.intersection(cells.keys())
        else:
            keep_keys = cells.keys()

        cells = {key: cells[key] for key in keep_keys}
        cell_data = {key: cell_data[key] for key in keep_keys}

    if prune_vertices:
        # Make sure to include only those vertices which belong to a cell.
        ncells = numpy.concatenate([
            numpy.concatenate(c) for c in cells.values()
            ])
        uvertices, uidx = numpy.unique(ncells, return_inverse=True)

        k = 0
        for key in cells.keys():
            n = numpy.prod(cells[key].shape)
            cells[key] = uidx[k:k+n].reshape(cells[key].shape)
            k += n

        X = X[uvertices]
        for key in pt_data:
            pt_data[key] = pt_data[key][uvertices]

    # clean up
    os.remove(msh_filename)
    if preserve_geo:
        print('\ngeo file: {}'.format(geo_filename))
    else:
        os.remove(geo_filename)
    return X, cells, pt_data, cell_data, field_data
