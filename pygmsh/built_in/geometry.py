import warnings

import gmsh
import numpy

from ..helpers import get_gmsh_major_version
from .bspline import BSpline
from .circle_arc import CircleArc
from .curve_loop import CurveLoop
from .dummy import Dummy
from .ellipse_arc import EllipseArc
from .line import Line
from .line_base import LineBase
from .plane_surface import PlaneSurface
from .point import Point
from .point_base import PointBase
from .spline import Spline
from .surface import Surface
from .surface_base import SurfaceBase
from .surface_loop import SurfaceLoop
from .volume import Volume
from .volume_base import VolumeBase


class Geometry:
    def __init__(self, gmsh_major_version=None):
        self._BOOLEAN_ID = 0
        self._ARRAY_ID = 0
        self._FIELD_ID = 0
        self._GMSH_MAJOR = gmsh_major_version
        self._TAKEN_PHYSICALGROUP_IDS = []
        self._COMPOUND_ENTITIES = []
        self._RECOMBINE_ENTITIES = []
        self._AFTER_SYNC_QUEUE = []

        gmsh.initialize()
        gmsh.model.add("pygmsh model")

    def _gmsh_major(self):
        if self._GMSH_MAJOR is None:
            self._GMSH_MAJOR = get_gmsh_major_version()
        return self._GMSH_MAJOR

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
        return BSpline(*args, **kwargs)

    def add_circle_arc(self, *args, **kwargs):
        return CircleArc(*args, **kwargs)

    def add_ellipse_arc(self, *args, **kwargs):
        return EllipseArc(*args, **kwargs)

    def add_line(self, *args, **kwargs):
        return Line(*args, **kwargs)

    def add_curve_loop(self, *args, **kwargs):
        return CurveLoop(*args, **kwargs)

    def add_plane_surface(self, *args, **kwargs):
        return PlaneSurface(*args, **kwargs)

    def add_point(self, *args, **kwargs):
        return Point(*args, **kwargs)

    def add_spline(self, *args, **kwargs):
        return Spline(*args, **kwargs)

    def add_surface(self, *args, **kwargs):
        return Surface(*args, **kwargs)

    def add_surface_loop(self, *args, **kwargs):
        return SurfaceLoop(*args, **kwargs)

    def add_volume(self, *args, **kwargs):
        return Volume(*args, **kwargs)

    def _new_physical_group(self, label=None):
        # See
        # https://github.com/nschloe/pygmsh/issues/46#issuecomment-286684321
        # for context.
        max_id = (
            0
            if not self._TAKEN_PHYSICALGROUP_IDS
            else max(self._TAKEN_PHYSICALGROUP_IDS)
        )

        if label is None:
            label = max_id + 1

        if isinstance(label, int):
            assert (
                label not in self._TAKEN_PHYSICALGROUP_IDS
            ), f"Physical group label {label} already taken."
            self._TAKEN_PHYSICALGROUP_IDS += [label]
            return str(label)

        assert isinstance(label, str)
        self._TAKEN_PHYSICALGROUP_IDS += [max_id + 1]
        return f'"{label}"'

    def add_physical(self, entities, label=None):
        if not isinstance(entities, list):
            entities = [entities]

        dim = entities[0].dimension
        for e in entities:
            assert isinstance(
                e,
                (
                    Point,
                    PointBase,
                    LineBase,
                    Surface,
                    PlaneSurface,
                    SurfaceBase,
                    Volume,
                    VolumeBase,
                ),
            ), "Can add physical groups only for Points, Lines, Surfaces, Volumes, not {}.".format(
                type(e)
            )
            assert e.dimension == dim

        label = self._new_physical_group(label)
        tag = gmsh.model.addPhysicalGroup(dim, [e._ID for e in entities])
        if label is not None:
            gmsh.model.setPhysicalName(dim, tag, label)

    def add_physical_point(self, points, label=None):
        warnings.warn("add_physical_point() is deprecated. use add_physical() instead.")
        self.add_physical(points, label=label)

    def add_physical_line(self, lines, label=None):
        warnings.warn("add_physical_line() is deprecated. use add_physical() instead.")
        self.add_physical(lines, label=label)

    def add_physical_surface(self, surfaces, label=None):
        warnings.warn(
            "add_physical_surface() is deprecated. use add_physical() instead."
        )
        self.add_physical(surfaces, label=label)

    def add_physical_volume(self, volumes, label=None):
        warnings.warn(
            "add_physical_volume() is deprecated. use add_physical() instead."
        )
        self.add_physical(volumes, label=label)
        return

    def set_transfinite_lines(self, lines, size, progression=None, bump=None):
        code = "Transfinite Line {{{0}}} = {1}".format(
            ", ".join([l.id for l in lines]), size
        )
        if progression is not None and bump is not None:
            raise ValueError("only one optional argument possible", progression, bump)
        elif progression is not None:
            code += " Using Progression " + str(progression)
        elif bump is not None:
            code += " Using Bump " + str(bump)
        self._GMSH_CODE.append(code + ";")
        return

    def set_transfinite_surface(self, surface, size=None, orientation=None):
        assert surface.num_edges == 4, "a transfinite surface can only have 4 sides"
        # size is not mandatory because in general a user can create it's own
        # transfinite lines and then just tell gmsh that the surface is
        # transfinite too
        if size is not None:
            assert isinstance(
                surface, (PlaneSurface, Surface, self.Polygon)
            ), "we can create transfinite lines only if we have a line loop"
            self.set_transfinite_lines(
                [surface.curve_loop.curves[0], surface.curve_loop.curves[2]], size[0]
            )
            self.set_transfinite_lines(
                [surface.curve_loop.curves[1], surface.curve_loop.curves[3]], size[1]
            )
        code = f"Transfinite Surface {{{surface.id}}}"
        if orientation is not None:
            code += " " + orientation
        self._GMSH_CODE.append(code + ";")
        return

    def set_recombined_surfaces(self, surfaces):
        for i, surface in enumerate(surfaces):
            assert isinstance(
                surface, (PlaneSurface, Surface)
            ), f"item {i} is not a surface"
        for surface in surfaces:
            self._RECOMBINE_ENTITIES.append((2, surface._ID))

    def add_circle(
        self,
        x0,
        radius,
        lcar=None,
        R=None,
        compound=False,
        num_sections=3,
        holes=None,
        make_surface=True,
    ):
        """Add circle in the :math:`x`-:math:`y`-plane."""
        if holes is None:
            holes = []
        else:
            assert make_surface

        # Define points that make the circle (midpoint and the four cardinal
        # directions).
        X = numpy.zeros((num_sections + 1, len(x0)))
        if num_sections == 4:
            # For accuracy, the points are provided explicitly.
            X[1:, [0, 1]] = numpy.array(
                [[radius, 0.0], [0.0, radius], [-radius, 0.0], [0.0, -radius]]
            )
        else:
            X[1:, [0, 1]] = numpy.array(
                [
                    [
                        radius * numpy.cos(2 * numpy.pi * k / num_sections),
                        radius * numpy.sin(2 * numpy.pi * k / num_sections),
                    ]
                    for k in range(num_sections)
                ]
            )

        if R is not None:
            assert numpy.allclose(
                abs(numpy.linalg.eigvals(R)), numpy.ones(X.shape[1])
            ), "The transformation matrix doesn't preserve circles; at least one eigenvalue lies off the unit circle."
            X = numpy.dot(X, R.T)

        X += x0

        # Add Gmsh Points.
        p = [self.add_point(x, lcar=lcar) for x in X]

        # Define the circle arcs.
        arcs = [
            self.add_circle_arc(p[k], p[0], p[k + 1]) for k in range(1, len(p) - 1)
        ] + [self.add_circle_arc(p[-1], p[0], p[1])]

        if compound:
            self._COMPOUND_ENTITIES.append((1, [arc._ID for arc in arcs]))

        curve_loop = self.add_curve_loop(arcs)

        if make_surface:
            plane_surface = self.add_plane_surface(curve_loop, holes)
            if compound:
                self._COMPOUND_ENTITIES.append((2, [plane_surface._ID]))
        else:
            plane_surface = None

        class Circle:
            def __init__(
                self,
                x0,
                radius,
                R,
                compound,
                num_sections,
                holes,
                curve_loop,
                plane_surface,
                lcar=None,
            ):
                self.x0 = x0
                self.radius = radius
                self.lcar = lcar
                self.R = R
                self.compound = compound
                self.num_sections = num_sections
                self.holes = holes
                self.curve_loop = curve_loop
                self.plane_surface = plane_surface
                return

        return Circle(
            x0,
            radius,
            R,
            compound,
            num_sections,
            holes,
            curve_loop,
            plane_surface,
            lcar=lcar,
        )

    def extrude(
        self,
        input_entity,
        translation_axis=None,
        rotation_axis=None,
        point_on_axis=None,
        angle=None,
        num_layers=None,
        heights=None,
        recombine=False,
    ):
        """Extrusion (translation + rotation) of any entity along a given
        translation_axis, around a given rotation_axis, about a given angle. If one of
        the entities is not provided, this method will produce only translation or
        rotation.
        """
        eid = input_entity._ID
        dim = input_entity.dimension

        assert dim is not None

        if isinstance(num_layers, int):
            num_layers = [num_layers]
        if num_layers is None:
            num_layers = []
            heights = []
        else:
            if heights is None:
                heights = []
            else:
                assert len(num_layers) == len(heights)

        if translation_axis is not None and rotation_axis is None:
            out_dim_tags = gmsh.model.geo.extrude(
                [(dim, eid)],
                translation_axis[0],
                translation_axis[1],
                translation_axis[2],
                numElements=num_layers,
                heights=heights,
                recombine=recombine,
            )
        elif translation_axis is None and rotation_axis is not None:
            assert angle < numpy.pi
            out_dim_tags = gmsh.model.geo.revolve(
                [(dim, eid)],
                point_on_axis[0],
                point_on_axis[1],
                point_on_axis[2],
                rotation_axis[0],
                rotation_axis[1],
                rotation_axis[2],
                angle,
                numElements=num_layers,
                heights=heights,
                recombine=recombine,
            )
        else:
            assert translation_axis is not None and rotation_axis is not None
            assert angle < numpy.pi
            out_dim_tags = gmsh.model.geo.twist(
                [(dim, eid)],
                point_on_axis[0],
                point_on_axis[1],
                point_on_axis[2],
                translation_axis[0],
                translation_axis[1],
                translation_axis[2],
                rotation_axis[0],
                rotation_axis[1],
                rotation_axis[2],
                angle,
                numElements=num_layers,
                heights=heights,
                recombine=recombine,
            )
        top = Dummy(*out_dim_tags[0])
        extruded = Dummy(*out_dim_tags[1])
        lateral = [Dummy(*e) for e in out_dim_tags[1:]]
        return top, extruded, lateral

    def add_boundary_layer(self, *args, **kwargs):
        layer = BoundaryLayer(*args, **kwargs)
        self._AFTER_SYNC_QUEUE.append(layer)
        return layer

    def set_background_mesh(self, *args, **kwargs):
        setter = SetBackgroundMesh(*args, **kwargs)
        self._AFTER_SYNC_QUEUE.append(setter)

    def add_raw_code(self, string_or_list):
        """Add raw Gmsh code."""
        if isinstance(string_or_list, str):
            self._GMSH_CODE.append(string_or_list)
        else:
            assert isinstance(string_or_list, list)
            for string in string_or_list:
                self._GMSH_CODE.append(string)

    def add_rectangle(
        self, xmin, xmax, ymin, ymax, z, lcar=None, holes=None, make_surface=True
    ):
        return self.add_polygon(
            [[xmin, ymin, z], [xmax, ymin, z], [xmax, ymax, z], [xmin, ymax, z]],
            lcar=lcar,
            holes=holes,
            make_surface=make_surface,
        )

    class Polygon:
        def __init__(self, points, lines, curve_loop, surface, lcar=None):
            self.points = points
            self.lines = lines
            self.num_edges = len(lines)
            self.curve_loop = curve_loop
            self.surface = surface
            self.lcar = lcar
            if surface is not None:
                self.id = self.surface.id
            self.dimension = 2

    def add_polygon(self, X, lcar=None, holes=None, make_surface=True):
        if holes is None:
            holes = []
        else:
            assert make_surface

        if isinstance(lcar, list):
            assert len(X) == len(lcar)
        else:
            lcar = len(X) * [lcar]

        # Create points.
        p = [self.add_point(x, lcar=l) for x, l in zip(X, lcar)]
        # Create lines
        lines = [self.add_line(p[k], p[k + 1]) for k in range(len(p) - 1)]
        lines.append(self.add_line(p[-1], p[0]))
        ll = self.add_curve_loop(lines)
        surface = self.add_plane_surface(ll, holes) if make_surface else None
        return self.Polygon(p, lines, ll, surface, lcar=lcar)

    def add_ellipsoid(self, x0, radii, lcar=None, with_volume=True, holes=None):
        """Creates an ellipsoid with radii around a given midpoint
        :math:`x_0`.
        """
        if holes is None:
            holes = []

        if holes:
            assert with_volume

        print(x0)
        print(radii)

        # Add points.
        p = [
            self.add_point(x0, lcar=lcar),
            self.add_point([x0[0] + radii[0], x0[1], x0[2]], lcar=lcar),
            self.add_point([x0[0], x0[1] + radii[1], x0[2]], lcar=lcar),
            self.add_point([x0[0], x0[1], x0[2] + radii[2]], lcar=lcar),
            self.add_point([x0[0] - radii[0], x0[1], x0[2]], lcar=lcar),
            self.add_point([x0[0], x0[1] - radii[1], x0[2]], lcar=lcar),
            self.add_point([x0[0], x0[1], x0[2] - radii[2]], lcar=lcar),
        ]
        # Add skeleton.
        # Alternative for circles:
        # `self.add_circle_arc(a, b, c)`
        c = [
            self.add_ellipse_arc(p[1], p[0], p[6], p[6]),
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
            self.add_curve_loop([c[4], c[9], c[3]]),
            self.add_curve_loop([c[8], -c[4], c[0]]),
            self.add_curve_loop([-c[9], c[5], c[2]]),
            self.add_curve_loop([-c[5], -c[8], c[1]]),
            # the other half
            self.add_curve_loop([c[7], -c[3], c[10]]),
            self.add_curve_loop([-c[11], c[7], c[0]]),
            self.add_curve_loop([-c[10], -c[2], c[6]]),
            self.add_curve_loop([c[1], c[6], c[11]]),
        ]
        # Create a surface for each line loop.
        print()
        for pp in p:
            print(pp)
        print()
        for cc in c:
            print(cc)
        print()
        for l in ll:
            print(l)
            self.add_surface(l)

        exit(1)
        s = [self.add_surface(l) for l in ll]

        # Combine the surfaces to avoid seams
        if self._gmsh_major() == 3:
            s = [self.add_compound_surface(s[:4]), self.add_compound_surface(s[4:])]
        else:
            assert self._gmsh_major() == 4
            # <https://gitlab.onelab.info/gmsh/gmsh/issues/507>
            self.add_raw_code(
                "Compound Surface{{{}}};".format(",".join([surf.id for surf in s[:4]]))
            )
            self.add_raw_code(
                "Compound Surface{{{}}};".format(",".join([surf.id for surf in s[4:]]))
            )

        # Create the surface loop.
        surface_loop = self.add_surface_loop(s)
        # if holes:
        #     # Create an array of surface loops; the first entry is the outer
        #     # surface loop, the following ones are holes.
        #     surface_loop = self.add_array([surface_loop] + holes)
        # Create volume.
        volume = self.add_volume(surface_loop, holes) if with_volume else None

        class Ellipsoid:
            dimension = 3

            def __init__(self, x0, radii, surface_loop, volume, lcar=None):
                self.x0 = x0
                self.lcar = lcar
                self.radii = radii
                self.surface_loop = surface_loop
                self.volume = volume
                return

        return Ellipsoid(x0, radii, surface_loop, volume, lcar=lcar)

    def add_ball(self, x0, radius, **kwargs):
        return self.add_ellipsoid(x0, [radius, radius, radius], **kwargs)

    def add_box(self, x0, x1, y0, y1, z0, z1, lcar=None, with_volume=True, holes=None):
        if holes is None:
            holes = []

        if holes:
            assert with_volume

        # Define corner points.
        p = [
            self.add_point([x1, y1, z1], lcar=lcar),
            self.add_point([x1, y1, z0], lcar=lcar),
            self.add_point([x1, y0, z1], lcar=lcar),
            self.add_point([x1, y0, z0], lcar=lcar),
            self.add_point([x0, y1, z1], lcar=lcar),
            self.add_point([x0, y1, z0], lcar=lcar),
            self.add_point([x0, y0, z1], lcar=lcar),
            self.add_point([x0, y0, z0], lcar=lcar),
        ]
        # Define edges.
        e = [
            self.add_line(p[0], p[1]),
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
        ll = [
            self.add_curve_loop([e[0], e[3], -e[5], -e[1]]),
            self.add_curve_loop([e[0], e[4], -e[8], -e[2]]),
            self.add_curve_loop([e[1], e[6], -e[9], -e[2]]),
            self.add_curve_loop([e[3], e[7], -e[10], -e[4]]),
            self.add_curve_loop([e[5], e[7], -e[11], -e[6]]),
            self.add_curve_loop([e[8], e[10], -e[11], -e[9]]),
        ]
        # Create a surface for each line loop.
        s = [self.add_surface(l) for l in ll]
        # Create the surface loop.
        surface_loop = self.add_surface_loop(s)

        # Create volume
        vol = self.add_volume(surface_loop, holes) if with_volume else None

        class Box:
            def __init__(self, x0, x1, y0, y1, z0, z1, surface_loop, volume, lcar=None):
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

        return Box(x0, x1, y0, y1, z0, z1, surface_loop, vol, lcar=lcar)

    def add_torus(
        self,
        irad,
        orad,
        lcar=None,
        R=numpy.eye(3),
        x0=numpy.array([0.0, 0.0, 0.0]),
        variant="extrude_lines",
    ):

        if variant == "extrude_lines":
            return self._add_torus_extrude_lines(irad, orad, lcar=lcar, R=R, x0=x0)
        assert variant == "extrude_circle"
        return self._add_torus_extrude_circle(irad, orad, lcar=lcar, R=R, x0=x0)

    def _add_torus_extrude_lines(
        self, irad, orad, lcar=None, R=numpy.eye(3), x0=numpy.array([0.0, 0.0, 0.0])
    ):
        """Create Gmsh code for the torus in the x-y plane under the coordinate
        transformation

        .. math::
            \\hat{x} = R x + x_0.

        :param irad: inner radius of the torus
        :param orad: outer radius of the torus
        """
        # Add circle
        x0t = numpy.dot(R, numpy.array([0.0, orad, 0.0]))
        # Get circles in y-z plane
        Rc = numpy.array([[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]])
        c = self.add_circle(x0 + x0t, irad, lcar=lcar, R=numpy.dot(R, Rc))

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
        previous = c.curve_loop.lines
        angle = 2 * numpy.pi / 3
        all_surfaces = []
        for i in range(3):
            for k, p in enumerate(previous):
                # ts1[] = Extrude {{0,0,1}, {0,0,0}, 2*Pi/3}{Line{tc1};};
                # ...
                top, surf, _ = self.extrude(
                    p,
                    rotation_axis=rot_axis,
                    point_on_axis=point_on_rot_axis,
                    angle=angle,
                )
                all_surfaces.append(surf)
                previous[k] = top

        # compound_surface = CompoundSurface(all_surfaces)

        surface_loop = self.add_surface_loop(all_surfaces)
        vol = self.add_volume(surface_loop)
        return vol

    def _add_torus_extrude_circle(
        self, irad, orad, lcar=None, R=numpy.eye(3), x0=numpy.array([0.0, 0.0, 0.0])
    ):
        """Create Gmsh code for the torus under the coordinate transformation

        .. math::
            \\hat{x} = R x + x_0.

        :param irad: inner radius of the torus
        :param orad: outer radius of the torus
        """
        # Add circle
        x0t = numpy.dot(R, numpy.array([0.0, orad, 0.0]))
        Rc = numpy.array([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        c = self.add_circle(x0 + x0t, irad, lcar=lcar, R=numpy.dot(R, Rc))

        rot_axis = [0.0, 0.0, 1.0]
        rot_axis = numpy.dot(R, rot_axis)
        point_on_rot_axis = [0.0, 0.0, 0.0]
        point_on_rot_axis = numpy.dot(R, point_on_rot_axis) + x0

        # Form the torus by extruding the circle three times by 2/3*pi. This
        # works around the inability of Gmsh to extrude by pi or more. The
        # Extrude() macro returns an array; the first [0] entry in the array is
        # the entity that has been extruded at the far end. This can be used
        # for the following Extrude() step.  The second [1] entry of the array
        # is the surface that was created by the extrusion. The third [2-end]
        # is a list of all the planes of the lateral surface.
        previous = c.plane_surface
        all_volumes = []
        num_steps = 3
        for _ in range(num_steps):
            top, vol, _ = self.extrude(
                previous,
                rotation_axis=rot_axis,
                point_on_axis=point_on_rot_axis,
                angle=2 * numpy.pi / num_steps,
            )
            previous = top
            all_volumes.append(vol)

        assert self._gmsh_major() == 4
        self._COMPOUND_ENTITIES.append((3, [v._ID for v in all_volumes]))

    def add_pipe(
        self,
        outer_radius,
        inner_radius,
        length,
        R=numpy.eye(3),
        x0=numpy.array([0.0, 0.0, 0.0]),
        lcar=None,
        variant="rectangle_rotation",
    ):
        if variant == "rectangle_rotation":
            return self._add_pipe_by_rectangle_rotation(
                outer_radius, inner_radius, length, R=R, x0=x0, lcar=lcar
            )
        assert variant == "circle_extrusion"
        return self._add_pipe_by_circle_extrusion(
            outer_radius, inner_radius, length, R=R, x0=x0, lcar=lcar
        )

    def _add_pipe_by_rectangle_rotation(
        self,
        outer_radius,
        inner_radius,
        length,
        R=numpy.eye(3),
        x0=numpy.array([0.0, 0.0, 0.0]),
        lcar=None,
    ):
        """Hollow cylinder.
        Define a rectangle, extrude it by rotation.
        """
        X = numpy.array(
            [
                [0.0, outer_radius, -0.5 * length],
                [0.0, outer_radius, +0.5 * length],
                [0.0, inner_radius, +0.5 * length],
                [0.0, inner_radius, -0.5 * length],
            ]
        )
        # Apply transformation.
        X = [numpy.dot(R, x) + x0 for x in X]
        # Create points set.
        p = [self.add_point(x, lcar=lcar) for x in X]

        # Define edges.
        e = [
            self.add_line(p[0], p[1]),
            self.add_line(p[1], p[2]),
            self.add_line(p[2], p[3]),
            self.add_line(p[3], p[0]),
        ]

        rot_axis = [0.0, 0.0, 1.0]
        rot_axis = numpy.dot(R, rot_axis)
        point_on_rot_axis = [0.0, 0.0, 0.0]
        point_on_rot_axis = numpy.dot(R, point_on_rot_axis) + x0

        # Extrude all edges three times by 2*Pi/3.
        previous = e
        angle = 2 * numpy.pi / 3
        all_surfaces = []
        # com = []
        for i in range(3):
            for k, p in enumerate(previous):
                # ts1[] = Extrude {{0,0,1}, {0,0,0}, 2*Pi/3}{Line{tc1};};
                top, surf, _ = self.extrude(
                    p,
                    rotation_axis=rot_axis,
                    point_on_axis=point_on_rot_axis,
                    angle=angle,
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
        outer_radius,
        inner_radius,
        length,
        R=numpy.eye(3),
        x0=numpy.array([0.0, 0.0, 0.0]),
        lcar=None,
    ):
        """Hollow cylinder.
        Define a ring, extrude it by translation.
        """
        # Define ring which to Extrude by translation.
        Rc = numpy.array([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        c_inner = self.add_circle(
            x0, inner_radius, lcar=lcar, R=numpy.dot(R, Rc), make_surface=False
        )
        circ = self.add_circle(
            x0, outer_radius, lcar=lcar, R=numpy.dot(R, Rc), holes=[c_inner.curve_loop]
        )

        # Now Extrude the ring surface.
        _, vol, _ = self.extrude(
            circ.plane_surface, translation_axis=numpy.dot(R, [length, 0, 0])
        )
        return vol

    def translate(self, input_entity, vector):
        """Translates input_entity itself by vector.

        Changes the input object.
        """
        d = {1: "Line", 2: "Surface", 3: "Volume"}
        self._GMSH_CODE.append(
            "Translate {{{}}} {{ {}{{{}}}; }}".format(
                ", ".join([str(co) for co in vector]),
                d[input_entity.dimension],
                input_entity.id,
            )
        )
        return

    def rotate(self, input_entity, point, angle, axis):
        """Rotate input_entity around a given point with a give angle.
           Rotation axis has to be specified.

        Changes the input object.
        """
        d = {1: "Line", 2: "Surface", 3: "Volume"}
        self._GMSH_CODE.append(
            "Rotate {{ {{{}}},  {{{}}}, {}  }} {{{}{{{}}}; }}".format(
                ", ".join([str(ax) for ax in axis]),
                ", ".join([str(p) for p in point]),
                angle,
                d[input_entity.dimension],
                input_entity.id,
            )
        )

        return

    def symmetry(self, input_entity, coefficients, duplicate=True):
        """Transforms all elementary entities symmetrically to a plane. The vector
        should contain four expressions giving the coefficients of the plane's equation.
        """
        d = {1: "Line", 2: "Surface", 3: "Volume"}
        entity = "{}{{{}}};".format(d[input_entity.dimension], input_entity.id)

        if duplicate:
            entity = f"Duplicata{{{entity}}}"

        self._GMSH_CODE.append(
            "Symmetry {{{}}} {{{}}}".format(
                ", ".join([str(co) for co in coefficients]), entity
            )
        )
        return

    def in_surface(self, input_entity, surface):
        """Embed the point(s) or curve(s) in the given surface. The surface mesh
        will conform to the mesh of the point(s) or curves(s).
        """
        d = {0: "Point", 1: "Line"}
        entity = "{}{{{}}}".format(d[input_entity.dimension], input_entity.id)

        self._GMSH_CODE.append(f"{entity} In Surface{{{surface.id}}};")
        return

    def in_volume(self, input_entity, volume):
        """Embed the point(s)/curve(s)/surface(s) in the given volume. The volume mesh
        will conform to the mesh of the input entities.
        """
        d = {0: "Point", 1: "Line", 2: "Surface"}
        entity = "{}{{{}}}".format(d[input_entity.dimension], input_entity.id)

        self._GMSH_CODE.append(f"{entity} In Volume{{{volume.id}}};")
        return


class BoundaryLayer:
    def __init__(
        self,
        lcmin,
        lcmax,
        distmin,
        distmax,
        edges_list=None,
        faces_list=None,
        nodes_list=None,
    ):
        self.lcmin = lcmin
        self.lcmax = lcmax
        self.distmin = distmin
        self.distmax = distmax
        # Don't use [] as default argument, cf.
        # <https://stackoverflow.com/a/113198/353337>
        self.edges_list = edges_list if edges_list else []
        self.faces_list = faces_list if faces_list else []
        self.nodes_list = nodes_list if nodes_list else []

    def exec(self):
        tag1 = gmsh.model.mesh.field.add("Distance")

        if self.edges_list:
            gmsh.model.mesh.field.setNumbers(
                tag1, "EdgesList", [e._ID for e in self.edges_list]
            )
            # edge nodes must be specified, too, cf.
            # <https://gitlab.onelab.info/gmsh/gmsh/-/issues/812#note_9454>
            nodes = list(set([p for e in self.edges_list for p in e.points]))
            gmsh.model.mesh.field.setNumbers(tag1, "NodesList", [n._ID for n in nodes])
        if self.faces_list:
            gmsh.model.mesh.field.setNumbers(
                tag1, "FacesList", [f._ID for f in self.faces_list]
            )
        if self.nodes_list:
            gmsh.model.mesh.field.setNumbers(
                tag1, "NodesList", [n._ID for n in self.nodes_list]
            )

        tag2 = gmsh.model.mesh.field.add("Threshold")
        gmsh.model.mesh.field.setNumber(tag2, "IField", tag1)
        gmsh.model.mesh.field.setNumber(tag2, "LcMin", self.lcmin)
        gmsh.model.mesh.field.setNumber(tag2, "LcMax", self.lcmax)
        gmsh.model.mesh.field.setNumber(tag2, "DistMin", self.distmin)
        gmsh.model.mesh.field.setNumber(tag2, "DistMax", self.distmax)
        self.tag = tag2


class SetBackgroundMesh:
    def __init__(self, fields, operator="Min"):
        self.fields = fields
        self.operator = operator

    def exec(self):
        tag = gmsh.model.mesh.field.add(self.operator)
        gmsh.model.mesh.field.setNumbers(
            tag, "FieldsList", [f.tag for f in self.fields]
        )
        gmsh.model.mesh.field.setAsBackgroundMesh(tag)
