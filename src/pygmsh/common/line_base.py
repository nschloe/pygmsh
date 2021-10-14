from __future__ import annotations

import copy


class LineBase:
    dim = 1

    def __init__(self, id0: int, points: list[int]):
        self._id = id0
        self.dim_tag = (1, self._id)
        self.dim_tags = [self.dim_tag]
        self.points = points

    def __neg__(self):
        neg_self = copy.deepcopy(self)
        neg_self._id = -self._id
        neg_self.points = self.points[::-1]
        return neg_self
