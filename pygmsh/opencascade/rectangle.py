from .surface_base import SurfaceBase


class Rectangle(SurfaceBase):
    """
    Creates a rectangle.

    x0 : array-like[3]
         The 3 first expressions define the lower-left corner.
    a : float
        Rectangle width.
    b : float
        Rectangle height.
    corner_radius : float
        Defines a radius to round the rectangle corners.
    char_length : float
        Characteristic length of the mesh elements of this polygon.
    """

    def __init__(self, x0, a, b, corner_radius=None, char_length=None):
        super().__init__()

        assert len(x0) == 3

        self.x0 = x0
        self.a = a
        self.b = b
        self.corner_radius = corner_radius
        self.char_length = char_length

        args = list(x0) + [a, b]
        if corner_radius is not None:
            args.append(corner_radius)

        args = ", ".join([f"{arg}" for arg in args])

        self.code = "\n".join(
            [f"{self.id} = news;", f"Rectangle({self.id}) = {{{args}}};"]
            + self.char_length_code(char_length)
        )
        return
