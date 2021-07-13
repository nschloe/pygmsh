from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.geo.Geometry() as geom:
        lcar = 0.1
        circle = geom.add_circle([0.5, 0.5, 0.0], 1.0, lcar)
        triangle = geom.add_polygon(
            [[2.0, -0.5, 0.0], [4.0, -0.5, 0.0], [4.0, 1.5, 0.0]], lcar
        )
        rectangle = geom.add_rectangle(4.75, 6.25, -0.24, 1.25, 0.0, lcar)
        # hold all domain
        geom.add_polygon(
            [
                [-1.0, -1.0, 0.0],
                [+7.0, -1.0, 0.0],
                [+7.0, +2.0, 0.0],
                [-1.0, +2.0, 0.0],
            ],
            lcar,
            holes=[circle.curve_loop, triangle.curve_loop, rectangle.curve_loop],
        )
        mesh = geom.generate_mesh()

    ref = 24.0
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("subdomains.vtu")
