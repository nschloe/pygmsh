# -*- coding: utf-8 -*-
#
from .volume_base import VolumeBase


class Ball(VolumeBase):
    def __init__(
            self, center, radius, x0=None, x1=None, alpha=None,
            char_length=None
            ):
        '''Generate a solid ball.

        Parameters
        ----------
        center: list of 3 floats
           Center of the ball.

        radius: float
           Radius of the ball.

        x0: float (optional)
           If specified and `x0 > -1`, the ball is cut off at `x0*radius`
           parallel to the y-z plane.

        x1: float (optional)
           If specified and `x1 < +1`, the ball is cut off at `x1*radius`
           parallel to the y-z plane.

        alpha: float (optional)
           If specified and `alpha < 2*pi`, the points between `alpha` and
           `2*pi` w.r.t. to the x-y plane are not part of the object.

        char_length: float (optional)
           If specified, sets the `Characteristic Length` property.
        '''
        super(Ball, self).__init__()

        self.center = center
        self.radius = radius
        self.char_length = char_length

        args = [center[0], center[1], center[2], radius]
        if x0 is not None:
            args.append(x0)
            if x1 is not None:
                args.append(x1)
                if alpha is not None:
                    args.append(alpha)
        args = ', '.join(['{}'.format(arg) for arg in args])

        code = [
            '{} = newv;'.format(self.id),
            'Sphere({}) = {{{}}};'.format(self.id, args)
            ]

        if self.char_length:
            code.extend([
                'pts_{}[] = PointsOf{{Volume{{{}}};}};'.format(
                    self.id, self.id
                    ),
                'Characteristic Length{{pts_{}[]}} = {};'.format(
                    self.id, char_length
                    ),
                ])

        self.code = '\n'.join(code)
        return
