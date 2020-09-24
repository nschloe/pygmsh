import math

import gmsh

from .ball import Ball
from .boolean import Boolean
from .box import Box
from .circle_arc import CircleArc
from .cone import Cone
from .curve_loop import CurveLoop
from .cylinder import Cylinder
from .disk import Disk
from .dummy import Dummy
from .line import Line
from .plane_surface import PlaneSurface
from .point import Point
from .rectangle import Rectangle
from .torus import Torus
from .wedge import Wedge


class Geometry:
    def __init__(self, characteristic_length_min=None, characteristic_length_max=None):
        self._AFTER_SYNC_QUEUE = []
        self._EMBED_QUEUE = []
        self._COMPOUND_ENTITIES = []
        self._RECOMBINE_ENTITIES = []
        self._TRANSFINITE_CURVE_QUEUE = []
        self._TRANSFINITE_SURFACE_QUEUE = []
        self._SIZE_QUEUE = []

        gmsh.initialize()

        if characteristic_length_min is not None:
            gmsh.option.setNumber(
                "Mesh.CharacteristicLengthMin", characteristic_length_min
            )

        if characteristic_length_max is not None:
            gmsh.option.setNumber(
                "Mesh.CharacteristicLengthMax", characteristic_length_max
            )

    def __del__(self):
        # TODO reset globally set values.
        # <https://gitlab.onelab.info/gmsh/gmsh/-/issues/1001>
        gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.0)
        gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 1.0e22)
        gmsh.finalize()

    def __repr__(self):
        return "<pygmsh Geometry object (OCC)>"

    def synchronize(self):
        gmsh.model.occ.synchronize()

    def add_point(self, *args, **kwargs):
        return Point(*args, **kwargs)

    def add_line(self, *args, **kwargs):
        return Line(*args, **kwargs)

    def add_circle_arc(self, *args, **kwargs):
        return CircleArc(*args, **kwargs)

    def add_curve_loop(self, *args, **kwargs):
        return CurveLoop(*args, **kwargs)

    def add_plane_surface(self, *args, **kwargs):
        return PlaneSurface(*args, **kwargs)

    def add_rectangle(self, *args, mesh_size=None, **kwargs):
        entity = Rectangle(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((entity, mesh_size))
        return entity

    def add_disk(self, *args, mesh_size=None, **kwargs):
        entity = Disk(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((entity, mesh_size))
        return entity

    def add_ball(self, *args, mesh_size=None, **kwargs):
        obj = Ball(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((obj, mesh_size))
        return obj

    def add_box(self, *args, mesh_size=None, **kwargs):
        box = Box(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((box, mesh_size))
        return box

    def add_cone(self, *args, mesh_size=None, **kwargs):
        cone = Cone(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((cone, mesh_size))
        return cone

    def add_cylinder(self, *args, mesh_size=None, **kwargs):
        cyl = Cylinder(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((cyl, mesh_size))
        return cyl

    def add_ellipsoid(self, center, radii, mesh_size=None):
        obj = Ball(center, 1.0)
        self.dilate(obj, center, radii)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((obj, mesh_size))
        return obj

    def add_torus(self, *args, mesh_size=None, **kwargs):
        obj = Torus(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((obj, mesh_size))
        return obj

    def add_wedge(self, *args, mesh_size=None, **kwargs):
        obj = Wedge(*args, **kwargs)
        if mesh_size is not None:
            self._SIZE_QUEUE.append((obj, mesh_size))
        return obj

    def boolean_intersection(self, entities):
        """Boolean intersection, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        """
        ent = entities[0].dim_tags
        # form subsequent intersections
        # https://gitlab.onelab.info/gmsh/gmsh/-/issues/999
        for e in entities[1:]:
            out, _ = gmsh.model.occ.intersect(
                [ent],
                [e.dim_tags],
                removeObject=True,
                removeTool=True,
            )
            assert all(out[0] == item for item in out)
            ent = out[0]
        return Boolean([ent], "Intersection")

    def boolean_union(self, entities):
        """Boolean union, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        """
        out, _ = gmsh.model.occ.fuse(
            [entities[0].dim_tags],
            [e.dim_tags for e in entities[1:]],
            removeObject=True,
            removeTool=True,
        )
        return Boolean(out, "Union")

    def boolean_difference(self, d0, d1):
        """Boolean difference, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        """
        out, _ = gmsh.model.occ.cut(d0.dim_tags, d1.dim_tags)
        return Boolean(out, "Difference")

    def boolean_fragments(self, d0, d1):
        """Boolean fragments, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        """
        out, _ = gmsh.model.occ.fragment(d0.dim_tags, d1.dim_tags)
        return Boolean(out, "Fragments")

    def translate(self, obj, vector):
        """Translates input_entity itself by vector.

        Changes the input object.
        """
        gmsh.model.occ.translate(obj.dim_tags, *vector)

    def rotate(self, obj, point, angle, axis):
        """Rotate input_entity around a given point with a give angle.
           Rotation axis has to be specified.

        Changes the input object.
        """
        gmsh.model.occ.rotate(obj.dim_tags, *point, *axis, angle)

    def symmetrize(self, obj, coefficients):
        """Transforms all elementary entities symmetrically to a plane. The vector
        should contain four expressions giving the coefficients of the plane's equation.
        """
        gmsh.model.occ.symmetrize(obj.dim_tags, *coefficients)

    def dilate(self, obj, x0, abc):
        gmsh.model.occ.dilate(obj.dim_tags, *x0, *abc)

    def extrude(
        self,
        input_entity,
        translation_axis,
        num_layers=None,
        heights=None,
        recombine=False,
    ):
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

        out_dim_tags = gmsh.model.occ.extrude(
            input_entity.dim_tags,
            translation_axis[0],
            translation_axis[1],
            translation_axis[2],
            numElements=num_layers,
            heights=heights,
            recombine=recombine,
        )
        top = Dummy(*out_dim_tags[0])
        extruded = Dummy(*out_dim_tags[1])
        lateral = [Dummy(*e) for e in out_dim_tags[2:]]
        return top, extruded, lateral

    def revolve(
        self,
        input_entity,
        rotation_axis,
        point_on_axis,
        angle,
        num_layers=None,
        heights=None,
        recombine=False,
    ):
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

        assert angle < math.pi
        out_dim_tags = gmsh.model.occ.revolve(
            input_entity.dim_tags,
            *point_on_axis,
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

    def twist(
        self,
        input_entity,
        translation_axis,
        rotation_axis,
        point_on_axis,
        angle,
        num_layers=None,
        heights=None,
        recombine=False,
    ):
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

        assert angle < math.pi
        out_dim_tags = gmsh.model.occ.twist(
            input_entity.dim_tags,
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
        lateral = [Dummy(*e) for e in out_dim_tags[2:]]
        return top, extruded, lateral
