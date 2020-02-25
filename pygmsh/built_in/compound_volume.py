class CompoundVolume:
    """
    Creates a compound volume from several elementary volumes.
    When meshed, a compound volume will be reparametrized as a
    single volume, whose mesh can thus cross internal boundaries.

    Parameters
    ----------
    volumes : array-like[N]
        Contains the identification number of the elementary
        volumes that should be reparametrized as a single volume.
    """

    _ID = 0

    def __init__(self, volumes):
        self.volumes = volumes

        self.id = f"cv{CompoundVolume._ID}"
        CompoundVolume._ID += 1

        self.code = "\n".join(
            [
                f"{self.id} = newv;",
                "Compound Volume({}) = {{{}}};".format(
                    self.id, ",".join([v.id for v in volumes])
                ),
            ]
        )
        return
