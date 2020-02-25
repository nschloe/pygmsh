import copy


class LineBase:
    """
    Increments the Line ID every time a new object
    is created that inherits from LineBase.

    Parameters
    ----------
    id0 : str
        If no unique ID is given, the object global is incremented.
    """

    _ID = 0
    dimension = 1

    def __init__(self, id0=None):
        if id0:
            self.id = id0
        else:
            self.id = f"l{LineBase._ID}"
            LineBase._ID += 1
        return

    def __neg__(self):
        neg_self = copy.deepcopy(self)
        neg_self.id = "-" + neg_self.id
        return neg_self
