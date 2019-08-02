class DefineConstant(object):
    def __init__(self, label, value, min_value, max_value, step=None, name=None):
        assert min_value <= value <= max_value

        self.label = label

        if name is None:
            name = "Parameters/{}".format(label)

        defined_constant = "{}, Min {}, Max {}".format(value, min_value, max_value)

        if step:
            defined_constant += ", Step {}".format(step)

        defined_constant += ', Name "{}"'.format(name)

        self.code = "DefineConstant[ {} = {{ {} }} ];".format(label, defined_constant)
        return

    # Need to overload repr so that the label will be formatted into gmsh code without any quotes
    def __repr__(self):
        return self.label
