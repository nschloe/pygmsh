import pygmsh


def test(lcar=0.5):
    geom = pygmsh.built_in.Geometry()
    poly = geom.add_polygon(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]], lcar
    )

    top, volume, lat = geom.extrude(poly.surface, [0, 0, 2])

    geom.add_physical(poly.surface, label="bottom")
    geom.add_physical(top, label="top")
    geom.add_physical(volume, label="volume")
    geom.add_physical(lat, label="lat")
    geom.add_physical(poly.lines[0], label="line")

    mesh = pygmsh.generate_mesh(geom, geo_filename="physical.geo")
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("physical.vtu", test())
