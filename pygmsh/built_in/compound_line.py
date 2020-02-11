from .line_base import LineBase


class CompoundLine(LineBase):
    """
    Creates a compound line from several elementary lines.
    When meshed, a compound line will be reparametrized as
    a single line, whose mesh can thus cross internal boundaries.

    Parameters
    ----------
    lines : array-like[N]
        Contains the identification number of the elementary lines
        that should be reparametrized as a single line.
    """

    def __init__(self, lines):
        super().__init__()

        self.lines = lines

        self.code = "\n".join(
            [
                f"{self.id} = newl;",
                "Compound Line({}) = {{{}}};".format(
                    self.id, ",".join([l.id for l in self.lines])
                ),
            ]
        )
        return
