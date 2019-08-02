import pygmsh
from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()

    poly = geom.add_polygon(
        [
            [0, 0.3, 0],
            [0, 1.1, 0],
            [0.9, 1.1, 0],
            [0.9, 0.3, 0],
            [0.6, 0.7, 0],
            [0.3, 0.7, 0],
            [0.2, 0.4, 0],
        ],
        lcar=[0.2, 0.2, 0.2, 0.2, 0.03, 0.03, 0.01],
    )

    geom.in_surface(poly.lines[4], poly.surface)
    geom.in_surface(poly.points[6], poly.surface)

    ref = 0.505
    mesh = pygmsh.generate_mesh(geom, prune_z_0=True)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("test.vtk", test())
