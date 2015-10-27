# -*- coding: utf8 -*-
#
'''
This module provides a Python interface for the Gmsh scripting language.  It
aims at working around some of Gmsh's inconveniences (e.g., having to manually
assign an ID for every entity created) and providing access to Python's
features.
'''

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
_FIELD_ID = 0

from pygmsh import __name__, __version__

def _header():
    '''Return file header.
    '''
    header = '// This code was created by %s v%s.' % (__name__, __version__)
    return header

_GMSH_CODE = [_header()]


def get_code():
    '''Returns properly formatted Gmsh code.
    '''
    return '\n'.join(_GMSH_CODE)


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


def Line(p0, p1):
    '''Add line.
    '''
    global _LINE_ID
    _LINE_ID += 1
    name = 'l%d' % _LINE_ID
    _GMSH_CODE.append('%s = newl;' % name)
    _GMSH_CODE.append('Line(%s) = {%s, %s};' % (name, p0, p1))
    return name


def BSpline(control_points):
    '''Add B-spline.
    '''
    n = len(control_points)
    if n < 4:
        raise RuntimeError(('BSpline needs at least four control points (%d '
                            'given).') % n)
    global _LINE_ID
    _LINE_ID += 1
    name = 'bspline%d' % _LINE_ID
    _GMSH_CODE.append('%s = newl;' % name)
    _GMSH_CODE.append('BSpline(%s) = {%s};'
                      % (name, ', '.join(control_points))
                      )
    return name


def Circle(point_ids):
    '''Add Circle.
    '''
    global _CIRCLE_ID
    _CIRCLE_ID += 1
    name = 'c%d' % _CIRCLE_ID
    _GMSH_CODE.append('%s = newl;' % name)
    _GMSH_CODE.append('Circle(%s) = {%s, %s, %s};'
                      % (name, point_ids[0], point_ids[1], point_ids[2])
                      )
    return name


def CompoundLine(lines):
    '''Gmsh Compound Line.
    '''
    global _LINE_ID
    _LINE_ID += 1
    name = 'l%d' % _LINE_ID
    _GMSH_CODE.append('%s = newl;' % name)
    _GMSH_CODE.append('Compound Line(%s) = {%s};' % (name, ','.join(lines)))
    return name


def LineLoop(lines):
    '''Gmsh Line Loops.
    '''
    global _LINELOOP_ID
    _LINELOOP_ID += 1
    name = 'll%d' % _LINELOOP_ID
    _GMSH_CODE.append('%s = newll;' % name)
    _GMSH_CODE.append('Line Loop(%s) = {%s};' % (name, ','.join(lines)))
    return name


def PlaneSurface(line_loop):
    '''Create Gmsh Surface.
    '''
    global _SURFACE_ID
    _SURFACE_ID += 1
    sname = 'surf%d' % _SURFACE_ID
    _GMSH_CODE.append('%s = news;' % sname)
    _GMSH_CODE.append('Plane Surface(%s) = {%s};' % (sname, line_loop))
    return sname


def RuledSurface(line_loop):
    '''Create Gmsh Surface.
    '''
    global _SURFACE_ID
    _SURFACE_ID += 1
    sname = 'surf%d' % _SURFACE_ID
    _GMSH_CODE.append('%s = news;' % sname)
    _GMSH_CODE.append('Ruled Surface(%s) = {%s};' % (sname, line_loop))
    return sname


def CompoundSurface(surfaces):
    '''Gmsh Compound Surface.
    '''
    global _SURFACE_ID
    _SURFACE_ID += 1
    name = 'surf%d' % _SURFACE_ID
    _GMSH_CODE.append('%s = news;' % name)
    _GMSH_CODE.append('Compound Surface(%s) = {%s};'
                      % (name, ','.join(surfaces))
                      )
    return name


def SurfaceLoop(surfaces):
    '''Gmsh Surface Loop.
    '''
    global _SURFACELOOP_ID
    _SURFACELOOP_ID += 1
    name = 'surfloop%d' % _SURFACELOOP_ID
    _GMSH_CODE.append('%s = newsl;' % name)
    _GMSH_CODE.append('Surface Loop(%s) = {%s};' % (name, ','.join(surfaces)))
    return name


def PhysicalSurface(surface, label):
    '''Gmsh Physical Surface.
    '''
    _GMSH_CODE.append('Physical Surface("%s") = %s;' % (label, surface))
    return


def Volume(surface_loop):
    '''Gmsh Volume.
    '''
    global _VOLUME_ID
    _VOLUME_ID += 1
    name = 'vol%d' % _VOLUME_ID
    _GMSH_CODE.append('%s = newv;' % name)
    _GMSH_CODE.append('Volume(%s) = %s;' % (name, surface_loop))

    return name


