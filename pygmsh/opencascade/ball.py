from .volume_base import VolumeBase


class Ball(VolumeBase):
    """
    Creates a sphere.

    Parameters
    ----------
    center: array-like[3]
        Center of the ball.
    radius: float
        Radius of the ball.
    x0: float
        If specified and `x0 > -1`, the ball is cut off at `x0*radius`
        parallel to the y-z plane.
    x1: float
        If specified and `x1 < +1`, the ball is cut off at `x1*radius`
        parallel to the y-z plane.
    alpha: float
        If specified and `alpha < 2*pi`, the points between `alpha` and
        `2*pi` w.r.t. to the x-y plane are not part of the object.
    char_length: float
        If specified, sets the `Characteristic Length` property.
    """

    def __init__(self, center, radius, x0=None, x1=None, alpha=None, char_length=None):
        super().__init__()

        self.center = center
        self.radius = radius
        self.char_length = char_length

        args = list(center) + [radius]
        if x0 is not None:
            args.append(x0)
            if x1 is not None:
                args.append(x1)
                if alpha is not None:
                    args.append(alpha)
        args = ", ".join([f"{arg}" for arg in args])

        self.code = "\n".join(
            [f"{self.id} = newv;", f"Sphere({self.id}) = {{{args}}};"]
            + self.char_length_code(char_length)
        )
        return
