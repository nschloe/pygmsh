import math

import gmsh
import meshio
import numpy

from .bspline import BSpline
from .circle_arc import CircleArc
from .curve_loop import CurveLoop
from .dummy import Dummy
from .ellipse_arc import EllipseArc
from .line import Line
from .plane_surface import PlaneSurface
from .point import Point
from .polygon import Polygon
from .spline import Spline
from .surface import Surface
from .surface_loop import SurfaceLoop
from .volume import Volume


class CommonGeometry:
    """Geometry base class containing all methods that can be shared between built-in
    and occ.
    """

    def __init__(self, env):
        self.env = env
        self._BOOLEAN_ID = 0
        self._ARRAY_ID = 0
        self._FIELD_ID = 0
        self._TAKEN_PHYSICALGROUP_IDS = []
        self._COMPOUND_ENTITIES = []
        self._RECOMBINE_ENTITIES = []
        self._EMBED_QUEUE = []
        self._TRANSFINITE_CURVE_QUEUE = []
        self._TRANSFINITE_SURFACE_QUEUE = []
        self._TRANSFINITE_VOLUME_QUEUE = []
        self._AFTER_SYNC_QUEUE = []
        self._SIZE_QUEUE = []

    def __enter__(self):
        gmsh.initialize()
        gmsh.model.add("pygmsh model")
        return self

    def __exit__(self, *a):
        gmsh.finalize()

    def synchronize(self):
        self.env.synchronize()

    def __repr__(self):
        return "<pygmsh Geometry object>"

    def add_bspline(self, *args, **kwargs):
        return BSpline(self.env, *args, **kwargs)

    def add_circle_arc(self, *args, **kwargs):
        return CircleArc(self.env, *args, **kwargs)

    def add_ellipse_arc(self, *args, **kwargs):
        return EllipseArc(self.env, *args, **kwargs)

    def add_line(self, *args, **kwargs):
        return Line(self.env, *args, **kwargs)

    def add_curve_loop(self, *args, **kwargs):
        return CurveLoop(self.env, *args, **kwargs)

    def add_plane_surface(self, *args, **kwargs):
        return PlaneSurface(self.env, *args, **kwargs)

    def add_point(self, *args, **kwargs):
        return Point(self.env, *args, **kwargs)

    def add_spline(self, *args, **kwargs):
        return Spline(self.env, *args, **kwargs)

    def add_surface(self, *args, **kwargs):
        return Surface(self.env, *args, **kwargs)

    def add_surface_loop(self, *args, **kwargs):
        return SurfaceLoop(self.env, *args, **kwargs)

    def add_volume(self, *args, **kwargs):
        return Volume(self.env, *args, **kwargs)

    def add_polygon(self, *args, **kwargs):
        return Polygon(self, *args, **kwargs)

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

        dim = entities[0].dim
        for e in entities:
            assert e.dim == dim

        label = self._new_physical_group(label)
        tag = gmsh.model.addPhysicalGroup(dim, [e._ID for e in entities])
        if label is not None:
            gmsh.model.setPhysicalName(dim, tag, label)

    def set_transfinite_curve(self, curve, num_nodes, mesh_type, coeff):
        assert mesh_type in ["Progression", "Bulk"]
        self._TRANSFINITE_CURVE_QUEUE.append((curve._ID, num_nodes, mesh_type, coeff))

    def set_transfinite_surface(self, surface, arrangement, corner_tags):
        self._TRANSFINITE_SURFACE_QUEUE.append((surface._ID, arrangement, corner_tags))

    def set_transfinite_volume(self, volume, arrangement, corner_tags):
        self._TRANSFINITE_VOLUME_QUEUE.append((volume._ID, corner_tags))

    def set_recombined_surfaces(self, surfaces):
        for i, surface in enumerate(surfaces):
            assert isinstance(
                surface, (PlaneSurface, Surface)
            ), f"item {i} is not a surface"
        self._RECOMBINE_ENTITIES += [s.dim_tags[0] for s in surfaces]

    def extrude(
        self,
        input_entity,
        translation_axis,
        num_layers=None,
        heights=None,
        recombine=False,
    ):
        """Extrusion of any entity along a given translation_axis."""
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

        assert len(translation_axis) == 3

        out_dim_tags = self.env.extrude(
            input_entity.dim_tags,
            *translation_axis,
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
        """Rotation of any entity around a given rotation_axis, about a given angle."""
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
        assert len(point_on_axis) == 3
        assert len(rotation_axis) == 3
        out_dim_tags = self.env.revolve(
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

    def translate(self, obj, vector):
        """Translates input_entity itself by vector.

        Changes the input object.
        """
        self.env.translate(obj.dim_tags, *vector)

    def rotate(self, obj, point, angle, axis):
        """Rotate input_entity around a given point with a give angle.
           Rotation axis has to be specified.

        Changes the input object.
        """
        self.env.rotate(obj.dim_tags, *point, *axis, angle)

    def copy(self, obj):
        dim_tag = self.env.copy(obj.dim_tags)
        assert len(dim_tag) == 1
        return Dummy(*dim_tag[0])

    def symmetrize(self, obj, coefficients):
        """Transforms all elementary entities symmetrically to a plane. The vector
        should contain four expressions giving the coefficients of the plane's equation.
        """
        self.env.symmetrize(obj.dim_tags, *coefficients)

    def dilate(self, obj, x0, abc):
        self.env.dilate(obj.dim_tags, *x0, *abc)

    def mirror(self, obj, abcd):
        self.env.mirror(obj.dim_tags, *abcd)

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

    def set_mesh_size_callback(self, fun):
        gmsh.model.mesh.setSizeCallback(fun)

    def generate_mesh(  # noqa: C901
        self,
        dim=3,
        order=None,
        prune_vertices=True,
        prune_z_0=False,
        remove_lower_dim_cells=False,
    ):
        """Return a meshio.Mesh, storing the mesh points, cells, and data, generated by
        Gmsh from the `self`.
        """
        self.synchronize()

        for item in self._AFTER_SYNC_QUEUE:
            item.exec()

        for item, host in self._EMBED_QUEUE:
            gmsh.model.mesh.embed(item.dim, [item._ID], host.dim, host._ID)

        # set compound entities after sync
        for c in self._COMPOUND_ENTITIES:
            gmsh.model.mesh.setCompound(*c)

        for s in self._RECOMBINE_ENTITIES:
            gmsh.model.mesh.setRecombine(*s)

        for t in self._TRANSFINITE_CURVE_QUEUE:
            gmsh.model.mesh.setTransfiniteCurve(*t)

        for t in self._TRANSFINITE_SURFACE_QUEUE:
            gmsh.model.mesh.setTransfiniteSurface(*t)

        for e in self._TRANSFINITE_VOLUME_QUEUE:
            gmsh.model.mesh.setTransfiniteVolume(*e)

        for item, size in self._SIZE_QUEUE:
            gmsh.model.mesh.setSize(
                gmsh.model.getBoundary(item.dim_tags, False, False, True), size
            )

        if order is not None:
            gmsh.model.mesh.setOrder(order)

        gmsh.model.mesh.generate(dim)

        # extract point coords
        idx, points, _ = gmsh.model.mesh.getNodes()
        points = points.reshape(-1, 3)
        idx -= 1
        srt = numpy.argsort(idx)
        assert numpy.all(idx[srt] == numpy.arange(len(idx)))
        points = points[srt]
        if prune_z_0 and numpy.all(numpy.abs(points[:, 2]) < 1.0e-13):
            points = points[:, :2]

        # extract cells
        elem_types, elem_tags, node_tags = gmsh.model.mesh.getElements()
        cells = []
        for elem_type, node_tags in zip(elem_types, node_tags):
            # `elementName', `dim', `order', `numNodes', `localNodeCoord',
            # `numPrimaryNodes'
            num_nodes_per_cell = gmsh.model.mesh.getElementProperties(elem_type)[3]
            meshio.gmsh.gmsh_to_meshio_type
            cells.append(
                meshio.CellBlock(
                    meshio.gmsh.gmsh_to_meshio_type[elem_type],
                    node_tags.reshape(-1, num_nodes_per_cell) - 1,
                )
            )

        # print("a", gmsh.model.getEntities())
        # grps = gmsh.model.getPhysicalGroups()
        # print("a", grps)
        # for dim, tag in grps:
        #     print("a", gmsh.model.getPhysicalName(dim, tag))
        #     ent = gmsh.model.getEntitiesForPhysicalGroup(dim, tag)
        #     print("a", ent)
        #     assert len(ent) == 1
        #     print("a", gmsh.model.mesh.getElements(dim, ent[0]))

        # make meshio mesh
        mesh = meshio.Mesh(points, cells)

        if remove_lower_dim_cells:
            # Only keep the cells of highest topological dimension; discard faces and
            # such.
            cells_2d = {"triangle", "quad"}
            cells_3d = {
                "tetra",
                "hexahedron",
                "wedge",
                "pyramid",
                "penta_prism",
                "hexa_prism",
            }
            if any(c.type in cells_3d for c in mesh.cells):
                keep_types = cells_3d
            elif any(c.type in cells_2d for c in mesh.cells):
                keep_types = cells_2d
            else:
                keep_types = set(cell_type for cell_type, _ in mesh.cells)

            for name, val in mesh.cell_data.items():
                mesh.cell_data[name] = [
                    d for d, c in zip(val, mesh.cells) if c[0] in keep_types
                ]
            mesh.cells = [c for c in mesh.cells if c[0] in keep_types]

        if prune_vertices:
            # Make sure to include only those vertices which belong to a cell.
            ncells = numpy.concatenate([numpy.concatenate(c) for _, c in mesh.cells])
            uvertices, uidx = numpy.unique(ncells, return_inverse=True)

            k = 0
            cells = []
            for key, cellblock in mesh.cells:
                n = numpy.prod(cellblock.shape)
                cells.append(
                    meshio.CellBlock(key, uidx[k : k + n].reshape(cellblock.shape))
                )
                k += n
            mesh.cells = cells

            mesh.points = mesh.points[uvertices]
            for key in mesh.point_data:
                mesh.point_data[key] = mesh.point_data[key][uvertices]

        return mesh
