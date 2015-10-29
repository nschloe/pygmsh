#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a mesh for a ball.
'''
import pygmsh as pg

def generate():
    geom = pg.Geometry()

    geom.add_ball([0.0, 0.0, 0.0], 1.0, 0.05)

    return geom.get_code()


if __name__ == '__main__':
    print(generate())
