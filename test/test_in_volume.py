from helpers import compute_volume

import pygmsh


def test():
    geom = pygmsh.built_in.Geometry()

    box = geom.add_box(-1, 2, -1, 2, -1, 1, lcar=0.5)
    poly = geom.add_polygon(
        [
            [0, 0.3, 0],
            [0, 1.1, 0],
            [0.9, 1.1, 0],
            [0.9, 0.3, 0],
            [0.6, 0.7, 0],
            [0.3, 0.7, 0],
            [0.2, 0.4, 0],
        ],
        lcar=[0.2, 0.2, 0.2, 0.2, 0.03, 0.03, 0.01],
    )
    geom.in_volume(poly.lines[4], box.volume)
    geom.in_volume(poly.points[6], box.volume)
    geom.in_volume(poly.surface, box.volume)

    ref = 18.0
    mesh = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("test.vtk", test())
