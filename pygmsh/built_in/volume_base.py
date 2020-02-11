class VolumeBase:
    """
    Increments the Line ID every time a new object
    is created that inherits from LineBase.

    Parameters
    ----------
    id0 : str
        If no unique ID is given, the object global is incremented.
    """

    _ID = 0
    dimension = 3

    def __init__(self, id0=None):
        if id0:
            self.id = id0
        else:
            self.id = f"vol{VolumeBase._ID}"
            VolumeBase._ID += 1
        return
