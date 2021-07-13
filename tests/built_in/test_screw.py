import numpy as np
from helpers import compute_volume

import pygmsh


def test(mesh_size=0.05):
    with pygmsh.geo.Geometry() as geom:
        # Draw a cross with a circular hole
        circ = geom.add_circle([0.0, 0.0], 0.1, mesh_size=mesh_size)
        poly = geom.add_polygon(
            [
                [+0.0, +0.5],
                [-0.1, +0.1],
                [-0.5, +0.0],
                [-0.1, -0.1],
                [+0.0, -0.5],
                [+0.1, -0.1],
                [+0.5, +0.0],
                [+0.1, +0.1],
            ],
            mesh_size=mesh_size,
            holes=[circ],
        )

        geom.twist(
            poly,
            translation_axis=[0.0, 0.0, 1.0],
            rotation_axis=[0.0, 0.0, 1.0],
            point_on_axis=[0.0, 0.0, 0.0],
            angle=2.0 / 6.0 * np.pi,
        )
        mesh = geom.generate_mesh()

    ref = 0.16951514066385628
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("screw.vtu")
