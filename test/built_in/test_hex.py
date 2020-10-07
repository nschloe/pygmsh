from itertools import permutations

import meshio
from helpers import compute_volume

import pygmsh


def test(lcar=1.0):
    with pygmsh.geo.Geometry() as geom:
        lbw = [2, 3, 5]
        points = [geom.add_point([x, 0.0, 0.0], lcar) for x in [0.0, lbw[0]]]
        line = geom.add_line(*points)

        _, rectangle, _ = geom.extrude(
            line, translation_axis=[0.0, lbw[1], 0.0], num_layers=lbw[1], recombine=True
        )
        geom.extrude(
            rectangle,
            translation_axis=[0.0, 0.0, lbw[2]],
            num_layers=lbw[2],
            recombine=True,
        )
        # compute_volume only supports 3D for tetras, but does return surface area for
        # quads
        mesh = geom.generate_mesh()
        # mesh.remove_lower_dimensional_cells()
        # mesh.remove_orphaned_nodes()

    ref = sum(l * w for l, w in permutations(lbw, 2))  # surface area
    # TODO compute hex volumes
    quad_mesh = meshio.Mesh(mesh.points, {"quad": mesh.cells_dict["quad"]})
    assert abs(compute_volume(quad_mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    meshio.write("hex.vtu", test())
