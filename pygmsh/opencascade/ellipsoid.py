from .ball import Ball


class Ellipsoid(Ball):
    """
    Creates an ellipsoid.

    Parameters
    ----------
    center: array-like[3]
        Center of the ellipsoid.
    radii: array-like[3]
        The radii of the ellipsoid along the semi-axes
    x0: float
        If specified and `x0 > -1`, the ellipsoid is cut off at `x0*radius`
        parallel to the y-z plane.
    x1: float
        If specified and `x1 < +1`, the ellipsoid is cut off at `x1*radius`
        parallel to the y-z plane.
    alpha: float
        If specified and `alpha < 2*pi`, the points between `alpha` and
        `2*pi` w.r.t. to the x-y plane are not part of the object.
    char_length: float
        If specified, sets the `Characteristic Length` property.
    """

    def __init__(self, center, radii, char_length=None, **kwargs):
        self.center = center
        self.radii = radii
        self.char_length = char_length

        # Instantiate the ball and later stretch it
        Ball.__init__(self, center, 1.0, char_length=None, **kwargs)

        def as_str(point):
            return ", ".join(str(x) for x in point)

        self.code = "\n".join(
            [
                self.code,
                "Dilate {{{{{}}}, {{{}}}}} {{ Volume{{{}}}; }}".format(
                    as_str(center), as_str(radii), self.id
                ),
            ]
            + self.char_length_code(char_length)
        )
        return
