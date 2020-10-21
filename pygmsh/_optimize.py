from pathlib import Path
import tempfile

import gmsh
import numpy
import meshio


def optimize(mesh, method="", verbose=False):
    mesh.remove_lower_dimensional_cells()
    mesh.cell_data = {}

    if verbose:
        import meshplex
        meshplex_mesh = meshplex.from_meshio(mesh)
        print_stats(meshplex_mesh)

    # optimize
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdir = Path(tmpdirname)
        tmpfile = tmpdir / "tmp.msh"
        mesh.write(tmpfile)
        gmsh.initialize()
        gmsh.merge(str(tmpfile))
        # We need force=True because we're reading from a discrete mesh
        gmsh.model.mesh.optimize(method, force=True)
        gmsh.write(str(tmpfile))
        gmsh.finalize()
        mesh = meshio.read(tmpfile)

    if verbose:
        meshplex_mesh = meshplex.from_meshio(mesh)
        print_stats(meshplex_mesh)
    return mesh


def print_stats(mesh):
    import termplotlib
    q = mesh.q_radius_ratio
    q_hist, q_bin_edges = numpy.histogram(
        q, bins=numpy.linspace(0.0, 1.0, num=41, endpoint=True)
    )

    grid = termplotlib.subplot_grid((1, 2), column_widths=None, border_style=None)
    grid[0, 0].hist(q_hist, q_bin_edges, bar_width=1, strip=True)
    grid[0, 1].aprint("min quality: {:5.3f}".format(numpy.min(q)))
    grid[0, 1].aprint("avg quality: {:5.3f}".format(numpy.average(q)))
    grid[0, 1].aprint("max quality: {:5.3f}".format(numpy.max(q)))

    grid.show()
