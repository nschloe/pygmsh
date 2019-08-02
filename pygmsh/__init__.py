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
