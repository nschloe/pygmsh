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
    handle, tmp_base = tempfile.mkstemp(prefix=name)
    with open(handle, 'w') as f:
        f.write(test.generate())

    gmsh_out = subprocess.check_output(
        ['gmsh', '-3', handle],
        stderr=subprocess.STDOUT
        )
