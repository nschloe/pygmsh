"""
Creates a mesh for a square with a round hole.
"""
from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.geo.Geometry() as geom:
        circle = geom.add_circle(
            x0=[0.5, 0.5, 0.0],
            radius=0.25,
            mesh_size=0.1,
            num_sections=4,
            make_surface=False,
        )
        geom.add_rectangle(
            0.0, 1.0, 0.0, 1.0, 0.0, mesh_size=0.1, holes=[circle.curve_loop]
        )
        mesh = geom.generate_mesh()

    ref = 0.8086582838174551
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("rectangle_with_hole.vtu")
