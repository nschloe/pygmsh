import pytest


def test_raise_duplicate():
    import pygmsh

    with pygmsh.geo.Geometry() as geom:
        p = geom.add_rectangle(-1, 1, -1, 1, z=0, mesh_size=1)
        geom.add_physical(p.lines[0], label="A")
        with pytest.raises(ValueError):
            geom.add_physical(p.lines[1], label="A")
