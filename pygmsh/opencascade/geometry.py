# -*- coding: utf-8 -*-
#
from ..__about__ import __version__

from .. import built_in

from .ball import Ball
from .box import Box
from .cone import Cone
from .cylinder import Cylinder
from .disk import Disk
from .dummy import Dummy
from .rectangle import Rectangle
from .surface_base import SurfaceBase
from .torus import Torus
from .wedge import Wedge
from .volume_base import VolumeBase
from ..built_in import geometry as bl


class Geometry(bl.Geometry):
    def __init__(
            self,
            characteristic_length_min=None,
            characteristic_length_max=None
            ):
        super(Geometry, self).__init__()
        self._BOOLEAN_ID = 0
        self._EXTRUDE_ID = 0
        self._GMSH_CODE = [
            '// This code was created by pygmsh v{}.'.format(__version__),
            'SetFactory("OpenCASCADE");',
            ]

        if characteristic_length_min is not None:
            self._GMSH_CODE.append(
                'Mesh.CharacteristicLengthMin = {};'.format(
                    characteristic_length_min
                    ))

        if characteristic_length_max is not None:
            self._GMSH_CODE.append(
                'Mesh.CharacteristicLengthMax = {};'.format(
                    characteristic_length_max
                    ))
        return

    def get_code(self):
        '''Returns properly formatted Gmsh code.
        '''
        return '\n'.join(self._GMSH_CODE)

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

    def add_torus(self, *args, **kwargs):
        p = Torus(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_wedge(self, *args, **kwargs):
        p = Wedge(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    # pylint: disable=too-many-branches
    def _boolean_operation(
            self,
            operation,
            input_entities,
            tool_entities,
            delete_first=True,
            delete_other=True
            ):
        '''Boolean operations, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        '''
        self._BOOLEAN_ID += 1

        # assert that all entities are of the same dimensionality
        dim = None
        legal_dim_types = {
            1: 'Line',
            2: 'Surface',
            3: 'Volume',
            }
        for ldt in legal_dim_types:
            if input_entities[0].dimension == ldt:
                dim = ldt
                break
        assert dim is not None, \
            'Illegal input type \'{}\' for Boolean operation.'.format(
                type(input_entities[0])
                )
        for e in input_entities[1:] + tool_entities:
            assert e.dimension == dim, \
                'Incompatible input type \'{}\' for Boolean operation.'.format(
                    type(e)
                    )

        name = 'bo{}'.format(self._BOOLEAN_ID)

        input_delete = 'Delete;' if delete_first else ''

        tool_delete = 'Delete;' if delete_other else ''

        legal_dim_type = legal_dim_types[dim]

        if input_entities:
            formatted_input_entities = ';'.join(["%s{%s}" %
                (legal_dim_type, e.id) for e in input_entities]) + ';'
        else:
            formatted_input_entities = ''

        if tool_entities:
            formatted_tool_entities = ';'.join(["%s{%s}" %
                (legal_dim_type, e.id) for e in tool_entities]) + ';'
        else:
            formatted_tool_entities = ''

        self._GMSH_CODE.append(
            # I wonder what this line does in Lisp.
            #'{}[] = {}{{{} {{{}}}; {}}} {{{} {{{}}}; {}}};'
            #.format(
            #    name,
            #    operation,
            #    legal_dim_types[dim],
            #    ';'.join(e.id for e in input_entities),
            #    'Delete;' if delete_first else '',
            #    legal_dim_types[dim],
            #    ';'.join(e.id for e in tool_entities),
            #    'Delete;' if delete_other else ''
            #    ))
            '%(name)s[] = %(op)s{ %(ientities)s %(idelete)s } { %(tentities)s %(tdelete)s};' % {
              'name' : name,
              'op' : operation,
              'ientities' : formatted_input_entities,
              'idelete'   : input_delete,
              'tentities' : formatted_tool_entities,
              'tdelete'   : tool_delete,
            }
          )
        mapping = {'Line': None, 'Surface': SurfaceBase, 'Volume': VolumeBase}
        return mapping[legal_dim_types[dim]](id0=name, is_list=True)

    def boolean_intersection(
            self, entities, delete_first=True, delete_other=True
            ):
        '''Boolean intersection, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        '''
        assert len(entities) > 1
        return self._boolean_operation(
                'BooleanIntersection',
                [entities[0]], entities[1:],
                delete_first=delete_first, delete_other=delete_other
                )

    def boolean_union(self, entities, delete_first=True, delete_other=True):
        '''Boolean union, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        '''
        return self._boolean_operation(
                'BooleanUnion',
                [entities[0]], entities[1:],
                delete_first=delete_first, delete_other=delete_other
                )

    def boolean_difference(self, *args, **kwargs):
        '''Boolean difference, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        '''
        return self._boolean_operation('BooleanDifference', *args, **kwargs)

    def boolean_fragments(self, *args, **kwargs):
        '''Boolean fragments, see
        https://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        '''
        return self._boolean_operation('BooleanFragments', *args, **kwargs)

    def extrude(
            self,
            input_entity,
            translation_axis
            ):
        '''Extrusion (translation + rotation) of any entity along a given
        translation_axis, around a given rotation_axis, about a given angle. If
        one of the entities is not provided, this method will produce only
        translation or rotation.
        '''
        self._EXTRUDE_ID += 1

        assert isinstance(input_entity, built_in.surface_base.SurfaceBase)
        entity = Dummy('Surface{{{}}}'.format(input_entity.id))

        # out[] = Extrude{0,1,0}{ Line{1}; };
        name = 'ex{}'.format(self._EXTRUDE_ID)

        # Only translation
        self._GMSH_CODE.append(
            '{}[] = Extrude{{{}}}{{{};}};'.format(
                name,
                ','.join(repr(x) for x in translation_axis),
                entity.id
            ))

        # From <https://www.manpagez.com/info/gmsh/gmsh-2.4.0/gmsh_66.php>:
        #
        # > In this last extrusion command we retrieved the volume number
        # > programatically by saving the output of the command into a
        # > list. This list will contain the "top" of the extruded surface (in
        # > out[0]) as well as the newly created volume (in out[1]).
        #
        top = '{}[0]'.format(name)
        extruded = '{}[1]'.format(name)

        top = SurfaceBase(top)
        extruded = VolumeBase(is_list=False, id0=extruded)

        return top, extruded
