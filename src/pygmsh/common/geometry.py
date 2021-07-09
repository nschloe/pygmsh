import warnings
from typing import List, Optional, Tuple, Union

import gmsh

from ..helpers import extract_to_meshio
from .bspline import BSpline
from .circle_arc import CircleArc
from .curve_loop import CurveLoop
from .dummy import Dummy
from .ellipse_arc import EllipseArc
from .line import Line
from .plane_surface import PlaneSurface
from .point import Point
from .polygon import Polygon
from .size_field import BoundaryLayer, SetBackgroundMesh
from .spline import Spline
from .surface import Surface
from .surface_loop import SurfaceLoop
from .volume import Volume


class CommonGeometry:
    """Geometry base class containing all methods that can be shared between built-in
    and occ.
    """

    def __init__(self, env, init_argv=None):
        self.env = env
        self.init_argv = init_argv
        self._COMPOUND_ENTITIES = []
        self._RECOMBINE_ENTITIES = []
        self._EMBED_QUEUE = []
        self._TRANSFINITE_CURVE_QUEUE = []
        self._TRANSFINITE_SURFACE_QUEUE = []
        self._TRANSFINITE_VOLUME_QUEUE = []
        self._AFTER_SYNC_QUEUE = []
        self._SIZE_QUEUE = []
        self._PHYSICAL_QUEUE = []
        self._OUTWARD_NORMALS = []

    def __enter__(self):
        gmsh.initialize([] if self.init_argv is None else self.init_argv)
        gmsh.model.add("pygmsh model")
        return self

    def __exit__(self, *a):
        try:
            # Gmsh >= 4.7.0
            # https://gitlab.onelab.info/gmsh/gmsh/-/issues/1036
            gmsh.model.mesh.removeSizeCallback()
        except AttributeError:
            pass
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

    def add_physical(self, entities, label: Optional[str] = None):
        if label in [label for _, label in self._PHYSICAL_QUEUE]:
            raise ValueError(f'Label "{label}" already exists.')

        if not isinstance(entities, list):
            entities = [entities]

        # make sure the dimensionality is the same for all entities
        dim = entities[0].dim
        for e in entities:
            assert e.dim == dim

        if label is None:
            # 2021-02-18
            warnings.warn(
                "Physical groups without label are deprecated. "
                'Use add_physical(entities, "dummy").'
            )
        else:
            if not isinstance(label, str):
                raise ValueError(f"Physical label must be string, not {type(label)}.")

        self._PHYSICAL_QUEUE.append((entities, label))

    def set_transfinite_curve(
        self, curve, num_nodes: int, mesh_type: str, coeff: float
    ):
        assert mesh_type in ["Progression", "Bump", "Beta"]
        self._TRANSFINITE_CURVE_QUEUE.append((curve._id, num_nodes, mesh_type, coeff))

    def set_transfinite_surface(self, surface, arrangement: str, corner_pts):
        corner_tags = [pt._id for pt in corner_pts]
        self._TRANSFINITE_SURFACE_QUEUE.append((surface._id, arrangement, corner_tags))

    def set_transfinite_volume(self, volume, corner_pts):
        corner_tags = [pt._id for pt in corner_pts]
        self._TRANSFINITE_VOLUME_QUEUE.append((volume._id, corner_tags))

    def set_recombined_surfaces(self, surfaces):
        for i, surface in enumerate(surfaces):
            assert surface.dim == 2, f"item {i} is not a surface"
        self._RECOMBINE_ENTITIES += [s.dim_tags[0] for s in surfaces]

    def extrude(
        self,
        input_entity,
        translation_axis: Tuple[float, float, float],
        num_layers: Optional[Union[int, List[int]]] = None,
        heights: Optional[List[float]] = None,
        recombine: bool = False,
    ):
        """Extrusion of any entity along a given translation_axis."""
        if isinstance(num_layers, int):
            num_layers = [num_layers]
        if num_layers is None:
            num_layers = []
            assert heights is None
            heights = []
        else:
            if heights is None:
                heights = []
            else:
                assert len(num_layers) == len(heights)

        assert len(translation_axis) == 3

        ie_list = input_entity if isinstance(input_entity, list) else [input_entity]

        out_dim_tags = self.env.extrude(
            [e.dim_tag for e in ie_list],
            *translation_axis,
            numElements=num_layers,
            heights=heights,
            recombine=recombine,
        )
        top = Dummy(*out_dim_tags[0])
        extruded = Dummy(*out_dim_tags[1])
        lateral = [Dummy(*e) for e in out_dim_tags[2:]]
        return top, extruded, lateral

    def _revolve(
        self,
        input_entity,
        rotation_axis: Tuple[float, float, float],
        point_on_axis: Tuple[float, float, float],
        angle: float,
        num_layers: Optional[Union[int, List[int]]] = None,
        heights: Optional[List[float]] = None,
        recombine: bool = False,
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

    def translate(self, obj, vector: Tuple[float, float, float]):
        """Translates input_entity itself by vector.

        Changes the input object.
        """
        self.env.translate(obj.dim_tags, *vector)

    def rotate(
        self,
        obj,
        point: Tuple[float, float, float],
        angle: float,
        axis: Tuple[float, float, float],
    ):
        """Rotate input_entity around a given point with a given angle.
           Rotation axis has to be specified.

        Changes the input object.
        """
        self.env.rotate(obj.dim_tags, *point, *axis, angle)

    def copy(self, obj):
        dim_tag = self.env.copy(obj.dim_tags)
        assert len(dim_tag) == 1
        return Dummy(*dim_tag[0])

    def symmetrize(self, obj, coefficients: Tuple[float, float, float, float]):
        """Transforms all elementary entities symmetrically to a plane. The vector
        should contain four expressions giving the coefficients of the plane's equation.
        """
        self.env.symmetrize(obj.dim_tags, *coefficients)

    def dilate(
        self, obj, x0: Tuple[float, float, float], abc: Tuple[float, float, float]
    ):
        self.env.dilate(obj.dim_tags, *x0, *abc)

    def mirror(self, obj, abcd: Tuple[float, float, float, float]):
        self.env.mirror(obj.dim_tags, *abcd)

    def remove(self, obj, recursive: bool = False):
        self.env.remove(obj.dim_tags, recursive=recursive)

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

    def set_mesh_size_callback(self, fun, ignore_other_mesh_sizes=True):
        gmsh.model.mesh.setSizeCallback(fun)
        #
        # If a mesh size is set from a function, ignore the mesh sizes from the
        # entities.
        #
        # From <http://gmsh.info/doc/texinfo/gmsh.html#t10>:
        # ```
        # To determine the size of mesh elements, Gmsh locally computes the minimum of
        #
        # 1) the size of the model bounding box;
        # 2) if `Mesh.CharacteristicLengthFromPoints' is set, the mesh size specified at
        #    geometrical points;
        # 3) if `Mesh.CharacteristicLengthFromCurvature' is set, the mesh size based on
        #    the curvature and `Mesh.MinimumElementsPerTwoPi';
        # 4) the background mesh field;
        # 5) any per-entity mesh size constraint.
        #
        # This value is then constrained in the interval
        # [`Mesh.CharacteristicLengthMin', `Mesh.CharacteristicLengthMax'] and
        # multiplied by `Mesh.CharacteristicLengthFactor'.  In addition, boundary mesh
        # sizes (on curves or surfaces) are interpolated inside the enclosed entity
        # (surface or volume, respectively) if the option
        # `Mesh.CharacteristicLengthExtendFromBoundary' is set (which is the case by
        # default).
        # ```
        if ignore_other_mesh_sizes:
            gmsh.option.setNumber("Mesh.CharacteristicLengthExtendFromBoundary", 0)
            gmsh.option.setNumber("Mesh.CharacteristicLengthFromPoints", 0)
            gmsh.option.setNumber("Mesh.CharacteristicLengthFromCurvature", 0)

    def add_boundary_layer(self, *args, **kwargs):
        layer = BoundaryLayer(*args, **kwargs)
        self._AFTER_SYNC_QUEUE.append(layer)
        return layer

    def set_background_mesh(self, *args, **kwargs):
        setter = SetBackgroundMesh(*args, **kwargs)
        self._AFTER_SYNC_QUEUE.append(setter)

    def generate_mesh(  # noqa: C901
        self,
        dim: int = 3,
        order: Optional[int] = None,
        # http://gmsh.info/doc/texinfo/gmsh.html#index-Mesh_002eAlgorithm
        algorithm: Optional[int] = None,
        verbose: bool = False,
    ):
        """Return a meshio.Mesh, storing the mesh points, cells, and data, generated by
        Gmsh from the `self`.
        """
        self.synchronize()

        for item in self._AFTER_SYNC_QUEUE:
            item.exec()

        for item, host in self._EMBED_QUEUE:
            gmsh.model.mesh.embed(item.dim, [item._id], host.dim, host._id)

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

        for entities, label in self._PHYSICAL_QUEUE:
            d = entities[0].dim
            assert all(e.dim == d for e in entities)
            tag = gmsh.model.addPhysicalGroup(d, [e._id for e in entities])
            if label is not None:
                gmsh.model.setPhysicalName(d, tag, label)

        for entity in self._OUTWARD_NORMALS:
            gmsh.model.mesh.setOutwardOrientation(entity.id)

        if order is not None:
            gmsh.model.mesh.setOrder(order)

        gmsh.option.setNumber("General.Terminal", 1 if verbose else 0)

        # set algorithm
        # http://gmsh.info/doc/texinfo/gmsh.html#index-Mesh_002eAlgorithm
        if algorithm:
            gmsh.option.setNumber("Mesh.Algorithm", algorithm)

        gmsh.model.mesh.generate(dim)

        return extract_to_meshio()

    def save_geometry(self, filename: str):
        # filename is typically a geo_unrolled or brep file
        self.synchronize()
        gmsh.write(filename)
