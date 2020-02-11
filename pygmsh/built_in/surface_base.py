class SurfaceBase:
    """
    Increments the Line ID every time a new object is created that inherits
    from LineBase.

    Parameters
    ----------
    id0 : str
        If no unique ID is given, the object global is incremented.
    """

    _ID = 0
    num_edges = 0
    dimension = 2

    def __init__(self, id0=None, num_edges=0):
        if id0:
            assert isinstance(id0, str)
            self.id = id0
        else:
            self.id = f"s{SurfaceBase._ID}"
            SurfaceBase._ID += 1
        self.num_edges = num_edges
        return
