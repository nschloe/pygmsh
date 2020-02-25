from .. import built_in


class SurfaceBase(built_in.surface_base.SurfaceBase):
    """
    Increments the Surface ID every time a new surface object
    is created. Inherits from built_in SurfaceBase.
    """

    _ID = 0
    dimension = 2

    def __init__(self, is_list=False, id0=None):
        super().__init__(id0=id0)

        self.is_list = is_list
        if is_list:
            self.id += "[]"
        return

    def char_length_code(self, char_length):
        if char_length is None:
            return []

        return [
            f"pts_{self.id}[] = PointsOf{{Surface{{{self.id}}};}};",
            f"Characteristic Length{{pts_{self.id}[]}} = {char_length};",
        ]
