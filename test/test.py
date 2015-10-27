# -*- coding: utf-8 -*-
#
import pygmsh
import examples

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
    print(filename)

    with os.fdopen(handle, 'w') as h:
        h.write(test.generate())

    gmsh_out = subprocess.check_output(
        ['gmsh', '-3', filename],
        stderr=subprocess.STDOUT
        )

    return
