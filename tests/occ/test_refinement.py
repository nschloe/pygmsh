from math import sqrt

import pytest

import pygmsh


@pytest.mark.skip("Only works in Gmsh 4.7.0+")
def test():
    with pygmsh.occ.Geometry() as geom:
        geom.add_ball([0.0, 0.0, 0.0], 1.0)
        geom.set_mesh_size_callback(
            lambda dim, tag, x, y, z: abs(sqrt(x ** 2 + y ** 2 + z ** 2) - 0.5) + 0.1
        )
        mesh = geom.generate_mesh()

    assert mesh.cells[0].data.shape[0] > 1500
