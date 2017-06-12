# -*- coding: utf-8 -*-
#
'''
This class provides a Python interface for the Gmsh scripting language. It aims
at working around some of Gmsh's inconveniences (e.g., having to manually
assign an ID for every entity created) and providing access to Python's
features.
'''
import numpy

from .__about__ import __version__

from .bspline import Bspline
from .circle_arc import CircleArc
from .compound_line import CompoundLine
from .compound_surface import CompoundSurface
from .compound_volume import CompoundVolume
from .dummy import Dummy
from .ellipse_arc import EllipseArc
from .helper import _is_string
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
        self._TAKEN_PHYSICALGROUP_IDS = []
        self._GMSH_CODE = [
                '// This code was created by PyGmsh v{}.'.format(__version__)
                ]
        return

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
        # See
        # https://github.com/nschloe/pygmsh/issues/46#issuecomment-286684321
        # for context.
        max_id = \
            0 if not self._TAKEN_PHYSICALGROUP_IDS  \
            else max(self._TAKEN_PHYSICALGROUP_IDS)

        if label is None:
            label = max_id + 1

        if isinstance(label, int):
            assert label not in self._TAKEN_PHYSICALGROUP_IDS
            self._TAKEN_PHYSICALGROUP_IDS += [label]
            return str(label)

        assert _is_string(label)
        self._TAKEN_PHYSICALGROUP_IDS += [max_id + 1]
        return '"{}"'.format(label)

    def _add_physical(self, tpe, entities, label=None):
        label = self._new_physical_group(label)
        if not isinstance(entities, list):
            entities = [entities]
        self._GMSH_CODE.append(
            'Physical {}({}) = {{{}}};'.format(
                tpe, label, ', '.join([e.id for e in entities])
            ))
        return

    def add_physical_point(self, points, label=None):
        self._add_physical('Point', points, label=label)
        return

    def add_physical_line(self, lines, label=None):
        self._add_physical('Line', lines, label=label)
        return

    def add_physical_surface(self, surfaces, label=None):
        self._add_physical('Surface', surfaces, label=label)
        return

    def add_physical_volume(self, volumes, label=None):
        self._add_physical('Volume', volumes, label=label)
        return

    def add_circle(
            self,
            x0, radius, lcar,
            R=None,
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
        X = numpy.zeros((num_sections+1, len(x0)))
        if num_sections == 4:
            # For accuracy, the points are provided explicitly.
            X[1:, [0, 1]] = numpy.array([
                [radius, 0.0],
                [0.0, radius],
                [-radius, 0.0],
                [0.0, -radius]
                ])
        else:
            X[1:, [0, 1]] = numpy.array([
                [
                    radius*numpy.cos(2*numpy.pi * k / num_sections),
                    radius*numpy.sin(2*numpy.pi * k / num_sections),
                ]
                for k in range(num_sections)
                ])

        # Apply the transformation.
        # TODO assert that the transformation preserves circles
        if R is not None:
            X = [numpy.dot(R, x) + x0 for x in X]

        X += x0

        # Add Gmsh Points.
        p = [self.add_point(x, lcar) for x in X]

        # Define the circle arcs.
        arcs = [
            self.add_circle_arc(p[k], p[0], p[k+1])
            for k in range(1, len(p)-1)
            ]
        arcs.append(self.add_circle_arc(p[-1], p[0], p[1]))

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
            angle=None,
            ):
        '''Extrusion (translation + rotation) of any entity along a given
        translation_axis, around a given rotation_axis, about a given angle. If
        one of the entities is not provided, this method will produce only
        translation or rotation.
        '''
        self._EXTRUDE_ID += 1

        if _is_string(input_entity):
            entity = Dummy(input_entity)
        elif isinstance(input_entity, SurfaceBase):
            entity = Dummy('Surface{{{}}}'.format(input_entity.id))
        elif hasattr(input_entity, 'surface'):
            entity = Dummy('Surface{{{}}}'.format(input_entity.surface.id))
        else:
            assert isinstance(input_entity, LineBase), \
                'Illegal extrude entity.'
            entity = Dummy('Line{{{}}}'.format(input_entity.id))

        # out[] = Extrude{0,1,0}{ Line{1}; };
        name = 'ex{}'.format(self._EXTRUDE_ID)
        if translation_axis is not None and rotation_axis is not None:
            self._GMSH_CODE.append(
                '{}[] = Extrude{{{{{}}}, {{{}}}, {{{}}}, {}}}{{{};}};'
                .format(
                    name,
                    ','.join(repr(x) for x in translation_axis),
                    ','.join(repr(x) for x in rotation_axis),
                    ','.join(repr(x) for x in point_on_axis),
                    angle,
                    entity.id
                ))

        elif translation_axis is not None:
            # Only translation
            self._GMSH_CODE.append(
                '{}[] = Extrude{{{}}}{{{};}};'.format(
                    name,
                    ','.join(repr(x) for x in translation_axis),
                    entity.id
                ))
        else:
            assert rotation_axis is not None, \
                'Specify at least translation or rotation.'
            # Only rotation
            self._GMSH_CODE.append(
                '{}[] = Extrude{{{{{}}}, {{{}}}, {}}}{{{};}};'.format(
                    name,
                    ','.join(repr(x) for x in rotation_axis),
                    ','.join(repr(x) for x in point_on_axis),
                    angle,
                    entity.id
                ))

        # From <http://www.manpagez.com/info/gmsh/gmsh-2.4.0/gmsh_66.php>:
        #
        # > In this last extrusion command we retrieved the volume number
        # > programatically by saving the output of the command into a
        # > list. This list will contain the "top" of the extruded surface (in
        # > out[0]) as well as the newly created volume (in out[1]).
        #
        top = '{}[0]'.format(name)
        extruded = '{}[1]'.format(name)

        if isinstance(input_entity, LineBase):
            top = LineBase(top)
            # A surface extruded from a single line has always 4 edges
            extruded = SurfaceBase(extruded, 4)
        elif isinstance(input_entity, SurfaceBase):
            top = SurfaceBase(top, input_entity.num_edges)
            extruded = VolumeBase(extruded)
        else:
            top = Dummy(top)
            extruded = Dummy(extruded)

        lat = []
        # lateral surfaces can be deduced only if we start from a SurfaceBase
        if isinstance(input_entity, SurfaceBase):
            # out[0]` is the surface, out[1] the top, and everything after that
            # the sides, cf.<http://gmsh.info/doc/texinfo/gmsh.html#Extrusions>.
            # each lateral surface has 4 edges: the one from input_entity,
            # the one from top, and the two lines (or splines) connecting their
            # extreme points.
            lat = [SurfaceBase('{}[{}]'.format(name, i+2), 4) \
              for i in range(input_entity.num_edges)]

        return top, extruded, lat

    def add_boundary_layer(
            self,
            edges_list=None,
            faces_list=None,
            nodes_list=None,
            anisomax=None,
            hfar=None,
            hwall_n=None,
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
        name = 'field{}'.format(self._FIELD_ID)

        self._GMSH_CODE.append('{} = newf;'.format(name))

        self._GMSH_CODE.append('Field[{}] = BoundaryLayer;'.format(name))
        if edges_list:
            self._GMSH_CODE.append(
                'Field[{}].EdgesList = {{{}}};'.format(
                    name, ','.join([e.id for e in edges_list])
                ))
        if faces_list:
            self._GMSH_CODE.append(
                'Field[{}].FacesList = {{{}}};'.format(
                    name, ','.join(faces_list)
                ))
        if nodes_list:
            self._GMSH_CODE.append(
                'Field[{}].NodesList = {{{}}};'.format(
                    name, ','.join([n.id for n in nodes_list])
                ))
        if hfar:
            self._GMSH_CODE.append('Field[{}].hfar= {!r};'.format(name, hfar))
        if hwall_n:
            self._GMSH_CODE.append(
                'Field[{}].hwall_n= {!r};'.format(name, hwall_n)
                )
        if ratio:
            self._GMSH_CODE.append('Field[{}].ratio= {!r};'.format(name, ratio))
        if thickness:
            self._GMSH_CODE.append(
                'Field[{}].thickness= {!r};'.format(name, thickness)
                )
        if anisomax:
            self._GMSH_CODE.append(
                'Field[{}].AnisoMax= {!r};'.format(name, anisomax)
                )
        return name

    def add_background_field(self, fields, aggregation_type='Min'):
        self._FIELD_ID += 1
        name = 'field{}'.format(self._FIELD_ID)
        self._GMSH_CODE.append('{} = newf;'.format(name))
        self._GMSH_CODE.append(
            'Field[{}] = {};'.format(name, aggregation_type)
            )
        self._GMSH_CODE.append(
            'Field[{}].FieldsList = {{{}}};'.format(name, ', '.join(fields))
            )
        self._GMSH_CODE.append(
            'Background Field = {};'.format(name)
            )
        return name

    def add_comment(self, string):
        self._GMSH_CODE.append('// ' + string)
        return

    def add_raw_code(self, string_or_list):
        '''Add raw Gmsh code.
        '''
        if _is_string(string_or_list):
            self._GMSH_CODE.append(string_or_list)
        else:
            assert isinstance(string_or_list, list)
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
        surface = self.add_plane_surface(ll, holes) if make_surface else None

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
            holes=None
            ):
        '''Creates an ellipsoid with radii around a given midpoint
        :math:`x_0`.
        '''
        if holes is None:
            holes = []

        if holes:
            assert with_volume

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
        # `self.add_circle_arc(a, b, c)`
        c = [self.add_ellipse_arc(p[1], p[0], p[6], p[6]),
             self.add_ellipse_arc(p[6], p[0], p[4], p[4]),
             self.add_ellipse_arc(p[4], p[0], p[3], p[3]),
             self.add_ellipse_arc(p[3], p[0], p[1], p[1]),
             self.add_ellipse_arc(p[1], p[0], p[2], p[2]),
             self.add_ellipse_arc(p[2], p[0], p[4], p[4]),
             self.add_ellipse_arc(p[4], p[0], p[5], p[5]),
             self.add_ellipse_arc(p[5], p[0], p[1], p[1]),
             self.add_ellipse_arc(p[6], p[0], p[2], p[2]),
             self.add_ellipse_arc(p[2], p[0], p[3], p[3]),
             self.add_ellipse_arc(p[3], p[0], p[5], p[5]),
             self.add_ellipse_arc(p[5], p[0], p[6], p[6]),
             ]
        # Add surfaces (1/8th of the ball surface).
        ll = [
            # one half
            self.add_line_loop([c[4], c[9], c[3]]),
            self.add_line_loop([c[8], -c[4], c[0]]),
            self.add_line_loop([-c[9], c[5], c[2]]),
            self.add_line_loop([-c[5], -c[8], c[1]]),
            # the other half
            self.add_line_loop([c[7], -c[3], c[10]]),
            self.add_line_loop([c[11], -c[7], -c[0]]),
            self.add_line_loop([-c[10], -c[2], c[6]]),
            self.add_line_loop([-c[1], -c[6], -c[11]]),
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
        volume = self.add_volume(surface_loop, holes) if with_volume else None

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
            holes=None
            ):
        return self.add_ellipsoid(
            x0, [radius, radius, radius], lcar,
            with_volume,
            holes
            )

    def add_box(
            self,
            x0, x1, y0, y1, z0, z1,
            lcar,
            with_volume=True,
            holes=None
            ):

        if holes is None:
            holes = []

        if holes:
            assert with_volume

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
        ll = [self.add_line_loop([e[0], e[3], -e[5], -e[1]]),
              self.add_line_loop([e[0], e[4], -e[8], -e[2]]),
              self.add_line_loop([e[1], e[6], -e[9], -e[2]]),
              self.add_line_loop([e[3], e[7], -e[10], -e[4]]),
              self.add_line_loop([e[5], e[7], -e[11], -e[6]]),
              self.add_line_loop([e[8], e[10], -e[11], -e[9]]),
              ]
        # Create a surface for each line loop.
        s = [self.add_ruled_surface(l) for l in ll]
        # Create the surface loop.
        surface_loop = self.add_surface_loop(s)

        # Create volume
        vol = self.add_volume(surface_loop, holes) if with_volume else None

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
            variant='extrude_lines'
            ):

        if variant == 'extrude_lines':
            return self._add_torus_extrude_lines(
                irad, orad,
                lcar,
                R=R,
                x0=x0
                )
        assert variant == 'extrude_circle'
        return self._add_torus_extrude_circle(
            irad, orad,
            lcar,
            R=R,
            x0=x0
            )

    def _add_torus_extrude_lines(
            self,
            irad, orad,
            lcar,
            R=numpy.eye(3),
            x0=numpy.array([0.0, 0.0, 0.0])
            ):
        '''Create Gmsh code for the torus in the x-y plane under the coordinate
        transformation

        .. math::
            \\hat{x} = R x + x_0.

        :param irad: inner radius of the torus
        :param orad: outer radius of the torus
        '''
        self.add_comment('Torus')

        # Add circle
        x0t = numpy.dot(R, numpy.array([0.0, orad, 0.0]))
        # Get circles in y-z plane
        Rc = numpy.array([
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 0.0]
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
            self.add_comment('Round no. {}'.format(i+1))
            for k, p in enumerate(previous):
                # ts1[] = Extrude {{0,0,1}, {0,0,0}, 2*Pi/3}{Line{tc1};};
                # ...
                top, surf, _ = self.extrude(
                    p,
                    rotation_axis=rot_axis,
                    point_on_axis=point_on_rot_axis,
                    angle=angle
                    )
                all_surfaces.append(surf)
                previous[k] = top

        # compound_surface = CompoundSurface(all_surfaces)

        surface_loop = self.add_surface_loop(all_surfaces)
        vol = self.add_volume(surface_loop)

        # The newline at the end is essential:
        # If a GEO file doesn't end in a newline, Gmsh will report a syntax
        # error.
        self.add_comment('\n')
        return vol

    def _add_torus_extrude_circle(
            self,
            irad, orad,
            lcar,
            R=numpy.eye(3),
            x0=numpy.array([0.0, 0.0, 0.0])
            ):
        '''Create Gmsh code for the torus under the coordinate transformation

        .. math::
            \\hat{x} = R x + x_0.

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
        # is the surface that was created by the extrusion. The third [2-end] is
        # a list of all the planes of the lateral surface.
        previous = c.plane_surface
        all_volumes = []
        num_steps = 3
        for _ in range(num_steps):
            top, vol, _ = self.extrude(
                previous,
                rotation_axis=rot_axis,
                point_on_axis=point_on_rot_axis,
                angle='2*Pi/{}'.format(num_steps)
                )
            previous = top
            all_volumes.append(vol)

        vol = self.add_compound_volume(all_volumes)
        self.add_comment(76*'-' + '\n')
        return vol

    def add_pipe(
            self,
            outer_radius, inner_radius, length,
            R=numpy.eye(3),
            x0=numpy.array([0.0, 0.0, 0.0]),
            lcar=0.1,
            variant='rectangle_rotation'
            ):
        if variant == 'rectangle_rotation':
            return self._add_pipe_by_rectangle_rotation(
                outer_radius, inner_radius, length,
                R=R,
                x0=x0,
                lcar=lcar
                )
        assert variant == 'circle_extrusion'
        return self._add_pipe_by_circle_extrusion(
            outer_radius, inner_radius, length,
            R=R,
            x0=x0,
            lcar=lcar
            )

    def _add_pipe_by_rectangle_rotation(
            self,
            outer_radius, inner_radius, length,
            R=numpy.eye(3),
            x0=numpy.array([0.0, 0.0, 0.0]),
            lcar=0.1
            ):
        '''Hollow cylinder.
        Define a rectangle, extrude it by rotation.
        '''
        self.add_comment('Define rectangle.')
        X = numpy.array([
            [0.0, outer_radius, -0.5*length],
            [0.0, outer_radius, +0.5*length],
            [0.0, inner_radius, +0.5*length],
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
            self.add_comment('Step {}'.format(i+1))
            for k, p in enumerate(previous):
                # ts1[] = Extrude {{0,0,1}, {0,0,0}, 2*Pi/3}{Line{tc1};};
                top, surf, _ = self.extrude(
                        p,
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
        return vol

    def _add_pipe_by_circle_extrusion(
            self,
            outer_radius, inner_radius, length,
            R=numpy.eye(3),
            x0=numpy.array([0.0, 0.0, 0.0]),
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
        _, vol, _ = self.extrude(
                circ.plane_surface,
                translation_axis=numpy.dot(R, [length, 0, 0])
                )
        return vol
