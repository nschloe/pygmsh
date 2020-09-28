class Dummy:
    def __init__(self, dim, id0):
        assert isinstance(id0, int)
        self.dim = dim
        self.id = id0
        self._ID = id0
        self.dim_tags = [(dim, id0)]

    def __repr__(self):
        return f"<pygmsh Dummy object, ID {self._ID}>"
