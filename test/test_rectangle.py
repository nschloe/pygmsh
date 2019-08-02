import pygmsh
from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()

    geom.add_rectangle(0.0, 1.0, 0.0, 1.0, 0.0, 0.1)

    ref = 1.0
    mesh = pygmsh.generate_mesh(geom, mesh_file_type="vtk")
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("rectangle.vtu", test())
