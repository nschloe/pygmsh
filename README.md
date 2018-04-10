# pygmsh

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/pygmsh/master.svg)](https://circleci.com/gh/nschloe/pygmsh)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/pygmsh.svg)](https://codecov.io/gh/nschloe/pygmsh)
[![Codacy grade](https://img.shields.io/codacy/grade/03aca50105054d18bf1f5ca3add9f2ee.svg)](https://app.codacy.com/app/nschloe/pygmsh/dashboard)
[![Documentation Status](https://readthedocs.org/projects/pygmsh/badge/?version=latest)](https://pygmsh.readthedocs.org/en/latest/?badge=latest)
[![PyPi Version](https://img.shields.io/pypi/v/pygmsh.svg)](https://pypi.org/project/pygmsh)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1173105.svg)](https://doi.org/10.5281/zenodo.1173105)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/pygmsh.svg?logo=github&label=Stars)](https://github.com/nschloe/pygmsh)

<p align="center">
  <img src="https://nschloe.github.io/pygmsh/logo.png" width="20%">
</p>

[Gmsh](https://gmsh.info/) is a powerful mesh generation tool with a
scripting language that is notoriously hard to write.

The goal of pygmsh is to combine the power of Gmsh with the versatility of
Python and to provide useful abstractions from the Gmsh scripting language
so you can create complex geometries more easily.

#### Built-in

![](https://nschloe.github.io/pygmsh/screw.png)

To create the above mesh, simply do
```python,test
import pygmsh
import numpy as np

geom = pygmsh.built_in.Geometry()

# Draw a cross.
poly = geom.add_polygon([
    [ 0.0,  0.5, 0.0],
    [-0.1,  0.1, 0.0],
    [-0.5,  0.0, 0.0],
    [-0.1, -0.1, 0.0],
    [ 0.0, -0.5, 0.0],
    [ 0.1, -0.1, 0.0],
    [ 0.5,  0.0, 0.0],
    [ 0.1,  0.1, 0.0]
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

points, cells, point_data, cell_data, field_data = pygmsh.generate_mesh(geom)
```
to retrieve all points and cells of the mesh for the specified geometry.
To store the mesh, you can use [meshio](https://pypi.org/project/meshio);
for example
```python
import meshio
meshio.write('test.vtu', points, cells, cell_data=cell_data)
```
The output file can be visualized with various tools, e.g.,
[ParaView](https://www.paraview.org/).

You will find the above mesh in the directory
[`test/`](https://github.com/nschloe/pygmsh/tree/master/test/) along with other
small examples.

#### OpenCASCADE

![](https://nschloe.github.io/pygmsh/puzzle.png)

As of version 3.0, Gmsh supports OpenCASCADE, allowing for a CAD-style geometry
specification.

Example:
```python,test
import pygmsh

geom = pygmsh.opencascade.Geometry(
  characteristic_length_min=0.1,
  characteristic_length_max=0.1,
  )

rectangle = geom.add_rectangle([-1.0, -1.0, 0.0], 2.0, 2.0)
disk1 = geom.add_disk([-1.2, 0.0, 0.0], 0.5)
disk2 = geom.add_disk([+1.2, 0.0, 0.0], 0.5)
union = geom.boolean_union([rectangle, disk1, disk2])

disk3 = geom.add_disk([0.0, -0.9, 0.0], 0.5)
disk4 = geom.add_disk([0.0, +0.9, 0.0], 0.5)
flat = geom.boolean_difference([union], [disk3, disk4])

geom.extrude(flat, [0, 0, 0.3])

points, cells, point_data, cell_data, field_data = pygmsh.generate_mesh(geom)
```

### Installation

pygmsh is [available from the Python Package
Index](https://pypi.org/project/pygmsh/), so simply type
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
[documentation](https://pygmsh.readthedocs.org/) and the examples under
[`test/`](https://github.com/nschloe/pygmsh/tree/master/test/)
might inspire you.


### Testing

To run the pygmsh unit tests, check out this repository and type
```
pytest
```

### Building Documentation

Docs are built using [Sphinx](http://www.sphinx-doc.org/en/stable/).

To build run
```
sphinx-build -b html doc doc/_build
```

### Distribution

To create a new release

1. bump the `__version__` number,

2. publish to PyPi and GitHub:
    ```
    $ make publish
    ```

### License

pygmsh is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
