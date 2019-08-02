"""Creates a mesh on a cube.
"""
import pygmsh
from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()
    geom.add_box(0, 1, 0, 1, 0, 1, 1.0)

    ref = 1.0
    mesh = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("cube.vtu", test())
