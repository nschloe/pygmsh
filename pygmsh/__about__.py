import gmsh

__gmsh_version__ = gmsh.__version__

try:
    # Python 3.8
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

try:
    __version__ = metadata.version("pygmsh")
except Exception:
    __version__ = "unknown"
