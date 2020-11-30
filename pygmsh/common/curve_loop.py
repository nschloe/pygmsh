class CurveLoop:
    """
    Increments the Line ID every time a new object is created that inherits
    from LineBase.

    Parameters
    ----------
    id0 : str
        If no unique ID is given, the object global is incremented.
    lines : list
        Containing the lines defining the shape.

    Notes
    -----
    A line loop must be a closed loop, and the elementary lines should be ordered and
    oriented (negating to specify reverse orientation). If the orientation is correct,
    but the ordering is wrong, Gmsh will actually reorder the list internally to create
    a consistent loop.
    """

    dim = 1

    def __init__(self, env, curves):
        for k in range(len(curves) - 1):
            assert curves[k].points[-1] == curves[k + 1].points[0]
        assert curves[-1].points[-1] == curves[0].points[0]
        self._id = env.addCurveLoop([c._id for c in curves])
        self.dim_tag = (1, self._id)
        self.dim_tags = [self.dim_tag]
        self.curves = curves

    def __len__(self):
        return len(self.curves)

    def __repr__(self):
        curves = ", ".join([str(l._id) for l in self.curves])
        return f"<pygmsh CurveLoop object, ID {self._id}, curves ({curves})>"
