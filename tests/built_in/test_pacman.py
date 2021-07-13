from helpers import compute_volume
from numpy import cos, pi, sin

import pygmsh


def test(lcar=0.3):
    with pygmsh.geo.Geometry() as geom:
        r = 1.25 * 3.4
        p1 = geom.add_point([0.0, 0.0, 0.0], lcar)
        # p2 = geom.add_point([+r, 0.0, 0.0], lcar)
        p3 = geom.add_point([-r, 0.0, 0.0], lcar)
        p4 = geom.add_point([0.0, +r, 0.0], lcar)
        p5 = geom.add_point([0.0, -r, 0.0], lcar)
        p6 = geom.add_point([r * cos(+pi / 12.0), r * sin(+pi / 12.0), 0.0], lcar)
        p7 = geom.add_point([r * cos(-pi / 12.0), r * sin(-pi / 12.0), 0.0], lcar)
        p8 = geom.add_point([0.5 * r, 0.0, 0.0], lcar)

        c0 = geom.add_circle_arc(p6, p1, p4)
        c1 = geom.add_circle_arc(p4, p1, p3)
        c2 = geom.add_circle_arc(p3, p1, p5)
        c3 = geom.add_circle_arc(p5, p1, p7)
        l1 = geom.add_line(p7, p8)
        l2 = geom.add_line(p8, p6)
        ll = geom.add_curve_loop([c0, c1, c2, c3, l1, l2])

        pacman = geom.add_plane_surface(ll)

        # test setting physical groups
        geom.add_physical(p1, label="c")
        geom.add_physical(c0, label="arc")
        geom.add_physical(pacman, "dummy")
        geom.add_physical(pacman, label="77")

        mesh = geom.generate_mesh()

    ref = 54.312974717523744
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("pacman.vtu")
