from ..__about__ import __version__
from ..built_in import geometry as bl
from .ball import Ball
from .box import Box
from .cone import Cone
from .cylinder import Cylinder
from .disk import Disk
from .ellipsoid import Ellipsoid
from .rectangle import Rectangle
from .surface_base import SurfaceBase
from .torus import Torus
from .volume_base import VolumeBase
from .wedge import Wedge


class Geometry(bl.Geometry):
    def __init__(self, characteristic_length_min=None, characteristic_length_max=None):
        super().__init__()
        self._BOOLEAN_ID = 0
        self._EXTRUDE_ID = 0
        self._GMSH_CODE = [
            f"// This code was created by pygmsh v{__version__}.",
            'SetFactory("OpenCASCADE");',
        ]

        if characteristic_length_min is not None:
            self._GMSH_CODE.append(
                f"Mesh.CharacteristicLengthMin = {characteristic_length_min};"
            )

        if characteristic_length_max is not None:
            self._GMSH_CODE.append(
                f"Mesh.CharacteristicLengthMax = {characteristic_length_max};"
            )
        return

    def get_code(self):
        """Returns properly formatted Gmsh code.
        """
        return "\n".join(self._GMSH_CODE)

    def add_rectangle(self, *args, **kwargs):
        p = Rectangle(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_disk(self, *args, **kwargs):
        p = Disk(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_ball(self, *args, **kwargs):
        p = Ball(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_box(self, *args, **kwargs):
        p = Box(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_cone(self, *args, **kwargs):
        p = Cone(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_cylinder(self, *args, **kwargs):
        p = Cylinder(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_ellipsoid(self, *args, **kwargs):
        p = Ellipsoid(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_torus(self, *args, **kwargs):
        p = Torus(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_wedge(self, *args, **kwargs):
        p = Wedge(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def _boolean_operation(
        self,
        operation,
        input_entities,
        tool_entities,
        delete_first=True,
        delete_other=True,
    ):
        """Boolean operations, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        """
        self._BOOLEAN_ID += 1

        # assert that all entities are of the same dimensionality
        dim = None
        legal_dim_types = {1: "Line", 2: "Surface", 3: "Volume"}
        for ldt in legal_dim_types:
            if input_entities[0].dimension == ldt:
                dim = ldt
                break
        assert dim is not None, "Illegal input type '{}' for Boolean operation.".format(
            type(input_entities[0])
        )
        for e in input_entities[1:] + tool_entities:
            assert (
                e.dimension == dim
            ), "Incompatible input type '{}' for Boolean operation.".format(type(e))

        name = f"bo{self._BOOLEAN_ID}"

        input_delete = "Delete;" if delete_first else ""

        tool_delete = "Delete;" if delete_other else ""

        legal_dim_type = legal_dim_types[dim]

        if input_entities:
            formatted_input_entities = (
                ";".join([f"{legal_dim_type}{{{e.id}}}" for e in input_entities]) + ";"
            )
        else:
            formatted_input_entities = ""

        if tool_entities:
            formatted_tool_entities = (
                ";".join([f"{legal_dim_type}{{{e.id}}}" for e in tool_entities]) + ";"
            )
        else:
            formatted_tool_entities = ""

        self._GMSH_CODE.append(
            # I wonder what this line does in Lisp. ;)
            # '{}[] = {}{{{} {{{}}}; {}}} {{{} {{{}}}; {}}};'
            # .format(
            #    name,
            #    operation,
            #    legal_dim_types[dim],
            #    ';'.join(e.id for e in input_entities),
            #    'Delete;' if delete_first else '',
            #    legal_dim_types[dim],
            #    ';'.join(e.id for e in tool_entities),
            #    'Delete;' if delete_other else ''
            #    ))
            "%(name)s[] = %(op)s{ %(ientities)s %(idelete)s } { %(tentities)s %(tdelete)s};"
            % {
                "name": name,
                "op": operation,
                "ientities": formatted_input_entities,
                "idelete": input_delete,
                "tentities": formatted_tool_entities,
                "tdelete": tool_delete,
            }
        )
        mapping = {"Line": None, "Surface": SurfaceBase, "Volume": VolumeBase}
        return mapping[legal_dim_types[dim]](id0=name, is_list=True)

    def boolean_intersection(self, entities, delete_first=True, delete_other=True):
        """Boolean intersection, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        """
        assert len(entities) > 1
        return self._boolean_operation(
            "BooleanIntersection",
            [entities[0]],
            entities[1:],
            delete_first=delete_first,
            delete_other=delete_other,
        )

    def boolean_union(self, entities, delete_first=True, delete_other=True):
        """Boolean union, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        """
        out = self._boolean_operation(
            "BooleanUnion",
            [entities[0]],
            entities[1:],
            delete_first=delete_first,
            delete_other=delete_other,
        )
        # Cannot add Compound Surface yet; see
        # <https://gitlab.onelab.info/gmsh/gmsh/issues/525>.
        # if compound:
        #     self._GMSH_CODE.append("Compound Surface {{{}}};".format(out.id))
        return out

    def boolean_difference(self, *args, **kwargs):
        """Boolean difference, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        """
        return self._boolean_operation("BooleanDifference", *args, **kwargs)

    def boolean_fragments(self, *args, **kwargs):
        """Boolean fragments, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        """
        return self._boolean_operation("BooleanFragments", *args, **kwargs)
