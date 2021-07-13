"""Test translation for all dimensions."""
import numpy as np

import pygmsh


def test_rotation2d():
    """Rotation of a surface object."""
    angle = np.pi / 5

    # Generate reference geometry
    with pygmsh.geo.Geometry() as geom:
        rect = geom.add_rectangle(0.0, 2.0, 0.0, 1.0, 0.0, 0.1)
        mesh_unrot = geom.generate_mesh()
    vertex_index = mesh_unrot.cells_dict["vertex"]
    vertex_index = vertex_index.reshape((vertex_index.shape[0],))

    with pygmsh.geo.Geometry() as geom:
        # Generate rotated geometry
        geom = pygmsh.geo.Geometry()
        rect = geom.add_rectangle(0.0, 2.0, 0.0, 1.0, 0.0, 0.1)
        geom.rotate(rect.surface, (0, 0, 0), angle, (0, 0, 1))
        mesh = geom.generate_mesh()

    new_vertex_index = mesh.cells_dict["vertex"]
    new_vertex_index = new_vertex_index.reshape((new_vertex_index.shape[0],))

    # Generate rotation matrix and compare with rotated geometry
    Rm = pygmsh.helpers.rotation_matrix([0, 0, 1], angle)
    for v, v_new in zip(vertex_index, new_vertex_index):
        point = mesh_unrot.points[v, :]
        rot_point = np.dot(Rm, point)
        new_point = mesh.points[v, :]
        assert np.allclose(rot_point, new_point)


if __name__ == "__main__":
    test_rotation2d()
