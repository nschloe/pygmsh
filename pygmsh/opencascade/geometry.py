# -*- coding: utf-8 -*-
#
from ..__about__ import __version__
from ..helpers import get_gmsh_major_version

from .rectangle import Rectangle


class Geometry(object):
    def __init__(
            self,
            characteristic_length_min=None,
            characteristic_length_max=None
            ):
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

    # # pylint: disable=too-many-branches
    # def _boolean_operation(
    #         self,
    #         operation,
    #         input_entity,
    #         tool_entity,
    #         delete=True
    #         ):
    #     '''Boolean operations, see
    #     http://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
    #     and tool_entity are called object and tool in gmsh documentation.
    #     '''
    #     assert self._FACTORY_TYPE == 'OpenCASCADE', \
    #         'Boolean operations are supported only ' \
    #         'with the OpenCASCADE factory.'
    #     self._BOOLEAN_ID += 1

    #     shape_type = None
    #     entities = []
    #     for ie in input_entity:
    #         if isinstance(ie, LineBase):
    #             shape_type = 'Line'
    #             entities.append(Dummy('{}'.format(ie.id)))
    #         elif isinstance(ie, SurfaceBase):
    #             shape_type = 'Surface'
    #             entities.append(Dummy('{}'.format(ie.id)))
    #         elif hasattr(ie, 'surface'):
    #             shape_type = 'Surface'
    #             entities.append(Dummy('{}'.format(ie.surface.id)))
    #         else:
    #             assert isinstance(ie, VolumeBase), \
    #                 'Illegal input entity ({}) ' \
    #                 'for Boolean operation.'.format(type(ie))
    #             shape_type = 'Volume'
    #             entities.append(Dummy('{}'.format(ie.id)))

    #     tools = []
    #     for te in tool_entity:
    #         if isinstance(te, LineBase):
    #             tools.append(Dummy('{}'.format(te.id)))
    #         elif isinstance(te, SurfaceBase):
    #             tools.append(Dummy('{}'.format(te.id)))
    #         elif hasattr(te, 'surface'):
    #             tools.append(Dummy('{}'.format(te.surface.id)))
    #         else:
    #             assert isinstance(te, VolumeBase), \
    #                 'Illegal tool entity ({}) ' \
    #                 'for Boolean operation.'.format(type(te))
    #             tools.append(Dummy('{}'.format(te.id)))

    #     # out[] = BooleanDifference { boolean-list } { boolean-list }
    #     name = 'bo{}'.format(self._BOOLEAN_ID)
    #     self._GMSH_CODE.append(
    #         '{}[] = {}{{{} {{{}}}; {}}} {{{} {{{}}}; {}}};'
    #         .format(
    #             name,
    #             operation,
    #             shape_type,
    #             ','.join(e.id for e in entities),
    #             'Delete;' if delete else '',
    #             shape_type,
    #             ','.join(e.id for e in tools),
    #             'Delete;' if delete else ''
    #         ))

    #     # currently only the new generated objects can be retrieved
    #     shapes = []
    #     for i, entity in enumerate(input_entity):
    #         shape = '{}[{}]'.format(name, i)

    #         if isinstance(entity, LineBase):
    #             shapes.append(LineBase(shape))
    #         elif isinstance(entity, SurfaceBase):
    #             shapes.append(SurfaceBase(shape))
    #         else:
    #             shapes.append(VolumeBase(shape))

    #     return shapes

    # def boolean_intersection(self, *args, **kwargs):
    #     '''Boolean intersection, see
    #     http://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
    #     and tool_entity are called object and tool in gmsh documentation.
    #     '''
    #     return self._boolean_operation('BooleanIntersection', *args, **kwargs)

    # def boolean_union(self, *args, **kwargs):
    #     '''Boolean union, see http://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations
    #     input_entity and tool_entity are called object and tool in gmsh
    #     documentation.
    #     '''
    #     return self._boolean_operation('BooleanUnion', *args, **kwargs)

    # def boolean_difference(self, *args, **kwargs):
    #     '''Boolean difference, see
    #     http://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
    #     and tool_entity are called object and tool in gmsh documentation.
    #     '''
    #     return self._boolean_operation('BooleanDifference', *args, **kwargs)

    # def boolean_fragments(self, *args, **kwargs):
    #     '''Boolean fragments, see
    #     http://gmsh.info/doc/texinfo/gmsh.html#Boolean-operations input_entity
    #     and tool_entity are called object and tool in gmsh documentation.
    #     '''
    #     return self._boolean_operation('BooleanFragments', *args, **kwargs)
