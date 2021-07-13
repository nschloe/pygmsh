import numpy as np

import pygmsh


def test():
    with pygmsh.geo.Geometry() as geom:
        pts = [
            geom.add_point((0.0, 0.0, 0.0), mesh_size=1.0),
            geom.add_point((2.0, 0.0, 0.0), mesh_size=1.0),
            geom.add_point((0.0, 1.0, 0.0), mesh_size=1.0),
            geom.add_point((2.0, 1.0, 0.0), mesh_size=1.0),
        ]
        lines = [
            geom.add_line(pts[0], pts[1]),
            geom.add_line(pts[1], pts[3]),
            geom.add_line(pts[3], pts[2]),
            geom.add_line(pts[2], pts[0]),
        ]
        ll0 = geom.add_curve_loop(lines)
        rs0 = geom.add_surface(ll0)

        geom.set_transfinite_curve(lines[3], 3, "Progression", 1.0)
        geom.set_transfinite_curve(lines[1], 3, "Progression", 1.0)
        geom.set_transfinite_curve(lines[2], 3, "Progression", 1.0)
        geom.set_transfinite_curve(lines[0], 3, "Progression", 1.0)
        geom.set_transfinite_surface(rs0, "Left", pts)
        geom.set_recombined_surfaces([rs0])

        mesh = geom.generate_mesh()

    assert "quad" in mesh.cells_dict.keys()
    ref = np.array([[0, 4, 8, 7], [7, 8, 6, 2], [4, 1, 5, 8], [8, 5, 3, 6]])
    assert np.array_equal(ref, mesh.cells_dict["quad"])
    return mesh


if __name__ == "__main__":
    test().write("rectangle_structured.vtu")
