# -*- coding: utf-8 -*-
#
'''
This class provides a Python interface for the Gmsh scripting language. It aims
at working around some of Gmsh's inconveniences (e.g., having to manually
assign an ID for every entity created) and providing access to Python's
features.
'''

from .__about__ import __version__

from .bspline import Bspline
from .circle_arc import CircleArc
from .compound_line import CompoundLine
from .compound_surface import CompoundSurface
from .compound_volume import CompoundVolume
from .dummy import Dummy
from .ellipse_arc import EllipseArc
from .line import Line
from .line_base import LineBase
from .line_loop import LineLoop
from .plane_surface import PlaneSurface
from .point import Point
from .ruled_surface import RuledSurface
from .surface_base import SurfaceBase
from .surface_loop import SurfaceLoop
from .volume import Volume
from .volume_base import VolumeBase

import numpy


class Geometry(object):

    def __init__(self):
        # In Gmsh, the user must manually provide a unique ID for every point,
        # curce, volume created. This can get messy when a lot of entities are
        # created and it isn't clear which IDs are already in use. Some Gmsh
        # commands even create new entities and silently reserve IDs in that
        # way. This module tries to work around this by providing routines in
        # the style of add_point(x) which *returns* the ID. To make variable
        # names in Gmsh unique, keep track of how many points, cirlces, etc.
        # have already been created. Variable names will then be p1, p2, etc.
        # for points, c1, c2, etc. for circles and so on.
        self._EXTRUDE_ID = 0
        self._ARRAY_ID = 0
        self._FIELD_ID = 0
        self._PHYSICALGROUP_ID = 0
        self._GMSH_CODE = [
                self._header()
                ]
        return

    def _header(self):
        '''Return file header.
        '''
        header = '// This code was created by PyGmsh v%s.' % __version__
        return header

    def get_code(self):
        '''Returns properly formatted Gmsh code.
        '''
        return '\n'.join(self._GMSH_CODE)

    # All of the add_* method below could be replaced by
    #
    #   def add(self, entity):
    #       self._GMSH_CODE.append(entity.code)
    #       return entity
    #
    # to be used like
    #
    #    geom.add(pg.Circle(...))
    #
    # However, this would break backwards compatibility and perhaps encourage
    # users to do
    #
    #    c = pg.Circle(...)
    #    # ... use c
    #
    # in which case the circle code never gets added to geom.

    def add_bspline(self, *args, **kwargs):
        p = Bspline(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_circle_arc(self, *args, **kwargs):
        p = CircleArc(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_compound_line(self, *args, **kwargs):
        e = CompoundLine(*args, **kwargs)
        self._GMSH_CODE.append(e.code)
        return e

    def add_compound_surface(self, *args, **kwargs):
        e = CompoundSurface(*args, **kwargs)
        self._GMSH_CODE.append(e.code)
        return e

    def add_compound_volume(self, *args, **kwargs):
        e = CompoundVolume(*args, **kwargs)
        self._GMSH_CODE.append(e.code)
        return e

    def add_ellipse_arc(self, *args, **kwargs):
        p = EllipseArc(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_line(self, *args, **kwargs):
        p = Line(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_line_loop(self, *args, **kwargs):
        p = LineLoop(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_plane_surface(self, *args, **kwargs):
        p = PlaneSurface(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_point(self, *args, **kwargs):
        p = Point(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_ruled_surface(self, *args, **kwargs):
        p = RuledSurface(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_surface_loop(self, *args, **kwargs):
        e = SurfaceLoop(*args, **kwargs)
        self._GMSH_CODE.append(e.code)
        return e

    def add_volume(self, *args, **kwargs):
        e = Volume(*args, **kwargs)
        self._GMSH_CODE.append(e.code)
        return e

    def _new_physical_group(self, label=None):
        self._PHYSICALGROUP_ID += 1
        if label is None:
            label = '%d' % self._PHYSICALGROUP_ID
        else:
            label = '"%s"' % label
        return label

    def add_physical_point(self, point, label=None):
        label = self._new_physical_group(label)
        self._GMSH_CODE.append(
            'Physical Point(%s) = %s;' % (label, point.id)
            )
        return

    def add_physical_line(self, line, label=None):
        label = self._new_physical_group(label)
        self._GMSH_CODE.append(
            'Physical Line(%s) = %s;' % (label, line.id)
            )
        return

    def add_physical_surface(self, surface, label=None):
        label = self._new_physical_group(label)
        self._GMSH_CODE.append(
            'Physical Surface(%s) = %s;' % (label, surface.id)
            )
        return

    def add_physical_volume(self, volume, label=None):
        label = self._new_physical_group(label)
        self._GMSH_CODE.append(
            'Physical Volume(%s) = %s;' % (label, volume.id)
            )
        return

    def add_circle(
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

        # Apply the transformation.
        # TODO assert that the transformation preserves circles
        X = [numpy.dot(R, x) + x0 for x in X]
        # Add Gmsh Points.
        p = [self.add_point(x, lcar) for x in X]

        # Define the circle arcs.
        arcs = [
            self.add_circle_arc([p[k], p[0], p[k+1]])
            for k in range(1, len(p)-1)
            ]
        arcs.append(self.add_circle_arc([p[-1], p[0], p[1]]))

        if compound:
            arcs = [self.add_compound_line(arcs)]

        line_loop = self.add_line_loop(arcs)

        if make_surface:
            plane_surface = self.add_plane_surface(line_loop, holes)
        else:
            plane_surface = None

        class Circle(object):
            def __init__(
                    self, x0, radius, lcar, R, compound, num_sections, holes,
                    line_loop, plane_surface
                    ):
                self.x0 = x0
                self.radius = radius
                self.lcar = lcar
                self.R = R
                self.compound = compound
                self.num_sections = num_sections
                self.holes = holes
                self.line_loop = line_loop
                self.plane_surface = plane_surface
                return

        return Circle(
            x0, radius, lcar, R, compound, num_sections, holes,
            line_loop, plane_surface
            )

    def extrude(
            self,
            input_entity,
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
        self._EXTRUDE_ID += 1

        if isinstance(input_entity, str):
            entity = Dummy(input_entity)
        elif isinstance(input_entity, SurfaceBase):
            entity = Dummy('Surface{%s}' % input_entity.id)
        elif hasattr(input_entity, 'surface'):
            entity = Dummy('Surface{%s}' % input_entity.surface.id)
        elif isinstance(input_entity, LineBase):
            entity = Dummy('Line{%s}' % input_entity.id)
        else:
            raise RuntimeError('Illegal extrude entity.')

        # out[] = Extrude{0,1,0}{ Line{1}; };
        name = 'ex%d' % self._EXTRUDE_ID
        if translation_axis is not None and rotation_axis is not None:
            self._GMSH_CODE.append(
                    ('%s[] = Extrude{{%s,%s,%s}, '
                     '{%s,%s,%s}, {%s,%s,%s}, %s}{%s;};') %
                    ((name,) + tuple(translation_axis) + tuple(rotation_axis) +
                     tuple(point_on_axis) + (angle, entity.id))
                    )

        elif translation_axis is not None:
            # Only translation
            self._GMSH_CODE.append(
                '%s[] = Extrude{%s,%s,%s}{%s;};' %
                ((name,) + tuple(translation_axis) + (entity.id,))
                )
        elif rotation_axis is not None:
            # Only rotation
            self._GMSH_CODE.append(
                '%s[] = Extrude{{%s,%s,%s}, {%s,%s,%s}, %s}{%s;};' %
                ((name,) + tuple(rotation_axis) + tuple(point_on_axis) +
                    (angle, entity.id))
                )
        else:
            raise RuntimeError('Specify at least translation or rotation.')

        # From <http://www.manpagez.com/info/gmsh/gmsh-2.4.0/gmsh_66.php>:
        #
        # > In this last extrusion command we retrieved the volume number
        # > programatically by saving the output of the command into a
        # > list. This list will contain the "top" of the extruded surface (in
        # > out[0]) as well as the newly created volume (in out[1]).
        #
        top = '%s[0]' % name
        extruded = '%s[1]' % name

        if isinstance(input_entity, LineBase):
            top = LineBase(top)
            extruded = SurfaceBase(extruded)
        elif isinstance(input_entity, SurfaceBase):
            top = SurfaceBase(top)
            extruded = VolumeBase(extruded)
        else:
            top = Dummy(top)
            extruded = Dummy(extruded)

        return top, extruded

    def add_boundary_layer(
            self,
            edges_list=None,
            faces_list=None,
            nodes_list=None,
            anisomax=None,
            hfar=None,
            hwall_n=None,
            hwall_t=None,
            ratio=None,
            thickness=None
            ):
        # Don't use [] as default argument, cf.
        # <http://stackoverflow.com/a/113198/353337>
        if edges_list is None:
            edges_list = []
        if faces_list is None:
            faces_list = []
        if nodes_list is None:
            nodes_list = []

        self._FIELD_ID += 1
        name = 'field%d' % self._FIELD_ID

        self._GMSH_CODE.append('%s = newf;' % name)

        self._GMSH_CODE.append('Field[%s] = BoundaryLayer;' % name)
        if edges_list:
            self._GMSH_CODE.append(
                'Field[%s].EdgesList = {%s};'
                % (name, ','.join([e.id for e in edges_list]))
                )
        if faces_list:
            self._GMSH_CODE.append(
                'Field[%s].FacesList = {%s};' % (name, ','.join(faces_list))
                )
        if nodes_list:
            self._GMSH_CODE.append(
                'Field[%s].NodesList = {%s};' %
                (name, ','.join([n.id for n in nodes_list]))
                )
        if hfar:
            self._GMSH_CODE.append('Field[%s].hfar= %r;' % (name, hfar))
        if hwall_t:
            self._GMSH_CODE.append('Field[%s].hwall_t= %r;' % (name, hwall_t))
        if hwall_n:
            self._GMSH_CODE.append('Field[%s].hwall_n= %r;' % (name, hwall_n))
        if ratio:
            self._GMSH_CODE.append('Field[%s].ratio= %r;' % (name, ratio))
        if thickness:
            self._GMSH_CODE.append(
                'Field[%s].thickness= %r;' % (name, thickness)
                )
        if anisomax:
            self._GMSH_CODE.append(
                'Field[%s].AnisoMax= %r;' % (name, anisomax)
                )
        return name

    def add_background_field(self, fields, aggregation_type='Min'):
        self._FIELD_ID += 1
        name = 'field%d' % self._FIELD_ID
        self._GMSH_CODE.append(
            '%s = newf;' % name
            )
        self._GMSH_CODE.append(
            'Field[%s] = %s;' % (name, aggregation_type)
            )
        self._GMSH_CODE.append(
            'Field[%s].FieldsList = {%s};' % (name, ', '.join(fields))
            )
        self._GMSH_CODE.append(
            'Background Field = %s;' % name
            )
        return name

    def add_array(self, entities):
        '''Forms a Gmsh array from a list of entities.
        '''
        self._ARRAY_ID += 1
        name = 'array%d' % self._ARRAY_ID
        self._GMSH_CODE.append(
                '%s[] = {%s};'
                % (name, ','.join([e.id for e in entities]))
                )
        return name + '[]'

    def add_comment(self, string):
        self._GMSH_CODE.append('// ' + string)
        return

    def add_raw_code(self, string_or_list):
        '''Add raw Gmsh code.
        '''
        if isinstance(string_or_list, str):
            self._GMSH_CODE.append(string_or_list)
        else:
            for string in string_or_list:
                self._GMSH_CODE.append(string)
        return

    def add_rectangle(self, xmin, xmax, ymin, ymax, z, lcar, holes=None):
        return self.add_polygon([
                [xmin, ymin, z],
                [xmax, ymin, z],
                [xmax, ymax, z],
                [xmin, ymax, z]
                ],
                lcar,
                holes=holes
                )

    def add_polygon(self, X, lcar, holes=None, make_surface=True):
        if holes is None:
            holes = []
        else:
            assert make_surface

        # Create points.
        p = [self.add_point(x, lcar) for x in X]
        # Create lines
        lines = [self.add_line(p[k], p[k+1]) for k in range(len(p)-1)]
        lines.append(self.add_line(p[-1], p[0]))
        ll = self.add_line_loop((lines))
        if make_surface:
            surface = self.add_plane_surface(ll, holes)
        else:
            surface = None

        class Polygon(object):
            def __init__(self, line_loop, surface, lcar):
                self.line_loop = line_loop
                self.surface = surface
                self.lcar = lcar
                return

        return Polygon(ll, surface, lcar)

    def add_ellipsoid(
            self,
            x0, radii, lcar,
            with_volume=True,
            holes=None,
            label=None
            ):
        '''Creates an ellipsoid with radii around a given midpoint
        :math:`x_0`.
        '''
        if holes is None:
            holes = []

        # Add points.
        a = lcar
        p = [
            self.add_point(x0, lcar=lcar),
            self.add_point([x0[0]+radii[0], x0[1], x0[2]], lcar=a),
            self.add_point([x0[0], x0[1]+radii[1], x0[2]], lcar=a),
            self.add_point([x0[0], x0[1], x0[2]+radii[2]], lcar=a),
            self.add_point([x0[0]-radii[0], x0[1], x0[2]], lcar=a),
            self.add_point([x0[0], x0[1]-radii[1], x0[2]], lcar=a),
            self.add_point([x0[0], x0[1], x0[2]-radii[2]], lcar=a),
            ]
        # Add skeleton.
        # Alternative for circles:
        # `self.add_circle_arc([a, b, c])`
        c = [self.add_ellipse_arc([p[1], p[0], p[6], p[6]]),
             self.add_ellipse_arc([p[6], p[0], p[4], p[4]]),
             self.add_ellipse_arc([p[4], p[0], p[3], p[3]]),
             self.add_ellipse_arc([p[3], p[0], p[1], p[1]]),
             self.add_ellipse_arc([p[1], p[0], p[2], p[2]]),
             self.add_ellipse_arc([p[2], p[0], p[4], p[4]]),
             self.add_ellipse_arc([p[4], p[0], p[5], p[5]]),
             self.add_ellipse_arc([p[5], p[0], p[1], p[1]]),
             self.add_ellipse_arc([p[6], p[0], p[2], p[2]]),
             self.add_ellipse_arc([p[2], p[0], p[3], p[3]]),
             self.add_ellipse_arc([p[3], p[0], p[5], p[5]]),
             self.add_ellipse_arc([p[5], p[0], p[6], p[6]]),
             ]
        # Add surfaces (1/8th of the ball surface).
        ll = [
            # one half
            self.add_line_loop([c[4],   c[9],  c[3]]),
            self.add_line_loop([c[8],  -c[4], c[0]]),
            self.add_line_loop([-c[9],  c[5],  c[2]]),
            self.add_line_loop([-c[5], -c[8], c[1]]),
            # the other half
            self.add_line_loop([c[7],   -c[3],  c[10]]),
            self.add_line_loop([c[11],  -c[7], -c[0]]),
            self.add_line_loop([-c[10], -c[2],  c[6]]),
            self.add_line_loop([-c[1],  -c[6], -c[11]]),
            ]
        # Create a surface for each line loop.
        s = [self.add_ruled_surface(l) for l in ll]
        # Combine the surfaces to avoid seams
        new_surfs = [
                self.add_compound_surface(s[:4]),
                self.add_compound_surface(s[4:])
                ]

        # Create the surface loop.
        surface_loop = self.add_surface_loop(new_surfs)
        # if holes:
        #     # Create an array of surface loops; the first entry is the outer
        #     # surface loop, the following ones are holes.
        #     surface_loop = self.add_array([surface_loop] + holes)
        # Create volume.
        if with_volume:
            volume = self.add_volume(surface_loop, holes)
            if label:
                self.add_physical_volume(volume, label)
        else:
            volume = None

        class Ellipsoid(object):
            def __init__(self, x0, radii, lcar, surface_loop, volume):
                self.x0 = x0
                self.lcar = lcar
                self.radii = radii
                self.surface_loop = surface_loop
                self.volume = volume
                return

        return Ellipsoid(x0, radii, lcar, surface_loop, volume)

    def add_ball(
            self,
            x0, radius, lcar,
            with_volume=True,
            holes=None,
            label=None
            ):
        return self.add_ellipsoid(
            x0, [radius, radius, radius], lcar,
            with_volume,
            holes,
            label
            )

    def add_box(
            self,
            x0, x1, y0, y1, z0, z1,
            lcar,
            with_volume=True,
            holes=None,
            label=None
            ):

        if holes is None:
            holes = []

        # Define corner points.
        p = [self.add_point([x1, y1, z1], lcar=lcar),
             self.add_point([x1, y1, z0], lcar=lcar),
             self.add_point([x1, y0, z1], lcar=lcar),
             self.add_point([x1, y0, z0], lcar=lcar),
             self.add_point([x0, y1, z1], lcar=lcar),
             self.add_point([x0, y1, z0], lcar=lcar),
             self.add_point([x0, y0, z1], lcar=lcar),
             self.add_point([x0, y0, z0], lcar=lcar),
             ]
        # Define edges.
        e = [self.add_line(p[0], p[1]),
             self.add_line(p[0], p[2]),
             self.add_line(p[0], p[4]),
             self.add_line(p[1], p[3]),
             self.add_line(p[1], p[5]),
             self.add_line(p[2], p[3]),
             self.add_line(p[2], p[6]),
             self.add_line(p[3], p[7]),
             self.add_line(p[4], p[5]),
             self.add_line(p[4], p[6]),
             self.add_line(p[5], p[7]),
             self.add_line(p[6], p[7]),
             ]
        # Define the six line loops.
        ll = [self.add_line_loop([e[0], e[3],  -e[5],  -e[1]]),
              self.add_line_loop([e[0], e[4],  -e[8],  -e[2]]),
              self.add_line_loop([e[1], e[6],  -e[9],  -e[2]]),
              self.add_line_loop([e[3], e[7],  -e[10], -e[4]]),
              self.add_line_loop([e[5], e[7],  -e[11], -e[6]]),
              self.add_line_loop([e[8], e[10], -e[11], -e[9]]),
              ]
        # Create a surface for each line loop.
        s = [self.add_ruled_surface(l) for l in ll]
        # Create the surface loop.
        surface_loop = self.add_surface_loop(s)
        if holes:
            # Create an array of surface loops; the first entry is the outer
            # surface loop, the following ones are holes.
            surface_loop = self.add_array([surface_loop] + holes)
        if with_volume:
            # Create volume
            vol = self.add_volume(surface_loop)
            if label:
                self.add_physical_volume(vol, label)
        else:
            vol = None

        class Box(object):
            def __init__(
                    self, x0, x1, y0, y1, z0, z1,
                    lcar, surface_loop, volume
                    ):
                self.x0 = x0
                self.x1 = x1
                self.y0 = y0
                self.y1 = y1
                self.z0 = z0
                self.z1 = z1
                self.lcar = lcar
                self.surface_loop = surface_loop
                self.volume = volume
                return

        return Box(x0, x1, y0, y1, z0, z1, lcar, surface_loop, vol)

    def add_torus(
            self,
            irad, orad,
            lcar,
            R=numpy.eye(3),
            x0=numpy.array([0.0, 0.0, 0.0]),
            label=None,
            variant='extrude_lines'
            ):

        if variant == 'extrude_lines':
            return self._add_torus_extrude_lines(
                irad, orad,
                lcar,
                R=R,
                x0=x0,
                label=label
                )
        elif variant == 'extrude_circle':
            return self._add_torus_extrude_circle(
                irad, orad,
                lcar,
                R=R,
                x0=x0,
                label=label
                )
        else:
            raise ValueError(
                'Illegal variant \'%s\'.' % variant
                )

    def _add_torus_extrude_lines(
            self,
            irad, orad,
            lcar,
            R=numpy.eye(3),
            x0=numpy.array([0.0, 0.0, 0.0]),
            label=None
            ):
        '''Create Gmsh code for the torus in the x-y plane under the coordinate
        transformation

        .. math::
            \hat{x} = R x + x_0.

        :param irad: inner radius of the torus
        :param orad: outer radius of the torus
        '''
        self.add_comment(76 * '-')
        self.add_comment('Torus')

        # Add circle
        x0t = numpy.dot(R, numpy.array([0.0, orad, 0.0]))
        # Get circles in y-z plane
        Rc = numpy.array([
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0]
            ])

        c = self.add_circle(x0+x0t, irad, lcar, R=numpy.dot(R, Rc))

        rot_axis = [0.0, 0.0, 1.0]
        rot_axis = numpy.dot(R, rot_axis)
        point_on_rot_axis = [0.0, 0.0, 0.0]
        point_on_rot_axis = numpy.dot(R, point_on_rot_axis) + x0

        # Form the torus by extruding the circle three times by 2/3*pi. This
        # works around the inability of Gmsh to extrude by pi or more. The
        # Extrude() macro returns an array; the first [0] entry in the array is
        # the entity that has been extruded at the far end. This can be used
        # for the following Extrude() step.  The second [1] entry of the array
        # is the surface that was created by the extrusion.
        previous = c.line_loop.lines
        angle = '2*Pi/3'
        all_surfaces = []
        for i in range(3):
            self.add_comment('Round no. %s' % (i+1))
            for k in range(len(previous)):
                # ts1[] = Extrude {{0,0,1}, {0,0,0}, 2*Pi/3}{Line{tc1};};
                # ...
                top, surf = self.extrude(
                    previous[k],
                    rotation_axis=rot_axis,
                    point_on_axis=point_on_rot_axis,
                    angle=angle
                    )
                all_surfaces.append(surf)
                previous[k] = top

        # compound_surface = CompoundSurface(all_surfaces)

        surface_loop = self.add_surface_loop(all_surfaces)
        vol = self.add_volume(surface_loop)
        if label:
            self.add_physical_volume(vol, label)

        # The newline at the end is essential:
        # If a GEO file doesn't end in a newline, Gmsh will report a syntax
        # error.
        self.add_comment(76*'-' + '\n')
        return

    def _add_torus_extrude_circle(
            self,
            irad, orad,
            lcar,
            R=numpy.eye(3),
            x0=numpy.array([0.0, 0.0, 0.0]),
            label=None
            ):
        '''Create Gmsh code for the torus under the coordinate transformation

        .. math::
            \hat{x} = R x + x_0.

        :param irad: inner radius of the torus
        :param orad: outer radius of the torus
        '''
        self.add_comment(76*'-')
        self.add_comment('Torus')

        # Add circle
        x0t = numpy.dot(R, numpy.array([0.0, orad, 0.0]))
        Rc = numpy.array([
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0]
            ])
        c = self.add_circle(x0+x0t, irad, lcar, R=numpy.dot(R, Rc))

        rot_axis = [0.0, 0.0, 1.0]
        rot_axis = numpy.dot(R, rot_axis)
        point_on_rot_axis = [0.0, 0.0, 0.0]
        point_on_rot_axis = numpy.dot(R, point_on_rot_axis) + x0

        # Form the torus by extruding the circle three times by 2/3*pi. This
        # works around the inability of Gmsh to extrude by pi or more. The
        # Extrude() macro returns an array; the first [0] entry in the array is
        # the entity that has been extruded at the far end. This can be used
        # for the following Extrude() step.  The second [1] entry of the array
        # is the surface that was created by the extrusion.
        previous = c.plane_surface
        all_volumes = []
        num_steps = 3
        for _ in range(num_steps):
            top, vol = self.extrude(
                previous,
                rotation_axis=rot_axis,
                point_on_axis=point_on_rot_axis,
                angle='2*Pi/%d' % num_steps
                )
            previous = top
            all_volumes.append(vol)

        vol = self.add_compound_volume(all_volumes)
        if label:
            self.add_physical_volume(vol, label)
        self.add_comment(76*'-' + '\n')
        return

    def add_pipe(
            self,
            outer_radius, inner_radius, length,
            R=numpy.eye(3),
            x0=numpy.array([0.0, 0.0, 0.0]),
            label=None,
            lcar=0.1,
            variant='rectangle_rotation'
            ):
        if variant == 'rectangle_rotation':
            return self._add_pipe_by_rectangle_rotation(
                outer_radius, inner_radius, length,
                R=R,
                x0=x0,
                label=label,
                lcar=lcar
                )
        elif variant == 'circle_extrusion':
            return self._add_pipe_by_circle_extrusion(
                outer_radius, inner_radius, length,
                R=R,
                x0=x0,
                label=label,
                lcar=lcar
                )
        else:
            raise ValueError(
                'Illegal variant \'%s\'.' % variant
                )

    def _add_pipe_by_rectangle_rotation(
            self,
            outer_radius, inner_radius, length,
            R=numpy.eye(3),
            x0=numpy.array([0.0, 0.0, 0.0]),
            label=None,
            lcar=0.1
            ):
        '''Hollow cylinder.
        Define a rectangle, extrude it by rotation.
        '''
        self.add_comment('Define rectangle.')
        X = numpy.array([
            [0.0, outer_radius, -0.5*length],
            [0.0, outer_radius,  0.5*length],
            [0.0, inner_radius,  0.5*length],
            [0.0, inner_radius, -0.5*length]
            ])
        # Apply transformation.
        X = [numpy.dot(R, x) + x0 for x in X]
        # Create points set.
        p = [self.add_point(x, lcar) for x in X]

        # Define edges.
        e = [self.add_line(p[0], p[1]),
             self.add_line(p[1], p[2]),
             self.add_line(p[2], p[3]),
             self.add_line(p[3], p[0])
             ]

        rot_axis = [0.0, 0.0, 1.0]
        rot_axis = numpy.dot(R, rot_axis)
        point_on_rot_axis = [0.0, 0.0, 0.0]
        point_on_rot_axis = numpy.dot(R, point_on_rot_axis) + x0

        # Extrude all edges three times by 2*Pi/3.
        previous = e
        angle = '2*Pi/3'
        all_surfaces = []
        # com = []
        self.add_comment('Extrude in 3 steps.')
        for i in range(3):
            self.add_comment('Step %s' % (i+1))
            for k in range(len(previous)):
                # ts1[] = Extrude {{0,0,1}, {0,0,0}, 2*Pi/3}{Line{tc1};};
                top, surf = self.extrude(
                        previous[k],
                        rotation_axis=rot_axis,
                        point_on_axis=point_on_rot_axis,
                        angle=angle
                        )
                # if k==0:
                #     com.append(surf)
                # else:
                #     all_names.appends(surf)
                all_surfaces.append(surf)
                previous[k] = top
        #
        # cs = CompoundSurface(com)
        # Now just add surface loop and volume.
        # all_surfaces = all_names + [cs]
        surface_loop = self.add_surface_loop(all_surfaces)
        vol = self.add_volume(surface_loop)
        if label:
            self.add_physical_volume(vol, label)
        return

    def _add_pipe_by_circle_extrusion(
            self,
            outer_radius, inner_radius, length,
            R=numpy.eye(3),
            x0=numpy.array([0.0, 0.0, 0.0]),
            label=None,
            lcar=0.1
            ):
        '''Hollow cylinder.
        Define a ring, extrude it by translation.
        '''
        # Define ring which to Extrude by translation.
        Rc = numpy.array([
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0]
            ])
        c_inner = self.add_circle(
                x0, inner_radius, lcar, R=numpy.dot(R, Rc),
                make_surface=False
                )
        circ = self.add_circle(
                x0, outer_radius, lcar, R=numpy.dot(R, Rc),
                holes=[c_inner.line_loop]
                )

        # Now Extrude the ring surface.
        _, vol = self.extrude(
                circ.plane_surface,
                translation_axis=numpy.dot(R, [length, 0, 0])
                )
        if label:
            self.add_physical_volume(vol, label)
        return vol
