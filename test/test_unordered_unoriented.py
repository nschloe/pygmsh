import numpy
import random

import pygmsh
from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()

    # Generate an approximation of a circle
    t = numpy.arange(0, 2.0 * numpy.pi, 0.05)
    x = numpy.vstack((numpy.cos(t), numpy.sin(t), numpy.zeros_like(t))).T
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
    ll = geom.add_line_loop(oriented_lines)
    geom.add_plane_surface(ll)

    mesh = pygmsh.generate_mesh(geom, prune_z_0=True)

    ref = numpy.pi
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("physical.vtu", test())
