# -*- coding: utf-8 -*-
#
from pygmsh.geometry import Geometry
from pygmsh.helper import *

from .bspline import Bspline
from .circle import Circle
from .circle_arc import CircleArc
from .compound_line import CompoundLine
from .ellipse_arc import EllipseArc
from .line import Line
from .line_loop import LineLoop
from .plane_surface import PlaneSurface
from .point import Point

from pygmsh.__about__ import (
        __version__,
        __author__,
        __author_email__,
        __website__,
        )

import pipdated
if pipdated.needs_checking('pygmsh'):
    msg = pipdated.check('pygmsh', __version__)
    if msg:
        print(msg)

__all__ = [
        'geometry',
        'helper'
        ]
