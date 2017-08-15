# -*- coding: utf-8 -*-
#
from __future__ import print_function


from .__about__ import (
        __version__,
        __author__,
        __author_email__,
        __website__,
        )

from .geometry import Geometry
# pylint: disable=wildcard-import
from .helper import *

try:
    import pipdate
except ImportError:
    pass
else:
    if pipdate.needs_checking(__name__):
        print(pipdate.check(__name__, __version__))

__all__ = [
        'geometry',
        'helper'
        ]
