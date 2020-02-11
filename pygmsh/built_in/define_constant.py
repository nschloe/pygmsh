class DefineConstant:
    def __init__(self, label, value, min_value, max_value, step=None, name=None):
        assert min_value <= value <= max_value

        self.label = label

        if name is None:
            name = f"Parameters/{label}"

        defined_constant = f"{value}, Min {min_value}, Max {max_value}"

        if step:
            defined_constant += f", Step {step}"

        defined_constant += f', Name "{name}"'

        self.code = f"DefineConstant[ {label} = {{ {defined_constant} }} ];"
        return

    # Need to overload repr so that the label will be formatted into gmsh code without any quotes
    def __repr__(self):
        return self.label
