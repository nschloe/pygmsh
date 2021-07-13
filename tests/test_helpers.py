"""Tests module for helpers in tests."""
import numpy as np
from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.geo.Geometry() as geom:
        geom.add_circle([0, 0, 0], 1, 0.1, make_surface=False)
        mesh = geom.generate_mesh()
    ref = 2 * np.pi
    assert np.abs(compute_volume(mesh) - ref) < 1e-2 * ref


def test_save_geo():
    with pygmsh.geo.Geometry() as geom:
        geom.add_circle([0, 0, 0], 1, 0.1, make_surface=False)
        geom.save_geometry("out.geo_unrolled")


if __name__ == "__main__":
    test()
