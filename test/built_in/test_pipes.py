import numpy as np
from helpers import compute_volume

import pygmsh


def test():
    """Pipe with double-ring enclosure, rotated in space."""
    with pygmsh.geo.Geometry() as geom:
        sqrt2on2 = 0.5 * np.sqrt(2.0)
        R = pygmsh.rotation_matrix([sqrt2on2, sqrt2on2, 0], np.pi / 6.0)
        geom.add_pipe(
            inner_radius=0.3, outer_radius=0.4, length=1.0, R=R, mesh_size=0.04
        )

        R = np.array([[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]])
        geom.add_pipe(
            inner_radius=0.3,
            outer_radius=0.4,
            length=1.0,
            mesh_size=0.04,
            R=R,
            variant="circle_extrusion",
        )
        mesh = geom.generate_mesh()

    ref = 0.43988203517453256
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("pipes.vtu")
