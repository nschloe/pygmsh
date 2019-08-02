import pygmsh
from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()

    poly = geom.add_polygon(
        [[0.0, 0.5, 0.0], [1.0, 0.5, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]], lcar=0.05
    )

    geom.symmetry(poly, [0.0, 1.0, 0.0, -0.5])

    mesh = pygmsh.generate_mesh(geom)
    ref = 1.0
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("symmetry.vtk", test())
