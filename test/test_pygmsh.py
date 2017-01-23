# -*- coding: utf-8 -*-
#
import pygmsh
import examples

from importlib import import_module
import pytest


@pytest.mark.parametrize('name', examples.__all__)
def test_check_output(name):
    test = import_module('examples.' + name)
    pygmsh.generate_mesh(test.generate())
    return
