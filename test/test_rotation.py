"""Test translation for all dimensions."""
import numpy as np

import pygmsh


def test_rotation2d():
    """Rotation of a surface object."""
    angle = np.pi / 5

    # Generate reference geometry
    geom = pygmsh.built_in.Geometry()
    rect = geom.add_rectangle(0.0, 2.0, 0.0, 1.0, 0.0, 0.1)
    mesh_unrot = pygmsh.generate_mesh(geom, geo_filename="test.geo")
    vertex_index = mesh_unrot.cells_dict["vertex"]
    vertex_index = vertex_index.reshape((vertex_index.shape[0],))

    # Generate rotated geometry
    geom = pygmsh.built_in.Geometry()
    rect = geom.add_rectangle(0.0, 2.0, 0.0, 1.0, 0.0, 0.1)
    geom.rotate(rect, [0, 0, 0], angle, [0, 0, 1])
    mesh = pygmsh.generate_mesh(geom, geo_filename="rot.geo")
    new_vertex_index = mesh.cells_dict["vertex"]
    new_vertex_index = new_vertex_index.reshape((new_vertex_index.shape[0],))

    # Generate rotation matrix and compare with rotated geometry
    Rm = pygmsh.helpers.rotation_matrix([0, 0, 1], angle)
    for v, v_new in zip(vertex_index, new_vertex_index):
        point = mesh_unrot.points[v, :]

        rot_point = np.dot(Rm, point)
        new_point = mesh.points[v, :]
        assert np.allclose(rot_point, new_point)

    return


if __name__ == "__main__":
    test_rotation2d()
