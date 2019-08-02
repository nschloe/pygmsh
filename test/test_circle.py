import pygmsh
from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()

    geom.add_circle(
        [0.0, 0.0, 0.0],
        1.0,
        lcar=0.1,
        num_sections=4,
        # If compound==False, the section borders have to be points of the
        # discretization. If using a compound circle, they don't; gmsh can
        # choose by itself where to point the circle points.
        compound=True,
    )

    ref = 3.1363871677682247
    mesh = pygmsh.generate_mesh(geom, prune_z_0=True)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("circle.vtk", test())
