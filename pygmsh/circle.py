# -*- coding: utf-8 -*-
#
from .circle_arc import CircleArc
from .compound_line import CompoundLine
from .line_loop import LineLoop
from .plane_surface import PlaneSurface
from .point import Point
import numpy


class Circle(object):
    def __init__(
            self,
            x0, radius, lcar,
            R=numpy.eye(3),
            compound=False,
            num_sections=3,
            holes=None,
            make_surface=True
            ):
        '''Add circle in the :math:`x`-:math:`y`-plane.
        '''
        if holes is None:
            holes = []
        else:
            assert make_surface

        self.x0 = x0
        self.radius = radius
        self.lcar = lcar
        self.R = R
        self.compound = compound
        self.num_sections = num_sections
        self.holes = holes

        # Define points that make the circle (midpoint and the four cardinal
        # directions).
        if num_sections == 4:
            # For accuracy, the points are provided explicitly.
            X = [
                [0.0,     0.0,     0.0],
                [radius,  0.0,     0.0],
                [0.0,     radius,  0.0],
                [-radius, 0.0,     0.0],
                [0.0,     -radius, 0.0]
                ]
        else:
            X = [
                [0.0, 0.0, 0.0]
                ]
            for k in range(num_sections):
                alpha = 2*numpy.pi * k / num_sections
                X.append([
                    radius*numpy.cos(alpha),
                    radius*numpy.sin(alpha),
                    0.0
                    ])

        code = []

        # Apply the transformation.
        # TODO assert that the transformation preserves circles
        X = [numpy.dot(R, x) + x0 for x in X]
        # Add Gmsh Points.
        p = [Point(x, lcar) for x in X]
        for point in p:
            code.append(point.code)

        # Define the circle arcs.
        arcs = [
            CircleArc([p[k], p[0], p[k+1]])
            for k in range(1, len(p)-1)
            ]
        arcs.append(CircleArc([p[-1], p[0], p[1]]))
        for a in arcs:
            code.append(a.code)

        if compound:
            arcs = [CompoundLine(arcs)]
            code.append(arcs[0].code)

        self.line_loop = LineLoop(arcs)
        code.append(self.line_loop.code)

        if make_surface:
            self.plane_surface = PlaneSurface(self.line_loop, holes)
            code.append(self.plane_surface.code)

        self.code = '\n'.join(code)

        return
