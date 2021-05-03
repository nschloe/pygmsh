import numpy as np


class Polygon:
    dim = 2

    def __init__(self, host, points, mesh_size=None, holes=None, make_surface=True):
        if holes is None:
            holes = []
        else:
            assert make_surface

        if isinstance(mesh_size, list):
            assert len(points) == len(mesh_size)
        else:
            mesh_size = len(points) * [mesh_size]

        points = np.asarray(points)
        if points.shape[1] == 2:
            points = np.column_stack([points, np.zeros_like(points[:, 0])])

        # Create points.
        self.points = [
            host.add_point(x, mesh_size=l) for x, l in zip(points, mesh_size)
        ]
        # Create lines
        self.curves = [
            host.add_line(self.points[k], self.points[k + 1])
            for k in range(len(self.points) - 1)
        ] + [host.add_line(self.points[-1], self.points[0])]

        self.lines = self.curves

        self.curve_loop = host.add_curve_loop(self.curves)
        # self.surface = host.add_plane_surface(ll, holes) if make_surface else None
        if make_surface:
            self.surface = host.add_plane_surface(self.curve_loop, holes)
            self.dim_tag = self.surface.dim_tag
            self.dim_tags = self.surface.dim_tags
            self._id = self.surface._id

    def __repr__(self):
        return "<pygmsh Polygon object>"
