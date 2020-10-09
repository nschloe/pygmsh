from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.geo.Geometry() as geom:
        lcar = 0.1
        p1 = geom.add_point([0.0, 0.0, 0.0], lcar)
        p2 = geom.add_point([1.0, 0.0, 0.0], lcar)
        p3 = geom.add_point([1.0, 0.5, 0.0], lcar)
        p4 = geom.add_point([1.0, 1.0, 0.0], lcar)
        s1 = geom.add_bspline([p1, p2, p3, p4])

        p2 = geom.add_point([0.0, 1.0, 0.0], lcar)
        p3 = geom.add_point([0.5, 1.0, 0.0], lcar)
        s2 = geom.add_bspline([p4, p3, p2, p1])

        ll = geom.add_curve_loop([s1, s2])
        pl = geom.add_plane_surface(ll)

        # test some __repr__
        print(p1)
        print(ll)
        print(s1)
        print(pl)

        mesh = geom.generate_mesh(verbose=True)
    # ref = 0.9156598733673261
    ref = 0.7474554072002251
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("bsplines.vtu")
