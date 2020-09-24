from itertools import permutations

import meshio
from helpers import compute_volume

import pygmsh


def test(lcar=1.0):
    with pygmsh.built_in.Geometry() as geom:
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
        mesh = pygmsh.generate_mesh(geom, prune_vertices=False)

    ref = sum(l * w for l, w in permutations(lbw, 2))  # surface area
    # TODO compute hex volumes
    assert (
        abs(
            compute_volume(meshio.Mesh(mesh.points, {"quad": mesh.cells_dict["quad"]}))
            - ref
        )
        < 1.0e-2 * ref
    )
    return mesh


if __name__ == "__main__":
    meshio.write("hex.vtu", test())
