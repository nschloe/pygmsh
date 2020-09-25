import gmsh

from .. import common
from .ball import Ball
from .boolean import Boolean
from .box import Box
from .cone import Cone
from .cylinder import Cylinder
from .disk import Disk
from .rectangle import Rectangle
from .torus import Torus
from .wedge import Wedge


class Geometry(common.CommonGeometry):
    def __init__(self):
        super().__init__(gmsh.model.occ)
        self._AFTER_SYNC_QUEUE = []
        self._EMBED_QUEUE = []
        self._COMPOUND_ENTITIES = []
        self._RECOMBINE_ENTITIES = []
        self._TRANSFINITE_CURVE_QUEUE = []
        self._TRANSFINITE_SURFACE_QUEUE = []
        self._SIZE_QUEUE = []

    def __exit__(self, *a):
        # TODO remove once gmsh 4.7.0 is out
        # <https://gitlab.onelab.info/gmsh/gmsh/-/issues/1001>
        gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.0)
        gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 1.0e22)
        gmsh.finalize()

    @property
    def characteristic_length_min(self):
        return gmsh.option.getNumber("Mesh.CharacteristicLengthMin")

    @property
    def characteristic_length_max(self):
        return gmsh.option.getNumber("Mesh.CharacteristicLengthMax")

    @characteristic_length_min.setter
    def characteristic_length_min(self, val):
        gmsh.option.setNumber("Mesh.CharacteristicLengthMin", val)

    @characteristic_length_max.setter
    def characteristic_length_max(self, val):
        gmsh.option.setNumber("Mesh.CharacteristicLengthMax", val)

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

    def boolean_difference(self, d0, d1, delete_first=True, delete_other=True):
        """Boolean difference, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        """
        out, _ = gmsh.model.occ.cut(
            d0.dim_tags,
            d1.dim_tags,
            removeObject=delete_first,
            removeTool=delete_other,
        )
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

    def add_physical(self, entities, label=None):
        if not isinstance(entities, list):
            entities = [entities]

        dim = entities[0].dimension
        for e in entities:
            assert e.dimension == dim

        tag = gmsh.model.addPhysicalGroup(dim, [e._ID for e in entities])
        if label is not None:
            assert isinstance(label, str)
            gmsh.model.setPhysicalName(dim, tag, label)

    def add_polygon(self, X, mesh_size=None, holes=None, make_surface=True):
        class Polygon:
            def __init__(self, points, lines, curve_loop, surface, mesh_size=None):
                self.points = points
                self.lines = lines
                self.num_edges = len(lines)
                self.curve_loop = curve_loop
                self.surface = surface
                self.mesh_size = mesh_size
                if surface is not None:
                    self._ID = self.surface._ID
                self.dimension = 2
                self.dim_tags = [(2, surface)]

        if holes is None:
            holes = []
        else:
            assert make_surface

        if isinstance(mesh_size, list):
            assert len(X) == len(mesh_size)
        else:
            mesh_size = len(X) * [mesh_size]

        # Create points.
        p = [self.add_point(x, mesh_size=l) for x, l in zip(X, mesh_size)]
        # Create lines
        lines = [self.add_line(p[k], p[k + 1]) for k in range(len(p) - 1)]
        lines.append(self.add_line(p[-1], p[0]))
        ll = self.add_curve_loop(lines)
        surface = self.add_plane_surface(ll, holes) if make_surface else None
        return Polygon(p, lines, ll, surface, mesh_size=mesh_size)
