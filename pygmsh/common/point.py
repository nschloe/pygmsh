class Point:
    """
    Creates an elementary point.

    x : array-like[3]
        Give the three X, Y and Z coordinates of the
        point in the three-dimensional Euclidean space.
    mesh_size : float
        The prescribed mesh element size at this point.
    """

    dim = 0

    def __init__(self, env, x, mesh_size=None):
        if len(x) == 2:
            x = [x[0], x[1], 0.0]

        assert len(x) == 3
        self.x = x
        args = list(x)
        if mesh_size is not None:
            args.append(mesh_size)
        self._id = env.addPoint(*args)
        self.dim_tag = (0, self._id)
        self.dim_tags = [self.dim_tag]

    def __repr__(self):
        X = ", ".join(str(x) for x in self.x)
        return f"<pygmsh Point object, ID {self._id}, x = [{X}]>"
