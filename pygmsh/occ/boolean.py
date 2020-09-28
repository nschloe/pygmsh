class Boolean:
    def __init__(self, dim_tags, boolean_type):
        self.dim = dim_tags[0][0]
        assert all(self.dim == dt[0] for dt in dim_tags)
        self.dim_tags = dim_tags
        self.boolean_type = boolean_type

    def __repr__(self):
        return f"<pygmsh Boolean {self.boolean_type} object, dim={self.dim}>"
