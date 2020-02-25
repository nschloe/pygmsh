import numpy as np

import pygmsh


def test():
    geom = pygmsh.built_in.Geometry()
    p0 = geom.add_point((0.0, 0.0, 0.0), lcar=1.0)
    p1 = geom.add_point((2.0, 0.0, 0.0), lcar=1.0)
    p2 = geom.add_point((0.0, 1.0, 0.0), lcar=1.0)
    p3 = geom.add_point((2.0, 1.0, 0.0), lcar=1.0)
    l0 = geom.add_line(p0, p1)
    l1 = geom.add_line(p1, p3)
    l2 = geom.add_line(p3, p2)
    l3 = geom.add_line(p2, p0)
    ll0 = geom.add_line_loop((l0, l1, l2, l3))
    rs0 = geom.add_surface(ll0)
    geom.set_transfinite_lines([l3, l1], 3, progression=1)
    geom.set_transfinite_lines([l2, l0], 3, progression=1)
    geom.set_transfinite_surface(rs0)
    geom.set_recombined_surfaces([rs0])

    mesh = pygmsh.generate_mesh(geom)

    assert "quad" in mesh.cells_dict.keys()
    ref = np.array([[0, 4, 8, 7], [7, 8, 6, 2], [4, 1, 5, 8], [8, 5, 3, 6]])
    assert np.array_equal(ref, mesh.cells_dict["quad"])

    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("rectangle_structured.vtk", test())
