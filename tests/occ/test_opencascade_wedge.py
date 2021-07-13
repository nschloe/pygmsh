from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.occ.Geometry() as geom:
        geom.add_wedge([0.0, 0.0, 0.0], [1.0, 1.0, 1.0], top_extent=0.4, mesh_size=0.1)
        mesh = geom.generate_mesh()

    ref = 0.7
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("occ_wedge.vtu")
