import numpy as np

import pygmsh


def test():
    # Characteristic length
    lcar = 1e-1

    # Coordinates of lower-left and upper-right vertices of a square domain
    xmin = 0.0
    xmax = 5.0
    ymin = 0.0
    ymax = 5.0

    # Vertices of a square hole
    squareHoleCoordinates = np.array([[1.0, 1.0], [4.0, 1.0], [4.0, 4.0], [1.0, 4.0]])

    with pygmsh.geo.Geometry() as geom:
        # Create square hole
        squareHole = geom.add_polygon(squareHoleCoordinates, lcar, make_surface=False)
        # Create square domain with square hole
        geom.add_rectangle(
            xmin, xmax, ymin, ymax, 0.0, lcar, holes=[squareHole.curve_loop]
        )
        mesh = geom.generate_mesh(order=2)

    assert "triangle6" in mesh.cells_dict

    # TODO support for volumes of triangle6
    # ref = 16.0
    # from helpers import compute_volume
    # assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("hole_in_square.vtu")
