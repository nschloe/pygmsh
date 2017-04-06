# -*- coding: utf-8 -*-
#
from .__about__ import (
        __version__,
        __author__,
        __author_email__,
        __website__,
        )

from .geometry import Geometry
from .helper import *


import pipdated
if pipdated.needs_checking(__name__):
    print(pipdated.check(__name__, __version__))

__all__ = [
        'geometry',
        'helper'
        ]
