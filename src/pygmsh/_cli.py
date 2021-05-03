import argparse
from sys import version_info

import meshio

from .__about__ import __gmsh_version__, __version__
from ._optimize import optimize


def optimize_cli(argv=None):
    parser = argparse.ArgumentParser(
        description=("Optimize mesh."),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("infile", type=str, help="mesh to optimize")
    parser.add_argument("outfile", type=str, help="optimized mesh")

    parser.add_argument(
        "-q",
        "--quiet",
        dest="verbose",
        action="store_false",
        default=True,
        help="suppress output",
    )

    parser.add_argument(
        "-m",
        "--method",
        default="",
        # Valid choices are on
        # https://gmsh.info/doc/texinfo/gmsh.html#Namespace-gmsh_002fmodel_002fmesh
        help='method (e.g., "", Netgen, ...)',
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=_get_version_text(),
        help="display version information",
    )
    args = parser.parse_args(argv)

    mesh = meshio.read(args.infile)
    optimize(mesh, method=args.method, verbose=args.verbose).write(args.outfile)


def _get_version_text():
    return "\n".join(
        [
            f"pygmsh {__version__} "
            f"[Gmsh {__gmsh_version__}, "
            f"Python {version_info.major}.{version_info.minor}.{version_info.micro}]",
            "Copyright (c) 2013-2020 Nico Schlömer et al.",
        ]
    )
