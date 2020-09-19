class PointBase:
    """
    Increments the Point ID every time a new object
    is created that inherits from PointBase.

    Parameters
    ----------
    id0 : str
        If no unique ID is given, the object global is incremented.
    """

    dimension = 0

    def __init__(self, id0):
        self._ID = id0
