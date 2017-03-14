# PyGmsh

[![Build Status](https://travis-ci.org/nschloe/pygmsh.svg)](https://travis-ci.org/nschloe/pygmsh)
[![Code Health](https://landscape.io/github/nschloe/pygmsh/master/landscape.png)](https://landscape.io/github/nschloe/pygmsh/master)
[![codecov](https://codecov.io/gh/nschloe/pygmsh/branch/master/graph/badge.svg)](https://codecov.io/gh/nschloe/pygmsh)
[![Documentation Status](https://readthedocs.org/projects/pygmsh/badge/?version=latest)](http://pygmsh.readthedocs.org/en/latest/?badge=latest)
[![PyPi Version](https://img.shields.io/pypi/v/pygmsh.svg)](https://pypi.python.org/pypi/pygmsh)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/pygmsh.svg?style=social&label=Star&maxAge=2592000)](https://github.com/nschloe/pygmsh)

[Gmsh](http://geuz.org/gmsh/) is a powerful mesh generation tool with a
scripting language that is notoriously hard to write.

The goal of PyGmsh is to combine the power of Gmsh with the versatility of
Python and to provide useful abstractions from the Gmsh scripting language
so you can create complex geometries more easily.

![](https://nschloe.github.io/pygmsh/screw.png)

To create the above mesh, simply do
```python
import pygmsh as pg
import numpy as np

geom = pg.Geometry()

# Draw a cross.
poly = geom.add_polygon([
    [0.0,   0.5, 0.0],
    [-0.1,  0.1, 0.0],
    [-0.5,  0.0, 0.0],
    [-0.1, -0.1, 0.0],
    [0.0,  -0.5, 0.0],
    [0.1,  -0.1, 0.0],
    [0.5,   0.0, 0.0],
    [0.1,   0.1, 0.0]
    ],
    lcar=0.05
    )

axis = [0, 0, 1]

geom.extrude(
    poly,
    translation_axis=axis,
    rotation_axis=axis,
    point_on_axis=[0, 0, 0],
    angle=2.0 / 6.0 * np.pi
    )

points, cells, point_data, cell_data, field_data = pg.generate_mesh(geom)
```
to retrieve all points and cells of the mesh for the specified geometry.
To store the mesh, you can use [meshio](https://pypi.python.org/pypi/meshio);
for example
```python
import meshio
meshio.write('test.vtu', points, cells, cell_data=cell_data)
```
The output file can be visualized with various tools, e.g.,
[ParaView](http://www.paraview.org/).

You will find the above mesh in the directory `test/examples/` along with other
small examples.

### Installation

PyGmsh is [available from the Python Package
Index](https://pypi.python.org/pypi/pygmsh/), so simply type
```
pip install -U pygmsh
```
to install or upgrade.

### Usage

Just
```
import pygmsh as pg
```
and make use of all the goodies the module provides. The
[documentation](http://pygmsh.readthedocs.org/) and the examples under
[`test/examples/`](https://github.com/nschloe/pygmsh/tree/master/test/examples)
might inspire you.


### Testing

To run the PyGmsh unit tests, check out this repository and type
```
pytest
```

### Distribution

To create a new release

1. bump the `__version__` number,

2. publish to PyPi and GitHub:
    ```
    $ make publish
    ```

### License

PyGmsh is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
