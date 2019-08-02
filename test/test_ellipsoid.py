"""
Creates a mesh for an ellipsoid.
"""
import pygmsh
from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()
    geom.add_ellipsoid([0.0, 0.0, 0.0], [1.0, 0.5, 0.75], 0.05)

    ref = 1.5676038497587947
    mesh = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("ellipsoid.vtu", test())
