class Dummy:
    def __init__(self, dim, id0):
        assert isinstance(id0, int)
        self.dim = dim
        self._id = id0
        self.dim_tag = (dim, id0)
        self.dim_tags = [self.dim_tag]

    def __repr__(self):
        return f"<pygmsh Dummy object, ID {self._id}>"
