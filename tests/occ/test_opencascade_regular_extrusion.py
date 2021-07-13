"""Creates regular cube mesh by extrusion.
"""
from helpers import compute_volume

import pygmsh


def test():
    x = 5
    y = 4
    z = 3
    x_layers = 10
    y_layers = 5
    z_layers = 3
    with pygmsh.occ.Geometry() as geom:
        p = geom.add_point([0, 0, 0], 1)
        _, l, _ = geom.extrude(p, [x, 0, 0], num_layers=x_layers)
        _, s, _ = geom.extrude(l, [0, y, 0], num_layers=y_layers)
        geom.extrude(s, [0, 0, z], num_layers=z_layers)
        mesh = geom.generate_mesh()

    ref_vol = x * y * z
    assert abs(compute_volume(mesh) - ref_vol) < 1.0e-2 * ref_vol

    # Each grid-cell from layered extrusion will result in 6 tetrahedrons.
    ref_tetras = 6 * x_layers * y_layers * z_layers
    assert len(mesh.cells_dict["tetra"]) == ref_tetras

    return mesh


if __name__ == "__main__":
    test().write("cube.vtu")
