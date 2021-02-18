import gmsh
import meshio
import numpy as np

from .helpers import extract_to_meshio


def optimize(mesh, method="", verbose=False):
    mesh.remove_lower_dimensional_cells()
    mesh.cell_data = {}

    # read into meshio like
    # <https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/demos/api/import_perf.py>
    gmsh.initialize()
    # add dummy entity
    dim = 3
    tag = gmsh.model.addDiscreteEntity(dim=dim)
    #
    nodes = np.arange(1, len(mesh.points) + 1)
    assert mesh.points.shape[1] == 3
    gmsh.model.mesh.addNodes(dim, tag, nodes, mesh.points.flat)
    for cell_block in mesh.cells:
        gmsh.model.mesh.addElementsByType(
            tag,
            meshio.gmsh.meshio_to_gmsh_type[cell_block.type],
            [],
            cell_block.data.flatten() + 1,
        )
    gmsh.model.mesh.optimize(method, force=True)
    mesh = extract_to_meshio()
    gmsh.finalize()

    # This writes a temporary file and reads it into gmsh ("merge"). There are other
    # ways of feeding gmsh a mesh
    # (https://gitlab.onelab.info/gmsh/gmsh/-/issues/1030#note_11435), but let's not do
    # that for now.
    # with tempfile.TemporaryDirectory() as tmpdirname:
    #     tmpdir = Path(tmpdirname)
    #     tmpfile = tmpdir / "tmp.msh"
    #     mesh.write(tmpfile)
    #     gmsh.initialize()
    #     if verbose:
    #         gmsh.option.setNumber("General.Terminal", 1)
    #     gmsh.merge(str(tmpfile))
    #     # We need force=True because we're reading from a discrete mesh
    #     gmsh.model.mesh.optimize(method, force=True)
    #     mesh = extract_to_meshio()
    #     gmsh.finalize()
    return mesh


def print_stats(mesh):
    import termplotlib

    q = mesh.q_radius_ratio
    q_hist, q_bin_edges = np.histogram(
        q, bins=np.linspace(0.0, 1.0, num=41, endpoint=True)
    )

    grid = termplotlib.subplot_grid((1, 2), column_widths=None, border_style=None)
    grid[0, 0].hist(q_hist, q_bin_edges, bar_width=1, strip=True)
    grid[0, 1].aprint("min quality: {:5.3f}".format(np.min(q)))
    grid[0, 1].aprint("avg quality: {:5.3f}".format(np.average(q)))
    grid[0, 1].aprint("max quality: {:5.3f}".format(np.max(q)))

    grid.show()
