# -*- coding: utf-8 -*-
#
import pygmsh
import examples

import numpy
import os
import tempfile
from importlib import import_module
import subprocess


def test_generator():
    for name in examples.__all__:
        test = import_module('examples.' + name)
        yield check_output, test, name


def check_output(test, name):

    handle, filename = tempfile.mkstemp(
        prefix=name,
        suffix='.geo'
        )
    os.write(handle, test.generate())
    os.close(handle)

    print(filename)

    gmsh_out = subprocess.check_output(
        ['gmsh', '-3', filename],
        stderr=subprocess.STDOUT
        )

    return


def test_io():
    # generate a geometry
    import examples.screw as sc
    handle, filename = tempfile.mkstemp(
            prefix='screw',
            suffix='.geo'
            )
    os.write(handle, sc.generate(lcar=0.3))
    os.close(handle)

    # generate a mesh
    os.chdir(os.path.dirname(filename))
    gmsh_out = subprocess.check_output(
        ['gmsh', '-3', filename],
        stderr=subprocess.STDOUT
        )
    msh_file = filename.replace('.geo', '.msh')

    # read mesh data
    points, cells, field_data, point_data = pygmsh.read(msh_file)

    files = [
        filename.replace('.geo', '.vtk'),
        filename.replace('.geo', '.vtu'),
        ]

    # Don't test exodus yet, something funny is going on. When saving, exodus
    # reduces the number of points, as if to throw out unneccessary ones.
    # TODO investigate
    # filename.replace('.geo', '.e')

    for filename in files:
        yield _write_read, filename, points, cells

    return


def _write_read(filename, points, cells):
    '''Write and read a file, and make sure the data is the same as before.
    '''
    pygmsh.write(filename, points, cells)
    p, c, _, _ = pygmsh.read(filename)

    # We cannot compare the exact rows here since the order of the points might
    # have changes. Just compare the sums
    assert numpy.allclose(points, p)
    assert numpy.array_equal(cells, c)
    return

if __name__ == '__main__':
    test_io()
