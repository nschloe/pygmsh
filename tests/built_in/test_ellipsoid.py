"""
Creates a mesh for an ellipsoid.
"""
from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.geo.Geometry() as geom:
        geom.add_ellipsoid([0.0, 0.0, 0.0], [1.0, 0.5, 0.75], 0.05)
        mesh = geom.generate_mesh()
    ref = 1.5676038497587947
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("ellipsoid.vtu")
