class SurfaceLoop:
    """
    Creates a surface loop (a shell).
    Increments the Line ID every time a new object is created that inherits
    from LineBase.

    Parameters
    ----------
    id0 : str
        The surface loop’s identification number.
        If `None` then the object's global ID is incremented.
    surfaces : list
        Contain the identification numbers of all the elementary
        surfaces that constitute the surface loop.

    Notes
    -----
    A surface loop must always represent a closed shell, and the
    elementary surfaces should be oriented consistently (using
    negative identification numbers to specify reverse orientation).
    """

    _ID = 0
    dimension = 2

    def __init__(self, surfaces):
        self.surfaces = surfaces

        self.id = f"sl{SurfaceLoop._ID}"
        SurfaceLoop._ID += 1

        self.code = "\n".join(
            [
                f"{self.id} = news;",
                "Surface Loop({}) = {{{}}};".format(
                    self.id, ",".join([s.id for s in surfaces])
                ),
            ]
        )
        return
