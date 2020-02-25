class PointBase:
    """
    Increments the Point ID every time a new object
    is created that inherits from PointBase.

    Parameters
    ----------
    id0 : str
        If no unique ID is given, the object global is incremented.
    """

    _ID = 0
    dimension = 0

    def __init__(self, id0=None):
        if id0:
            self.id = id0
        else:
            self.id = f"p{PointBase._ID}"
            PointBase._ID += 1
        return
