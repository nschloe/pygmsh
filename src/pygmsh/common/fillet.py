class Fillet:

    def __init__(self, env, volumeEntity, curveEntity, radii):  
        curveIds = []
        for curve in curveEntity:
          curveIds.append(curve._id)
          
        self._id = env.fillet(volumeEntity._id, curveIds, radii)
        self.dim_tag = (3, self._id)
        self.dim_tags = [self.dim_tag]