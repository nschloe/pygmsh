import pygmsh


def test():
    with pygmsh.occ.Geometry() as geom:
        geom.characteristic_length_min = 0.1
        geom.characteristic_length_max = 0.1

        ball = geom.add_ball([0.0, 0.0, 0.0], 1.0)
        box1 = geom.add_box([0, 0, 0], [1, 1, 1])
        box2 = geom.add_box([-2, -0.5, -0.5], [1.5, 0.8, 0.8])

        cut = geom.boolean_difference(ball, box1)
        frag = geom.boolean_fragments(cut, box2)

        # The three fragments are:
        # frag[0]: The ball with two cuts
        # frag[1]: The intersection of the stick and the ball
        # frag[2]: The stick without the ball
        geom.add_physical([frag[0], frag[1]], label="Sphere cut by box 1")
        geom.add_physical(frag[2], label="Box 2 cut by sphere")

        mesh = geom.generate_mesh(algorithm=6)

    assert "Sphere cut by box 1" in mesh.cell_sets
    assert "Box 2 cut by sphere" in mesh.cell_sets

    # mesh.remove_lower_dimensional_cells()
    # mesh.sets_to_int_data()
    return mesh


if __name__ == "__main__":
    test().write("ball-with-stick.vtu")
