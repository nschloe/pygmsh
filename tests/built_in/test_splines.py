from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.geo.Geometry() as geom:
        lcar = 0.1
        p1 = geom.add_point([0.0, 0.0, 0.0], lcar)
        p2 = geom.add_point([1.0, 0.0, 0.0], lcar)
        p3 = geom.add_point([1.0, 0.5, 0.0], lcar)
        p4 = geom.add_point([1.0, 1.0, 0.0], lcar)
        s1 = geom.add_spline([p1, p2, p3, p4])

        p2 = geom.add_point([0.0, 1.0, 0.0], lcar)
        p3 = geom.add_point([0.5, 1.0, 0.0], lcar)
        s2 = geom.add_spline([p4, p3, p2, p1])

        ll = geom.add_curve_loop([s1, s2])
        geom.add_plane_surface(ll)

        mesh = geom.generate_mesh()
    ref = 1.0809439490373247
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("splines.vtu")
