#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a mesh for a ball.
'''
import pygmsh as pg

def generate():

    ball = pg.add_ball([0.0, 0.0, 0.0], 1.0, 0.05)

    return pg.get_code()


if __name__ == "__main__":
    print(generate())
