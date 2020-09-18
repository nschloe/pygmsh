class SurfaceBase:
    """
    Increments the Line ID every time a new object is created that inherits
    from LineBase.

    Parameters
    ----------
    id0 : int
    """

    num_edges = 0
    dimension = 2

    def __init__(self, id0, num_edges=0):
        self._ID = id0
        self.num_edges = num_edges
