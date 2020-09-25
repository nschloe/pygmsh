class VolumeBase:
    """
    Increments the Line ID every time a new object
    is created that inherits from LineBase.

    Parameters
    ----------
    id0 : str
        If no unique ID is given, the object global is incremented.
    """

    dimension = 3

    def __init__(self, id0):
        self._ID = id0
