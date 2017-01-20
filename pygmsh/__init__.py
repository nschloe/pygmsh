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
if pipdated.needs_checking('pygmsh'):
    msg = pipdated.check('pygmsh', __version__)
    if msg:
        print(msg)

__all__ = [
        'geometry',
        'helper'
        ]