def CompoundVolume(volumes):
    '''Gmsh Compound Volume.
    '''
    global _VOLUME_ID
    _VOLUME_ID += 1
    name = 'cv%d' % _VOLUME_ID
    _GMSH_CODE.append('%s = newv;' % name)
    _GMSH_CODE.append('Compound Volume(%s) = {%s};'
                      % (name, ','.join(volumes))
                      )
    return name


def PhysicalVolume(volume, label):
    '''Gmsh Physical Volume.
    '''
    _GMSH_CODE.append('Physical Volume("%s") = %s;' % (label, volume))
    return


def Extrude(entity,
            translation_axis=None,
            rotation_axis=None,
            point_on_axis=None,
            angle=None
            ):
    '''Extrusion (translation + rotation) of any entity along a given
    translation_axis, around a given rotation_axis, about a given angle. If
    one of the entities is not provided, this method will produce only
    translation or rotation.
    '''
    global _EXTRUDE_ID
    _EXTRUDE_ID += 1

    # out[] = Extrude{0,1,0}{ Line{1}; };
    name = 'ex%d' % _EXTRUDE_ID
    if translation_axis is not None and rotation_axis is not None:
        _GMSH_CODE.append(('%s[] = Extrude{{%s,%s,%s}, '
                           '{%s,%s,%s}, {%s,%s,%s}, %s}{%s;};')
                          % ((name,) +
                             tuple(translation_axis) +
                             tuple(rotation_axis) +
                             tuple(point_on_axis) +
                             (angle, entity))
                          )

    elif translation_axis is not None:
        # Only translation
        _GMSH_CODE.append('%s[] = Extrude{%s,%s,%s}{%s;};'
                          % ((name,) + tuple(translation_axis) + (entity,)))
    elif rotation_axis is not None:
        # Only rotation
        _GMSH_CODE.append('%s[] = Extrude{{%s,%s,%s}, {%s,%s,%s}, %s}{%s;};'
                          % ((name,) +
                             tuple(rotation_axis) +
                             tuple(point_on_axis) +
                             (angle, entity))
                          )

    else:
        raise RuntimeError('Specify at least translation or rotation.')
    return name


def BoundaryLayer(edges_list=None,
                  faces_list=None,
                  nodes_list=None,
                  anisomax=None,
                  hfar=None,
                  hwall_n=None,
                  hwall_t=None,
                  ratio=None,
                  thickness=None
                  ):
    '''Add boundary layer.
    '''
    # Don't use [] as default argument, cf.
    # <http://stackoverflow.com/a/113198/353337>
    if edges_list is None:
        edges_list = []
    if faces_list is None:
        faces_list = []
    if nodes_list is None:
        nodes_list = []

    global _FIELD_ID
    _FIELD_ID += 1
    name = 'field%d' % _FIELD_ID

    _GMSH_CODE.append('%s = newf;' % name)

    _GMSH_CODE.append('Field[%s] = BoundaryLayer;' % name)
    if edges_list:
        _GMSH_CODE.append('Field[%s].EdgesList = {%s};'
                          % (name, ','.join(edges_list)))
    if faces_list:
        _GMSH_CODE.append('Field[%s].FacesList = {%s};'
                          % (name, ','.join(faces_list)))
    if nodes_list:
        _GMSH_CODE.append('Field[%s].NodesList = {%s};'
                          % (name, ','.join(nodes_list)))
    if hfar:
        _GMSH_CODE.append('Field[%s].hfar= %g;' % (name, hfar))
    if hwall_t:
        _GMSH_CODE.append('Field[%s].hwall_t= %g;' % (name, hwall_t))
    if hwall_n:
        _GMSH_CODE.append('Field[%s].hwall_n= %g;' % (name, hwall_n))
    if ratio:
        _GMSH_CODE.append('Field[%s].ratio= %g;' % (name, ratio))
    if thickness:
        _GMSH_CODE.append('Field[%s].thickness= %g;' % (name, thickness))
    if anisomax:
        _GMSH_CODE.append('Field[%s].AnisoMax= %g;' % (name, anisomax))
    return name


def Array(entities):
    '''Forms a Gmsh array from a list of entities.
    '''
    global _ARRAY_ID
    _ARRAY_ID += 1
    name = 'array%d' % _ARRAY_ID
    _GMSH_CODE.append('%s[] = {%s};' % (name, ','.join(entities)))
    return name + '[]'


def Comment(string):
    '''Adds a Gmsh comment.
    '''
    _GMSH_CODE.append('// ' + string)
    return


def raw_code(list_of_strings):
    '''Add raw Gmsh code.
    '''
    for string in list_of_strings:
        _GMSH_CODE.append(string)
    return
