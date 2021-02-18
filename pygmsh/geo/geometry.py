import math
from typing import List, Optional, Union

import gmsh
import numpy as np

from .. import common
from .dummy import Dummy


class Circle:
    def __init__(
        self,
        x0: List[float],
        radius: float,
        R,
        compound,
        num_sections: int,
        holes,
        curve_loop,
        plane_surface,
        mesh_size: Optional[float] = None,
    ):
        self.x0 = x0
        self.radius = radius
        self.mesh_size = mesh_size
        self.R = R
        self.compound = compound
        self.num_sections = num_sections
        self.holes = holes
        self.curve_loop = curve_loop
        self.plane_surface = plane_surface


class Geometry(common.CommonGeometry):
    def __init__(self):
        super().__init__(gmsh.model.geo)

    def revolve(self, *args, **kwargs):
        if len(args) >= 4:
            angle = args[3]
        else:
            assert "angle" in kwargs
            angle = kwargs["angle"]

        assert angle < math.pi
        return super()._revolve(*args, **kwargs)

    def twist(
        self,
        input_entity,
        translation_axis: List[float],
        rotation_axis: List[float],
        point_on_axis: List[float],
        angle: float,
        num_layers: Optional[Union[int, List[int]]] = None,
        heights: Optional[List[float]] = None,
        recombine: bool = False,
    ):
        """Twist (translation + rotation) of any entity along a given translation_axis,
        around a given rotation_axis, about a given angle.
        """
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

        assert len(point_on_axis) == 3
        assert len(rotation_axis) == 3
        assert len(translation_axis) == 3
        assert angle < math.pi
        out_dim_tags = self.env.twist(
            input_entity.dim_tags,
            *point_on_axis,
            *translation_axis,
            *rotation_axis,
            angle,
            numElements=num_layers,
            heights=heights,
            recombine=recombine,
        )
        top = Dummy(*out_dim_tags[0])
        extruded = Dummy(*out_dim_tags[1])
        lateral = [Dummy(*e) for e in out_dim_tags[2:]]
        return top, extruded, lateral

    def add_circle(
        self,
        x0: List[float],
        radius: float,
        mesh_size: Optional[float] = None,
        R=None,
        compound=False,
        num_sections: int = 3,
        holes=None,
        make_surface: bool = True,
    ):
        """Add circle in the :math:`x`-:math:`y`-plane."""
        if holes is None:
            holes = []
        else:
            assert make_surface

        # Define points that make the circle (midpoint and the four cardinal
        # directions).
        X = np.zeros((num_sections + 1, len(x0)))
        if num_sections == 4:
            # For accuracy, the points are provided explicitly.
            X[1:, [0, 1]] = np.array(
                [[radius, 0.0], [0.0, radius], [-radius, 0.0], [0.0, -radius]]
            )
        else:
            X[1:, [0, 1]] = np.array(
                [
                    [
                        radius * np.cos(2 * np.pi * k / num_sections),
                        radius * np.sin(2 * np.pi * k / num_sections),
                    ]
                    for k in range(num_sections)
                ]
            )

        if R is not None:
            assert np.allclose(
                abs(np.linalg.eigvals(R)), np.ones(X.shape[1])
            ), "The transformation matrix doesn't preserve circles; at least one eigenvalue lies off the unit circle."
            X = np.dot(X, R.T)

        X += x0

        # Add Gmsh Points.
        p = [self.add_point(x, mesh_size=mesh_size) for x in X]

        # Define the circle arcs.
        arcs = [
            self.add_circle_arc(p[k], p[0], p[k + 1]) for k in range(1, len(p) - 1)
        ] + [self.add_circle_arc(p[-1], p[0], p[1])]

        if compound:
            self._COMPOUND_ENTITIES.append((1, [arc._id for arc in arcs]))

        curve_loop = self.add_curve_loop(arcs)

        if make_surface:
            plane_surface = self.add_plane_surface(curve_loop, holes)
            if compound:
                self._COMPOUND_ENTITIES.append((2, [plane_surface._id]))
        else:
            plane_surface = None

        return Circle(
            x0,
            radius,
            R,
            compound,
            num_sections,
            holes,
            curve_loop,
            plane_surface,
            mesh_size=mesh_size,
        )

    def add_boundary_layer(self, *args, **kwargs):
        layer = BoundaryLayer(*args, **kwargs)
        self._AFTER_SYNC_QUEUE.append(layer)
        return layer

    def set_background_mesh(self, *args, **kwargs):
        setter = SetBackgroundMesh(*args, **kwargs)
        self._AFTER_SYNC_QUEUE.append(setter)

    def add_rectangle(
        self,
        xmin: float,
        xmax: float,
        ymin: float,
        ymax: float,
        z: float,
        mesh_size: Optional[float] = None,
        holes=None,
        make_surface: bool = True,
    ):
        return self.add_polygon(
            [[xmin, ymin, z], [xmax, ymin, z], [xmax, ymax, z], [xmin, ymax, z]],
            mesh_size=mesh_size,
            holes=holes,
            make_surface=make_surface,
        )

    def add_ellipsoid(
        self,
        x0: List[float],
        radii: List[float],
        mesh_size: Optional[float] = None,
        with_volume: bool = True,
        holes=None,
    ):
        """Creates an ellipsoid with radii around a given midpoint :math:`x_0`."""
        if holes is None:
            holes = []

        if holes:
            assert with_volume

        # Add points.
        p = [
            self.add_point(x0, mesh_size=mesh_size),
            self.add_point([x0[0] + radii[0], x0[1], x0[2]], mesh_size=mesh_size),
            self.add_point([x0[0], x0[1] + radii[1], x0[2]], mesh_size=mesh_size),
            self.add_point([x0[0], x0[1], x0[2] + radii[2]], mesh_size=mesh_size),
            self.add_point([x0[0] - radii[0], x0[1], x0[2]], mesh_size=mesh_size),
            self.add_point([x0[0], x0[1] - radii[1], x0[2]], mesh_size=mesh_size),
            self.add_point([x0[0], x0[1], x0[2] - radii[2]], mesh_size=mesh_size),
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
        # Make sure the loops are oriented outwards!
        ll = [
            # one half
            self.add_curve_loop([c[4], c[9], c[3]]),
            self.add_curve_loop([c[8], -c[4], c[0]]),
            self.add_curve_loop([-c[9], c[5], c[2]]),
            self.add_curve_loop([-c[5], -c[8], c[1]]),
            # the other half
            self.add_curve_loop([c[7], -c[3], c[10]]),
            self.add_curve_loop([c[11], -c[0], -c[7]]),
            self.add_curve_loop([-c[10], -c[2], c[6]]),
            self.add_curve_loop([-c[1], -c[11], -c[6]]),
        ]

        # Create a surface for each line loop.
        s = [self.add_surface(l) for l in ll]

        # Combine the surfaces to avoid seams
        # <https://gitlab.onelab.info/gmsh/gmsh/issues/507>
        # Cannot enable those yet, <https://gitlab.onelab.info/gmsh/gmsh/-/issues/995>
        self._COMPOUND_ENTITIES.append((2, [surf._id for surf in s[:4]]))
        self._COMPOUND_ENTITIES.append((2, [surf._id for surf in s[4:]]))

        # Create the surface loop.
        surface_loop = self.add_surface_loop(s)
        # if holes:
        #     # Create an array of surface loops; the first entry is the outer
        #     # surface loop, the following ones are holes.
        #     surface_loop = self.add_array([surface_loop] + holes)
        # Create volume.
        volume = self.add_volume(surface_loop, holes) if with_volume else None

        class Ellipsoid:
            dim = 3

            def __init__(self, x0, radii, surface_loop, volume, mesh_size=None):
                self.x0 = x0
                self.mesh_size = mesh_size
                self.radii = radii
                self.surface_loop = surface_loop
                self.volume = volume
                return

        return Ellipsoid(x0, radii, surface_loop, volume, mesh_size=mesh_size)

    def add_ball(self, x0: List[float], radius: float, **kwargs):
        return self.add_ellipsoid(x0, [radius, radius, radius], **kwargs)

    def add_box(
        self,
        x0: float,
        x1: float,
        y0: float,
        y1: float,
        z0: float,
        z1: float,
        mesh_size: Optional[float] = None,
        with_volume: bool = True,
        holes=None,
    ):
        if holes is None:
            holes = []

        if holes:
            assert with_volume

        # Define corner points.
        p = [
            self.add_point([x1, y1, z1], mesh_size=mesh_size),
            self.add_point([x1, y1, z0], mesh_size=mesh_size),
            self.add_point([x1, y0, z1], mesh_size=mesh_size),
            self.add_point([x1, y0, z0], mesh_size=mesh_size),
            self.add_point([x0, y1, z1], mesh_size=mesh_size),
            self.add_point([x0, y1, z0], mesh_size=mesh_size),
            self.add_point([x0, y0, z1], mesh_size=mesh_size),
            self.add_point([x0, y0, z0], mesh_size=mesh_size),
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
            def __init__(
                self, x0, x1, y0, y1, z0, z1, surface_loop, volume, mesh_size=None
            ):
                self.x0 = x0
                self.x1 = x1
                self.y0 = y0
                self.y1 = y1
                self.z0 = z0
                self.z1 = z1
                self.mesh_size = mesh_size
                self.surface_loop = surface_loop
                self.volume = volume

        return Box(x0, x1, y0, y1, z0, z1, surface_loop, vol, mesh_size=mesh_size)

    def add_torus(
        self,
        irad: float,
        orad: float,
        mesh_size: Optional[float] = None,
        R=np.eye(3),
        x0=np.array([0.0, 0.0, 0.0]),
        variant: str = "extrude_lines",
    ):

        if variant == "extrude_lines":
            return self._add_torus_extrude_lines(
                irad, orad, mesh_size=mesh_size, R=R, x0=x0
            )
        assert variant == "extrude_circle"
        return self._add_torus_extrude_circle(
            irad, orad, mesh_size=mesh_size, R=R, x0=x0
        )

    def _add_torus_extrude_lines(
        self,
        irad: float,
        orad: float,
        mesh_size: float = None,
        R=np.eye(3),
        x0=np.array([0.0, 0.0, 0.0]),
    ):
        """Create Gmsh code for the torus in the x-y plane under the coordinate
        transformation

        .. math::
            \\hat{x} = R x + x_0.

        :param irad: inner radius of the torus
        :param orad: outer radius of the torus
        """
        # Add circle
        x0t = np.dot(R, np.array([0.0, orad, 0.0]))
        # Get circles in y-z plane
        Rc = np.array([[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]])
        c = self.add_circle(x0 + x0t, irad, mesh_size=mesh_size, R=np.dot(R, Rc))

        rot_axis = [0.0, 0.0, 1.0]
        rot_axis = np.dot(R, rot_axis)
        point_on_rot_axis = [0.0, 0.0, 0.0]
        point_on_rot_axis = np.dot(R, point_on_rot_axis) + x0

        # Form the torus by extruding the circle three times by 2/3*pi. This
        # works around the inability of Gmsh to extrude by pi or more. The
        # Extrude() macro returns an array; the first [0] entry in the array is
        # the entity that has been extruded at the far end. This can be used
        # for the following Extrude() step.  The second [1] entry of the array
        # is the surface that was created by the extrusion.
        previous = c.curve_loop.curves
        angle = 2 * np.pi / 3
        all_surfaces = []
        for _ in range(3):
            for k, p in enumerate(previous):
                # ts1[] = Extrude {{0,0,1}, {0,0,0}, 2*Pi/3}{Line{tc1};};
                # ...
                top, surf, _ = self.revolve(
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
        self,
        irad,
        orad,
        mesh_size=None,
        R=np.eye(3),
        x0=np.array([0.0, 0.0, 0.0]),
    ):
        """Create Gmsh code for the torus under the coordinate transformation

        .. math::
            \\hat{x} = R x + x_0.

        :param irad: inner radius of the torus
        :param orad: outer radius of the torus
        """
        # Add circle
        x0t = np.dot(R, np.array([0.0, orad, 0.0]))
        Rc = np.array([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        c = self.add_circle(x0 + x0t, irad, mesh_size=mesh_size, R=np.dot(R, Rc))

        rot_axis = [0.0, 0.0, 1.0]
        rot_axis = np.dot(R, rot_axis)
        point_on_rot_axis = [0.0, 0.0, 0.0]
        point_on_rot_axis = np.dot(R, point_on_rot_axis) + x0

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
            top, vol, _ = self.revolve(
                previous,
                rotation_axis=rot_axis,
                point_on_axis=point_on_rot_axis,
                angle=2 * np.pi / num_steps,
            )
            previous = top
            all_volumes.append(vol)

        assert int(gmsh.__version__.split(".")[0])
        self._COMPOUND_ENTITIES.append((3, [v._id for v in all_volumes]))

    def add_pipe(
        self,
        outer_radius,
        inner_radius,
        length,
        R=np.eye(3),
        x0=np.array([0.0, 0.0, 0.0]),
        mesh_size=None,
        variant="rectangle_rotation",
    ):
        if variant == "rectangle_rotation":
            return self._add_pipe_by_rectangle_rotation(
                outer_radius, inner_radius, length, R=R, x0=x0, mesh_size=mesh_size
            )
        assert variant == "circle_extrusion"
        return self._add_pipe_by_circle_extrusion(
            outer_radius, inner_radius, length, R=R, x0=x0, mesh_size=mesh_size
        )

    def _add_pipe_by_rectangle_rotation(
        self,
        outer_radius,
        inner_radius,
        length,
        R=np.eye(3),
        x0=np.array([0.0, 0.0, 0.0]),
        mesh_size=None,
    ):
        """Hollow cylinder.
        Define a rectangle, extrude it by rotation.
        """
        X = np.array(
            [
                [0.0, outer_radius, -0.5 * length],
                [0.0, outer_radius, +0.5 * length],
                [0.0, inner_radius, +0.5 * length],
                [0.0, inner_radius, -0.5 * length],
            ]
        )
        # Apply transformation.
        X = [np.dot(R, x) + x0 for x in X]
        # Create points set.
        p = [self.add_point(x, mesh_size=mesh_size) for x in X]

        # Define edges.
        e = [
            self.add_line(p[0], p[1]),
            self.add_line(p[1], p[2]),
            self.add_line(p[2], p[3]),
            self.add_line(p[3], p[0]),
        ]

        rot_axis = [0.0, 0.0, 1.0]
        rot_axis = np.dot(R, rot_axis)
        point_on_rot_axis = [0.0, 0.0, 0.0]
        point_on_rot_axis = np.dot(R, point_on_rot_axis) + x0

        # Extrude all edges three times by 2*Pi/3.
        previous = e
        angle = 2 * np.pi / 3
        all_surfaces = []
        # com = []
        for _ in range(3):
            for k, p in enumerate(previous):
                # ts1[] = Extrude {{0,0,1}, {0,0,0}, 2*Pi/3}{Line{tc1};};
                top, surf, _ = self.revolve(
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
        R=np.eye(3),
        x0=np.array([0.0, 0.0, 0.0]),
        mesh_size=None,
    ):
        """Hollow cylinder.
        Define a ring, extrude it by translation.
        """
        # Define ring which to Extrude by translation.
        Rc = np.array([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        c_inner = self.add_circle(
            x0,
            inner_radius,
            mesh_size=mesh_size,
            R=np.dot(R, Rc),
            make_surface=False,
        )
        circ = self.add_circle(
            x0,
            outer_radius,
            mesh_size=mesh_size,
            R=np.dot(R, Rc),
            holes=[c_inner.curve_loop],
        )

        # Now Extrude the ring surface.
        _, vol, _ = self.extrude(
            circ.plane_surface, translation_axis=np.dot(R, [length, 0, 0])
        )
        return vol

    def in_surface(self, input_entity, surface):
        """Embed the point(s) or curve(s) in the given surface. The surface mesh will
        conform to the mesh of the point(s) or curves(s).
        """
        self._EMBED_QUEUE.append((input_entity, surface))

    def in_volume(self, input_entity, volume):
        """Embed the point(s)/curve(s)/surface(s) in the given volume. The volume mesh
        will conform to the mesh of the input entities.
        """
        self._EMBED_QUEUE.append((input_entity, volume))


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
                tag1, "EdgesList", [e._id for e in self.edges_list]
            )
            # edge nodes must be specified, too, cf.
            # <https://gitlab.onelab.info/gmsh/gmsh/-/issues/812#note_9454>
            nodes = list(set([p for e in self.edges_list for p in e.points]))
            gmsh.model.mesh.field.setNumbers(tag1, "NodesList", [n._id for n in nodes])
        if self.faces_list:
            gmsh.model.mesh.field.setNumbers(
                tag1, "FacesList", [f._id for f in self.faces_list]
            )
        if self.nodes_list:
            gmsh.model.mesh.field.setNumbers(
                tag1, "NodesList", [n._id for n in self.nodes_list]
            )

        tag2 = gmsh.model.mesh.field.add("Threshold")
        gmsh.model.mesh.field.setNumber(tag2, "IField", tag1)
        gmsh.model.mesh.field.setNumber(tag2, "LcMin", self.lcmin)
        gmsh.model.mesh.field.setNumber(tag2, "LcMax", self.lcmax)
        gmsh.model.mesh.field.setNumber(tag2, "DistMin", self.distmin)
        gmsh.model.mesh.field.setNumber(tag2, "DistMax", self.distmax)
        self.tag = tag2


class SetBackgroundMesh:
    def __init__(self, fields, operator):
        self.fields = fields
        self.operator = operator

    def exec(self):
        tag = gmsh.model.mesh.field.add(self.operator)
        gmsh.model.mesh.field.setNumbers(
            tag, "FieldsList", [f.tag for f in self.fields]
        )
        gmsh.model.mesh.field.setAsBackgroundMesh(tag)
