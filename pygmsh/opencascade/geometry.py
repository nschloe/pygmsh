# -*- coding: utf-8 -*-
#
from ..__about__ import __version__
from ..helpers import get_gmsh_major_version

from .disk import Disk
from .rectangle import Rectangle
from .line_base import LineBase
from .surface_base import SurfaceBase
from .volume_base import VolumeBase


class Geometry(object):
    def __init__(
            self,
            characteristic_length_min=None,
            characteristic_length_max=None
            ):
        self._BOOLEAN_ID = 0
        self._GMSH_MAJOR = get_gmsh_major_version()
        self._GMSH_CODE = [
            '// This code was created by PyGmsh v{}.'.format(__version__),
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

    def get_gmsh_major(self):
        '''Return the major version of the gmsh executable.
        '''
        return self._GMSH_MAJOR

    def add_rectangle(self, *args, **kwargs):
        p = Rectangle(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    def add_disk(self, *args, **kwargs):
        p = Disk(*args, **kwargs)
        self._GMSH_CODE.append(p.code)
        return p

    # pylint: disable=too-many-branches
    def _boolean_operation(
            self,
            operation,
            input_entities,
            tool_entities,
            delete=True
            ):
        '''Boolean operations, see
        http://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        '''
        self._BOOLEAN_ID += 1

        # assert that all entities are of the same dimensionality
        dim_type = None
        legal_dim_types = {
            LineBase: 'Line',
            SurfaceBase: 'Surface',
            VolumeBase: 'Volume',
            }
        for ldt in legal_dim_types.keys():
            if isinstance(input_entities[0], ldt):
                dim_type = ldt
                break
        assert dim_type is not None, \
            'Illegal input type \'{}\' for Boolean operation.'.format(
                type(input_entities[0])
                )
        for e in input_entities[1:] + tool_entities:
            assert isinstance(e, dim_type), \
                'Incompatible input type \'{}\' for Boolean operation.'.format(
                    type(e)
                    )

        # shape_type = None
        # entities = []
        # for ie in input_entity:
        #     if isinstance(ie, LineBase):
        #         shape_type = 'Line'
        #         entities.append(Dummy('{}'.format(ie.id)))
        #     elif isinstance(ie, SurfaceBase):
        #         shape_type = 'Surface'
        #         entities.append(Dummy('{}'.format(ie.id)))
        #     elif hasattr(ie, 'surface'):
        #         shape_type = 'Surface'
        #         entities.append(Dummy('{}'.format(ie.surface.id)))
        #     else:
        #         assert isinstance(ie, VolumeBase), \
        #             'Illegal input entity ({}) ' \
        #             'for Boolean operation.'.format(type(ie))
        #         shape_type = 'Volume'
        #         entities.append(Dummy('{}'.format(ie.id)))

        # tools = []
        # for te in tool_entity:
        #     if isinstance(te, LineBase):
        #         tools.append(Dummy('{}'.format(te.id)))
        #     elif isinstance(te, SurfaceBase):
        #         tools.append(Dummy('{}'.format(te.id)))
        #     elif hasattr(te, 'surface'):
        #         tools.append(Dummy('{}'.format(te.surface.id)))
        #     else:
        #         assert isinstance(te, VolumeBase), \
        #             'Illegal tool entity ({}) ' \
        #             'for Boolean operation.'.format(type(te))
        #         tools.append(Dummy('{}'.format(te.id)))

        # out[] = BooleanDifference { boolean-list } { boolean-list }
        name = 'bo{}'.format(self._BOOLEAN_ID)
        self._GMSH_CODE.append(
            '{}[] = {}{{{} {{{}}}; {}}} {{{} {{{}}}; {}}};'
            .format(
                name,
                operation,
                legal_dim_types[dim_type],
                ','.join(e.id for e in input_entities),
                'Delete;' if delete else '',
                legal_dim_types[dim_type],
                ','.join(e.id for e in tool_entities),
                'Delete;' if delete else ''
                ))

        # # currently only the newly generated objects can be retrieved
        # shapes = []
        # for i, entity in enumerate(input_entity):
        #     shape = '{}[{}]'.format(name, i)

        #     if isinstance(entity, LineBase):
        #         shapes.append(LineBase(shape))
        #     elif isinstance(entity, SurfaceBase):
        #         shapes.append(SurfaceBase(shape))
        #     else:
        #         shapes.append(VolumeBase(shape))

        return  # shapes

    def boolean_intersection(self, entities, delete=True):
        '''Boolean intersection, see
        http://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        '''
        assert len(entities) > 1
        return self._boolean_operation(
                'BooleanIntersection',
                [entities[0]], entities[1:], delete=delete
                )

    def boolean_union(self, entities, delete=True):
        '''Boolean union, see http://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations
        input_entity and tool_entity are called object and tool in gmsh
        documentation.
        '''
        return self._boolean_operation(
                'BooleanUnion',
                [entities[0]], entities[1:], delete=delete
                )

    def boolean_difference(self, *args, **kwargs):
        '''Boolean difference, see
        http://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        '''
        return self._boolean_operation('BooleanDifference', *args, **kwargs)

    def boolean_fragments(self, *args, **kwargs):
        '''Boolean fragments, see
        http://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
        and tool_entity are called object and tool in gmsh documentation.
        '''
        return self._boolean_operation('BooleanFragments', *args, **kwargs)
