from .line_loop import LineLoop


class Surface:
    """
    Generates a Surface or Rules Surfaces.

    Parameters
    ----------
    line_loop : Object
        LineLoop object that contains all the Line objects for the
        loop construction.
    api_level : integer
        If larger than 2 a Surface will be constructed, otherwise
        a Ruled Surface will be constructed instead.

    Notes
    -----
    With the built-in kernel, the first line loop should be composed of
    either three or four elementary lines.

    With the built-in kernel, the optional In Sphere argument forces the
    surface to be a spherical patch (the extra parameter gives the
    identification number of the center of the sphere).
    """

    _ID = 0
    num_edges = 0
    dimension = 2

    def __init__(self, line_loop, api_level=2):
        assert isinstance(line_loop, LineLoop)

        self.line_loop = line_loop

        self.id = f"rs{Surface._ID}"
        Surface._ID += 1

        # `Ruled Surface` was deprecated in Gmsh 3 in favor of `Surface`.
        name = "Surface" if api_level > 2 else "Ruled Surface"

        self.code = "\n".join(
            [f"{self.id} = news;", f"{name}({self.id}) = {{{self.line_loop.id}}};"]
        )
        self.num_edges = len(line_loop)
        return
