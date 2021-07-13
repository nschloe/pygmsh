import meshio
import numpy as np
from helpers import compute_volume


def test_volume():
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [3.0, 0.0, 0.0],
            [3.0, 1.0, 0.0],
            [2.0, 1.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
        ]
    )
    cells = {
        "triangle": np.array([[0, 1, 6], [0, 6, 7]]),
        "quad": np.array([[1, 2, 5, 6], [2, 3, 4, 5]]),
    }
    vol = compute_volume(meshio.Mesh(points, cells))
    assert abs(vol - 3.0) < 1.0e-14
