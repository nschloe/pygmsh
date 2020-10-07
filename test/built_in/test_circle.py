from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.geo.Geometry() as geom:
        geom.add_circle(
            [0.0, 0.0, 0.0],
            1.0,
            mesh_size=0.1,
            num_sections=4,
            # If compound==False, the section borders have to be points of the
            # discretization. If using a compound circle, they don't; gmsh can
            # choose by itself where to point the circle points.
            compound=True,
        )
        # geom.add_physical(c.plane_surface, "super disk")
        mesh = geom.generate_mesh()

    ref = 3.1363871677682247
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("circle.vtk")
