class LineLoop:
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
    A line loop must be a closed loop, and the elementary lines
    should be ordered and oriented (negating to specify reverse orientation).
    If the orientation is correct, but the ordering is wrong, Gmsh will
    actually reorder the list internally to create a consistent loop.
    """

    _ID = 0
    dimension = 1

    def __init__(self, lines):
        self.lines = lines

        self.id = f"ll{LineLoop._ID}"
        LineLoop._ID += 1

        self.code = "\n".join(
            [
                f"{self.id} = newll;",
                "Line Loop({}) = {{{}}};".format(
                    self.id, ", ".join([l.id for l in lines])
                ),
            ]
        )
        return

    def __len__(self):
        return len(self.lines)
