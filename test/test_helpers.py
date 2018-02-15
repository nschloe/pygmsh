"""Tests module for helpers in tests."""

import numpy as np

import pygmsh
from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()
    geom.add_circle([0, 0, 0], 1, 0.1, make_surface=False)
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert np.abs((compute_volume(points, cells) - 2 * np.pi) / np.pi / 2) < 1e-2


if __name__ == '__main__':
    test()
