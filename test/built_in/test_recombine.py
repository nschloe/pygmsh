import numpy as np
import pytest

import pygmsh


@pytest.mark.skip()
def test():
    geom = pygmsh.built_in.Geometry()
    p = [
        geom.add_point((0.0, 0.0, 0.0), lcar=1.0),
        geom.add_point((2.0, 0.0, 0.0), lcar=1.0),
        geom.add_point((0.0, 1.0, 0.0), lcar=1.0),
        geom.add_point((2.0, 1.0, 0.0), lcar=1.0),
    ]
    l = [
        geom.add_line(p[0], p[1]),
        geom.add_line(p[1], p[3]),
        geom.add_line(p[3], p[2]),
        geom.add_line(p[2], p[0]),
    ]
    ll0 = geom.add_curve_loop(l)
    rs0 = geom.add_surface(ll0)

    geom.set_transfinite_curve(l[3], 3, "Progression", 1.0)
    geom.set_transfinite_curve(l[1], 3, "Progression", 1.0)
    geom.set_transfinite_curve(l[2], 3, "Progression", 1.0)
    geom.set_transfinite_curve(l[0], 3, "Progression", 1.0)
    geom.set_recombined_surfaces([rs0])

    mesh = pygmsh.generate_mesh(geom)

    print(mesh)
    mesh.write("out.vtu")

    assert "quad" in mesh.cells_dict.keys()
    ref = np.array([[0, 4, 8, 7], [7, 8, 6, 2], [4, 1, 5, 8], [8, 5, 3, 6]])
    assert np.array_equal(ref, mesh.cells_dict["quad"])

    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("rectangle_structured.vtk", test())
