import numpy as np

import pygmsh
from helpers import compute_volume


def test(radius=1.0):
    geom = pygmsh.built_in.Geometry()

    R = [
        pygmsh.rotation_matrix(np.eye(1, 3, d)[0], theta)
        for d, theta in enumerate(np.pi / np.array([2.0, 3.0, 5]))
    ]

    geom.add_circle([7.0, 11.0, 13.0], radius, 0.1, R[0] @ R[1] @ R[2])

    ref = np.pi * radius ** 2
    mesh = pygmsh.generate_mesh(geom)
    assert np.isclose(compute_volume(mesh), ref, rtol=1e-2)
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("circle_transformed.vtk", test())
