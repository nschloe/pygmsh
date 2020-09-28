import numpy as np
from helpers import compute_volume

import pygmsh


def test(radius=1.0):
    with pygmsh.geo.Geometry() as geom:
        R = [
            pygmsh.rotation_matrix(np.eye(1, 3, d)[0], theta)
            for d, theta in enumerate(np.pi / np.array([2.0, 3.0, 5]))
        ]
        geom.add_circle([7.0, 11.0, 13.0], radius, 0.1, R[0] @ R[1] @ R[2])
        ref = np.pi * radius ** 2
        mesh = geom.generate_mesh()

    assert np.isclose(compute_volume(mesh), ref, rtol=1e-2)
    return mesh


if __name__ == "__main__":
    test().write("circle_transformed.vtk")
