import random

import numpy as np
from helpers import compute_volume

import pygmsh


def test():
    with pygmsh.geo.Geometry() as geom:
        # Generate an approximation of a circle
        t = np.arange(0, 2.0 * np.pi, 0.05)
        x = np.column_stack([np.cos(t), np.sin(t), np.zeros_like(t)])
        points = [geom.add_point(p) for p in x]

        # Shuffle the orientation of lines by point order
        o = [0 if k % 3 == 0 else 1 for k in range(len(points))]

        lines = [
            geom.add_line(points[k + o[k]], points[k + (o[k] + 1) % 2])
            for k in range(len(points) - 1)
        ]
        lines.append(geom.add_line(points[-1], points[0]))

        # Shuffle the order of lines
        random.seed(1)
        random.shuffle(lines)

        oriented_lines = pygmsh.orient_lines(lines)
        ll = geom.add_curve_loop(oriented_lines)
        geom.add_plane_surface(ll)

        mesh = geom.generate_mesh()

    ref = np.pi
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("physical.vtu")
