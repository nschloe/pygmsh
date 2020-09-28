import copy


class LineBase:
    """
    Parameters
    ----------
    id0 : int
    points: list of int
    """

    dim = 1

    def __init__(self, id0, points):
        self._ID = id0
        self.points = points

    def __neg__(self):
        neg_self = copy.deepcopy(self)
        neg_self._ID = -self._ID
        neg_self.points = self.points[::-1]
        return neg_self
