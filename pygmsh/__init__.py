# -*- coding: utf-8 -*-
#
from __future__ import print_function

from . import built_in, opencascade
from .__about__ import __author__, __author_email__, __version__, __website__
from .helpers import generate_mesh, get_gmsh_major_version, rotation_matrix

__all__ = [
    "built_in",
    "opencascade",
    "generate_mesh",
    "get_gmsh_major_version",
    "rotation_matrix",
    "__version__",
    "__author__",
    "__author_email__",
    "__website__",
]

try:
    import pipdate
except ImportError:
    pass
else:
    if pipdate.needs_checking(__name__):
        print(pipdate.check(__name__, __version__), end="")
