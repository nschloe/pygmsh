import pygmsh


def test():
    with pygmsh.occ.Geometry() as geom:
        geom.add_ball([0.0, 0.0, 0.0], 1.0, mesh_size=0.1)
        mesh = geom.generate_mesh()

    pygmsh.optimize(mesh)
