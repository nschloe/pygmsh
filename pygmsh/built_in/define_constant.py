# -*- coding: utf-8 -*-
#


class DefineConstant(object):
    def __init__(self, label, value, min_value, max_value, step=None, name=None):
        assert min_value <= value <= max_value

        self.label = label

        if name is None:
            name = "Parameters/{}".format(label)

        step = "" if step is None else "Step {}".format(step)

        self.code = 'DefineConstant[ {} = {{ {}, Min {}, Max {}, {}, Name "{}" }} ];'.format(
            label, value, min_value, max_value, step, name
        )
        return

    # Need to overload repr so that the label will be formatted into gmsh code without and quotes
    def __repr__(self):
        return self.label
