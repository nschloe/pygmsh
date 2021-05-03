import gmsh


class BoundaryLayer:
    def __init__(
        self,
        lcmin,
        lcmax,
        distmin,
        distmax,
        edges_list=None,
        faces_list=None,
        nodes_list=None,
        num_points_per_curve=None,
    ):
        self.lcmin = lcmin
        self.lcmax = lcmax
        self.distmin = distmin
        self.distmax = distmax
        # Don't use [] as default argument, cf.
        # <https://stackoverflow.com/a/113198/353337>
        self.edges_list = edges_list if edges_list else []
        self.faces_list = faces_list if faces_list else []
        self.nodes_list = nodes_list if nodes_list else []
        self.num_points_per_curve = num_points_per_curve

    def exec(self):
        tag1 = gmsh.model.mesh.field.add("Distance")

        if self.edges_list:
            gmsh.model.mesh.field.setNumbers(
                tag1, "EdgesList", [e._id for e in self.edges_list]
            )
            # edge nodes must be specified, too, cf.
            # <https://gitlab.onelab.info/gmsh/gmsh/-/issues/812#note_9454>
            # nodes = list(set([p for e in self.edges_list for p in e.points]))
            # gmsh.model.mesh.field.setNumbers(tag1, "NodesList", [n._id for n in nodes])
        if self.faces_list:
            gmsh.model.mesh.field.setNumbers(
                tag1, "FacesList", [f._id for f in self.faces_list]
            )
        if self.nodes_list:
            gmsh.model.mesh.field.setNumbers(
                tag1, "NodesList", [n._id for n in self.nodes_list]
            )
        if self.num_points_per_curve:
            gmsh.model.mesh.field.setNumber(
                tag1, "NumPointsPerCurve", self.num_points_per_curve
            )

        tag2 = gmsh.model.mesh.field.add("Threshold")
        gmsh.model.mesh.field.setNumber(tag2, "IField", tag1)
        gmsh.model.mesh.field.setNumber(tag2, "LcMin", self.lcmin)
        gmsh.model.mesh.field.setNumber(tag2, "LcMax", self.lcmax)
        gmsh.model.mesh.field.setNumber(tag2, "DistMin", self.distmin)
        gmsh.model.mesh.field.setNumber(tag2, "DistMax", self.distmax)
        self.tag = tag2


class SetBackgroundMesh:
    def __init__(self, fields, operator):
        self.fields = fields
        self.operator = operator

    def exec(self):
        tag = gmsh.model.mesh.field.add(self.operator)
        gmsh.model.mesh.field.setNumbers(
            tag, "FieldsList", [f.tag for f in self.fields]
        )
        gmsh.model.mesh.field.setAsBackgroundMesh(tag)
