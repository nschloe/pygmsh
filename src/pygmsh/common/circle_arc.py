from .line_base import LineBase
from .point import Point

from ipdb import set_trace

class CircleArc(LineBase):
    """
    Creates a circle arc.

    Parameters
    ----------
    start : Coordinates of start point needed to construct circle-arc.
    center : Coordinates of center point needed to construct circle-arc.
    end : Coordinates of end point needed to construct circle-arc.
    nx : Plane normal in x dir
    ny : Plane normal in y dir
    nz : Plane normal in z dir
    """

    def __init__(
        self,
        env,
        start: Point,
        center: Point,
        end: Point,
        nx: float = 0.0,
        ny: float = 0.0,
        nz: float = 0.0,
    ):
        assert isinstance(start, Point)
        assert isinstance(center, Point)
        assert isinstance(end, Point)
        # print(f"nx:{nx}, ny:{ny}, nz:{nz}")
        # set_trace()
        # id0 = env.addCircleArc(start._id, center._id, end._id, nx=nx, ny=ny, nz=nz)
        id0 = env.addCircleArc(start._id, center._id, end._id)
        super().__init__(id0, [start, center, end])
