# -*- coding: utf-8 -*-
#
from __future__ import print_function

import pipdated

from .__about__ import (
        __version__,
        __author__,
        __author_email__,
        __website__,
        )

from .geometry import Geometry
# pylint: disable=wildcard-import
from .helper import *


if pipdated.needs_checking(__name__):
    print(pipdated.check(__name__, __version__))

__all__ = [
        'geometry',
        'helper'
        ]
