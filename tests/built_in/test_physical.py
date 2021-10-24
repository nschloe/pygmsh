import meshio

import pygmsh


def test(lcar=0.5):
    with pygmsh.geo.Geometry() as geom:
        poly = geom.add_polygon([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]], lcar)

        top, volume, lat = geom.extrude(poly, [0, 0, 2])

        geom.add_physical(poly, label="bottom")
        geom.add_physical(top, label="top")
        geom.add_physical(volume, label="volume")
        geom.add_physical(lat, label="lat")
        geom.add_physical(poly.lines[0], label="line")

        mesh = geom.generate_mesh()
        assert len(mesh.cell_sets) == 5
    return mesh


if __name__ == "__main__":
    test().write("physical.vtu")
    read_mesh = meshio.read("physical.vtu")
    assert len(read_mesh.cell_sets) == 5
