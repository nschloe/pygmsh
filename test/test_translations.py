"""Test translation for all dimensions."""
import pygmsh

def translation1d():
    """Translation of a line."""
    geom = pygmsh.built_in.Geometry()
    points = []
    for array in [[1, 0, 0], [0, 0, 0], [0, 1, 0]]:
        points.append(geom.add_point(array, 0.5))
    circle = geom.add_circle_arc(*points)
    import os
    directory = os.path.dirname(__name__)
    filename = os.path.join(directory, "translate.geo")
    points, _, _, _, _ = pygmsh.generate_mesh(geom, geo_filename=filename)
    geom.translate(circle, [1.5, 0, 0])
    translated_points, _, _, _, _ = pygmsh.generate_mesh(geom, geo_filename=filename)
    #print(points)
    #print(translated_points)



def translation2d():
    """Translation of a surface object."""



def translation3d():
    """Translation of a volume object."""



if __name__ == "__main__":
    translation1d()
    translation2d()
    translation3d()
