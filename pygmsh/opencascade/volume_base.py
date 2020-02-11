from .. import built_in


class VolumeBase(built_in.volume_base.VolumeBase):
    """
    Increments the Volume ID every time a new volume object
    is created. Inherits from built_in VolumeBase.
    """

    _ID = 0
    dimension = 3

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
            f"pts_{self.id}[] = PointsOf{{Volume{{{self.id}}};}};",
            f"Characteristic Length{{pts_{self.id}[]}} = {char_length};",
        ]
