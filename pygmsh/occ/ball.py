from math import pi

import gmsh


class Ball:
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

    dim = 3

    def __init__(self, center, radius, angle1=-pi / 2, angle2=pi / 2, angle3=2 * pi):
        self.center = center
        self.radius = radius
        self._id = gmsh.model.occ.addSphere(
            *center, radius, angle1=angle1, angle2=angle2, angle3=angle3
        )
        self.dim_tag = (3, self._id)
        self.dim_tags = [self.dim_tag]

    def __repr__(self):
        return f"<pygmsh Ball object (OCC), ID {self._id}>"
