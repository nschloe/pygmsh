import numpy as np
from helpers import compute_volume

import pygmsh


def test():
    X0 = np.array(
        [[+0.0, +0.0, 0.0], [+0.5, +0.3, 0.1], [-0.5, +0.3, 0.1], [+0.5, -0.3, 0.1]]
    )
    R = np.array([0.1, 0.2, 0.1, 0.14])

    with pygmsh.geo.Geometry() as geom:
        holes = [
            geom.add_ball(x0, r, with_volume=False, mesh_size=0.2 * r).surface_loop
            for x0, r in zip(X0, R)
        ]
        # geom.add_box(
        #         -1, 1,
        #         -1, 1,
        #         -1, 1,
        #         mesh_size=0.2,
        #         holes=holes
        #         )
        geom.add_ball([0, 0, 0], 1.0, mesh_size=0.2, holes=holes)
        # geom.add_physical_volume(ball, label="cheese")
        mesh = geom.generate_mesh(algorithm=5)

    ref = 4.07064892966291
    assert abs(compute_volume(mesh) - ref) < 2.0e-2 * ref
    return mesh


if __name__ == "__main__":
    test().write("swiss_cheese.vtu")
