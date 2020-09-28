from math import pi

from helpers import compute_volume

import pygmsh


def test(mesh_size=0.05):
    with pygmsh.geo.Geometry() as geom:
        # Draw a square
        poly = geom.add_polygon(
            [
                [+0.5, +0.0, 0.0],
                [+0.0, +0.5, 0.0],
                [-0.5, +0.0, 0.0],
                [+0.0, -0.5, 0.0],
            ],
            mesh_size=mesh_size,
        )
        axis = [0, 0, 1.0]
        geom.twist(
            poly,
            translation_axis=axis,
            rotation_axis=axis,
            point_on_axis=[0.0, 0.0, 0.0],
            angle=0.5 * pi,
            num_layers=5,
            recombine=True,
        )
        mesh = geom.generate_mesh()

    ref = 3.98156496566
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("rotated_layers.vtu")
