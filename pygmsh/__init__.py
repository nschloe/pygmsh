# -*- coding: utf-8 -*-
#
from pygmsh.geometry import Geometry
from pygmsh.helper import *

from pygmsh.__about__ import (
        __version__,
        __author__,
        __author_email__,
        __website__,
        )

import pipdated
if pipdated.needs_checking(__name__):
    print(pipdated.check(__name__, __version__))

__all__ = [
        'geometry',
        'helper'
        ]
