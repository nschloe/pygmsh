class Dummy:
    def __init__(self, dim, id0):
        assert isinstance(id0, int)
        self.dimension = dim
        self.id = id0
        self._ID = id0
