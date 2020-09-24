import pygmsh


def test(lcar=1.0):
    with pygmsh.built_in.Geometry() as geom:
        poly = geom.add_polygon(
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]], lcar
        )
        geom.set_transfinite_surface(poly.surface, "Left", corner_tags=[])
        mesh = pygmsh.generate_mesh(geom)
    # assert len(mesh.cells_dict["triangle"]) == 10 * 8 * 2
    return mesh


if __name__ == "__main__":
    test().write("transfinite.vtu")
