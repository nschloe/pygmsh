'''
This module provides a Python interface for the Gmsh scripting language.  It
aims at working around some of Gmsh's inconveniences (e.g., having to manually
assign an ID for every entity created) and providing access to Python's
features.
'''
# -----------------------------------------------------------------------------
import numpy as np
# -----------------------------------------------------------------------------
# In Gmsh, the user must manually provide a unique ID for every point, curce,
# volume created. This can get messy when a lot of entities are created and it
# isn't clear which IDs are already in use. Some Gmsh commands even create new
# entities and silently reserve IDs in that way. This module tries to work
# around this by providing routines in the style of add_point(x) which
# *returns* the ID. To make variable names in Gmsh unique, keep track of how
# many points, cirlces, etc. have already been created. Variable names will
# then be p1, p2, etc. for points, c1, c2, etc. for circles and so on.
POINT_ID = 0
LINE_ID = 0
LINELOOP_ID = 0
SURFACE_ID = 0
SURFACELOOP_ID = 0
VOLUME_ID = 0
CIRCLE_ID = 0
REG_ID = 0
OTHER_ID = 0
EXTRUDE_ID = 0

GMSH_CODE = []
# -----------------------------------------------------------------------------
def Point(x, lcar):
    '''Add point.
    '''
    global POINT_ID
    POINT_ID += 1
    name = 'p%d' % POINT_ID
    GMSH_CODE.append('%s = newp;' % name)
    GMSH_CODE.append('Point(%s) = {%g, %g, %g, %g};'
                    % (name, x[0], x[1], x[2], lcar)
                    )
    return name
# -----------------------------------------------------------------------------
def Line(p0, p1):
    '''Add line.
    '''
    global LINE_ID
    LINE_ID += 1
    name = 'l%d' % LINE_ID
    GMSH_CODE.append('%s = newreg;' % name)
    GMSH_CODE.append('Line(%s) = {%s, %s};' % (name, p0, p1))
    return name
# -----------------------------------------------------------------------------
def Circle(point_ids):
    '''Add Circle.
    '''
    global CIRCLE_ID
    CIRCLE_ID += 1
    name = 'c%d' % CIRCLE_ID
    GMSH_CODE.append('%s = newreg;' % name)
    GMSH_CODE.append('Circle(%s) = {%s, %s, %s};'
                    % (name, point_ids[0], point_ids[1], point_ids[2])
                    )
    return name
# -----------------------------------------------------------------------------
def LineLoop(lines):
    '''Gmsh Line Loops.
    '''
    global LINELOOP_ID
    LINELOOP_ID += 1
    name = 'll%d' % LINELOOP_ID
    GMSH_CODE.append('%s = newreg;' % name)
    GMSH_CODE.append('Line Loop(%s) = {%s};' % (name, ','.join(lines)))
    return name
# -----------------------------------------------------------------------------
def PlaneSurface(line_loop):
    '''Create Gmsh Surface.
    '''
    global SURFACE_ID
    SURFACE_ID += 1
    sname = 'surf%d' % SURFACE_ID
    GMSH_CODE.append('%s = newreg;' % sname)
    GMSH_CODE.append('Plane Surface(%s) = {%s};' % (sname, line_loop))

    return sname
# -----------------------------------------------------------------------------
def RuledSurface(line_loop):
    '''Create Gmsh Surface.
    '''
    global SURFACE_ID
    SURFACE_ID += 1
    sname = 'surf%d' % SURFACE_ID
    GMSH_CODE.append('%s = newreg;' % sname)
    GMSH_CODE.append('Ruled Surface(%s) = {%s};' % (sname, line_loop))

    return sname
# -----------------------------------------------------------------------------
def SurfaceLoop(surfaces):
    '''Gmsh Surface Loop.
    '''
    global SURFACELOOP_ID
    SURFACELOOP_ID += 1
    name = 'surfloop%d' % SURFACELOOP_ID
    GMSH_CODE.append('%s = newreg;' % name)
    GMSH_CODE.append('Surface Loop(%s) = {%s};' % (name, ','.join(surfaces)))

    return name
# -----------------------------------------------------------------------------
def Volume(surface_loop):
    '''Gmsh Volume.
    '''
    global VOLUME_ID
    VOLUME_ID += 1
    name = 'vol%d' % VOLUME_ID
    GMSH_CODE.append('%s = newreg;' % name)
    GMSH_CODE.append('Volume(%s) = %s;' % (name, surface_loop))

    return name
# -----------------------------------------------------------------------------
def PhysicalVolume(volume, label):
    '''Gmsh Physical Volume.
    '''
    GMSH_CODE.append('Physical Volume("%s") = %s;' % (label, volume))
    return
# -----------------------------------------------------------------------------
def Extrude(entity, axis, point_on_axis, angle):
    '''Extrusion (rotation) of any entity around an axis by a given angle.
    '''
    global EXTRUDE_ID
    EXTRUDE_ID += 1

    #  ex4[] = Extrude {{0,0,1}, {0,0,0}, 2*Pi/3}{Line{tc4};};
    name = 'ex%d' % EXTRUDE_ID
    GMSH_CODE.append('%s[] = Extrude{{%s,%s,%s}, {%s,%s,%s}, %s}{%s;};'
                    % ((name,) + tuple(axis) + tuple(point_on_axis)
                      + (angle, entity)))

    return name
# -----------------------------------------------------------------------------
