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
        yield check_output, test


def check_output(test):
    pygmsh.generate_mesh(test.generate())
    return


if __name__ == '__main__':
    test_io()
