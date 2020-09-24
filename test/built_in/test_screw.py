import numpy as np
from helpers import compute_volume

import pygmsh


def test(mesh_size=0.05):
    with pygmsh.built_in.Geometry() as geom:
        # Draw a cross with a circular hole
        circ = geom.add_circle([0.0, 0.0, 0.0], 0.1, mesh_size=mesh_size)
        poly = geom.add_polygon(
            [
                [+0.0, +0.5, 0.0],
                [-0.1, +0.1, 0.0],
                [-0.5, +0.0, 0.0],
                [-0.1, -0.1, 0.0],
                [+0.0, -0.5, 0.0],
                [+0.1, -0.1, 0.0],
                [+0.5, +0.0, 0.0],
                [+0.1, +0.1, 0.0],
            ],
            mesh_size=mesh_size,
            holes=[circ],
        )

        axis = [0, 0, 1.0]

        geom.extrude(
            poly,
            translation_axis=axis,
            rotation_axis=axis,
            point_on_axis=[0, 0, 0],
            angle=2.0 / 6.0 * np.pi,
        )
        mesh = pygmsh.generate_mesh(geom)

    ref = 0.16951514066385628
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("screw.vtu")
