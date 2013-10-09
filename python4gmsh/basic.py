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
_POINT_ID = 0
_LINE_ID = 0
_LINELOOP_ID = 0
_SURFACE_ID = 0
_SURFACELOOP_ID = 0
_VOLUME_ID = 0
_CIRCLE_ID = 0
_EXTRUDE_ID = 0
_ARRAY_ID = 0

_GMSH_CODE = []
# -----------------------------------------------------------------------------
def get_code():
    '''Returns properly formatted Gmsh code.
    '''
    return '\n'.join(_GMSH_CODE)
# -----------------------------------------------------------------------------
def Point(x, lcar):
    '''Add point.
    '''
    global _POINT_ID
    _POINT_ID += 1
    name = 'p%d' % _POINT_ID
    _GMSH_CODE.append('%s = newp;' % name)
    _GMSH_CODE.append('Point(%s) = {%g, %g, %g, %g};'
                    % (name, x[0], x[1], x[2], lcar)
                    )
    return name
# -----------------------------------------------------------------------------
def Line(p0, p1):
    '''Add line.
    '''
    global _LINE_ID
    _LINE_ID += 1
    name = 'l%d' % _LINE_ID
    _GMSH_CODE.append('%s = newreg;' % name)
    _GMSH_CODE.append('Line(%s) = {%s, %s};' % (name, p0, p1))
    return name
# -----------------------------------------------------------------------------
def Circle(point_ids):
    '''Add Circle.
    '''
    global _CIRCLE_ID
    _CIRCLE_ID += 1
    name = 'c%d' % _CIRCLE_ID
    _GMSH_CODE.append('%s = newreg;' % name)
    _GMSH_CODE.append('Circle(%s) = {%s, %s, %s};'
                    % (name, point_ids[0], point_ids[1], point_ids[2])
                    )
    return name
# -----------------------------------------------------------------------------
def LineLoop(lines):
    '''Gmsh Line Loops.
    '''
    global _LINELOOP_ID
    _LINELOOP_ID += 1
    name = 'll%d' % _LINELOOP_ID
    _GMSH_CODE.append('%s = newreg;' % name)
    _GMSH_CODE.append('Line Loop(%s) = {%s};' % (name, ','.join(lines)))
    return name
# -----------------------------------------------------------------------------
def PlaneSurface(line_loop):
    '''Create Gmsh Surface.
    '''
    global _SURFACE_ID
    _SURFACE_ID += 1
    sname = 'surf%d' % _SURFACE_ID
    _GMSH_CODE.append('%s = news;' % sname)
    _GMSH_CODE.append('Plane Surface(%s) = {%s};' % (sname, line_loop))

    return sname
# -----------------------------------------------------------------------------
def RuledSurface(line_loop):
    '''Create Gmsh Surface.
    '''
    global _SURFACE_ID
    _SURFACE_ID += 1
    sname = 'surf%d' % _SURFACE_ID
    _GMSH_CODE.append('%s = news;' % sname)
    _GMSH_CODE.append('Ruled Surface(%s) = {%s};' % (sname, line_loop))

    return sname
# -----------------------------------------------------------------------------
def SurfaceLoop(surfaces):
    '''Gmsh Surface Loop.
    '''
    global _SURFACELOOP_ID
    _SURFACELOOP_ID += 1
    name = 'surfloop%d' % _SURFACELOOP_ID
    _GMSH_CODE.append('%s = newreg;' % name)
    _GMSH_CODE.append('Surface Loop(%s) = {%s};' % (name, ','.join(surfaces)))

    return name
# -----------------------------------------------------------------------------
def PhysicalSurface(surface, label):
    '''Gmsh Physical Surface.
    '''
    _GMSH_CODE.append('Physical Surface("%s") = %s;' % (label, surface))
    return
# -----------------------------------------------------------------------------
def Volume(surface_loop):
    '''Gmsh Volume.
    '''
    global _VOLUME_ID
    _VOLUME_ID += 1
    name = 'vol%d' % _VOLUME_ID
    _GMSH_CODE.append('%s = newreg;' % name)
    _GMSH_CODE.append('Volume(%s) = %s;' % (name, surface_loop))

    return name
# -----------------------------------------------------------------------------
def PhysicalVolume(volume, label):
    '''Gmsh Physical Volume.
    '''
    _GMSH_CODE.append('Physical Volume("%s") = %s;' % (label, volume))
    return
# -----------------------------------------------------------------------------
def Extrude(entity, axis, point_on_axis, angle, recombine=True):
    '''Extrusion (rotation) of any entity around an axis by a given angle.
    '''
    global _EXTRUDE_ID
    _EXTRUDE_ID += 1

    #  ex4[] = Extrude {{0,0,1}, {0,0,0}, 2*Pi/3}{Line{tc4};};
    name = 'ex%d' % _EXTRUDE_ID
    if recombine:
        recombine_str = 'Recombine;'
    else:
        recombine_str = ''
    _GMSH_CODE.append('%s[] = Extrude{{%s,%s,%s}, {%s,%s,%s}, %s}{%s;%s};'
                    % ((name,) + tuple(axis) + tuple(point_on_axis)
                      + (angle, entity, recombine_str)))

    return name
# -----------------------------------------------------------------------------
def Array(entities):
    '''Forms a Gmsh array from a list of entities.
    '''
    global _ARRAY_ID
    _ARRAY_ID += 1
    name = 'array%d' % _ARRAY_ID
    _GMSH_CODE.append('%s[] = {%s};' % (name, ','.join(entities)))
    return name + '[]'
# -----------------------------------------------------------------------------
def Comment(string):
    _GMSH_CODE.append('// ' + string)
    return
# -----------------------------------------------------------------------------
def raw_code(list_of_strings):
    '''Add raw Gmsh code.
    '''
    for string in list_of_strings:
        _GMSH_CODE.append(string)
    return
# -----------------------------------------------------------------------------
