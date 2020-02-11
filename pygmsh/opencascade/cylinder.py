from .volume_base import VolumeBase


class Cylinder(VolumeBase):
    """
    Creates a cylinder.

    Parameters
    ----------
    x0 : array-like[3]
        The 3 coordinates of the center of the first circular face.
    axis : array-like[3]
        The 3 components of the vector defining its axis.
    radius : float
        Radius value of the cylinder.
    angle : float
        Angular opening of the cylinder.
    char_length : float
        Characteristic length of the mesh elements of this polygon.
    """

    def __init__(self, x0, axis, radius, angle=None, char_length=None):
        super().__init__()

        assert len(x0) == 3
        assert len(axis) == 3

        self.x0 = x0
        self.axis = axis
        self.radius = radius
        self.angle = angle
        self.char_length = char_length

        args = list(x0) + list(axis) + [radius]
        if angle is not None:
            args.append(angle)
        args = ", ".join([f"{arg}" for arg in args])

        code = [
            f"{self.id} = newv;",
            f"Cylinder({self.id}) = {{{args}}};",
        ]

        if self.char_length:
            code.extend(
                [
                    f"pts_{self.id}[] = PointsOf{{Volume{{{self.id}}};}};",
                    "Characteristic Length{{pts_{}[]}} = {};".format(
                        self.id, char_length
                    ),
                ]
            )

        self.code = "\n".join(code)
        return
