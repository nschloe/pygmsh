from .volume_base import VolumeBase


class Ellipsoid(VolumeBase):
    """
    Creates an ellipsoid.

    Parameters
    ----------
    center: array-like[3]
        Center of the ball.
    radii: array-like[3]
        The radii of the ellipsoid along the semi-axes
    char_length: float
        If specified, sets the `Characteristic Length` property.
    """

    def __init__(self, center, radii, char_length=None):
        super(Ellipsoid, self).__init__()

        self.center = center
        self.radii = radii
        self.char_length = char_length

        def as_str(point):
            return ", ".join(str(x) for x in point)

        self.code = "\n".join(
            ["{} = newv;".format(self.id),
             "Sphere({}) = {{ {}, 1.0 }};".format(self.id, as_str(center)),
             "Dilate {{{{{}}}, {{{}}}}} {{ Volume{{{}}}; }}".format(as_str(center), as_str(radii), self.id),
             ]
            + self.char_length_code(char_length)
        )
        return
