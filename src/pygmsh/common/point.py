from __future__ import annotations


class Point:
    """
    Creates an elementary point.

    Parameters
    ----------
    x : Give the coordinates X, Y (and Z) of the point in the three-dimensional
        Euclidean space.
    mesh_size : The prescribed mesh element size at this point.


    Attributes
    ----------
    x : array-like
        Point coordinates.
    """

    dim = 0

    def __init__(
        self,
        env,
        x: tuple[float, float] | tuple[float, float, float],
        mesh_size: float | None = None,
    ):
        if len(x) == 2:
            x = (x[0], x[1], 0.0)

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
