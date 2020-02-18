<p align="center">
  <a href="https://github.com/nschloe/pygmsh"><img alt="pygmsh" src="https://nschloe.github.io/pygmsh/logo-with-text.svg" width="60%"></a>
  <p align="center">Gmsh for Python.</p>
</p>

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/pygmsh/master.svg?style=flat-square)](https://circleci.com/gh/nschloe/pygmsh)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/pygmsh.svg?style=flat-square)](https://codecov.io/gh/nschloe/pygmsh)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/pygmsh/badge/?version=latest&style=flat-square)](https://pygmsh.readthedocs.org/en/latest/?badge=latest)
[![PyPi Version](https://img.shields.io/pypi/v/pygmsh.svg?style=flat-square)](https://pypi.org/project/pygmsh)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pygmsh.svg?style=flat-square)](https://pypi.org/pypi/pygmsh/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1173105.svg?style=flat-square)](https://doi.org/10.5281/zenodo.1173105)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/pygmsh.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/pygmsh)
[![PyPi downloads](https://img.shields.io/pypi/dm/pygmsh.svg?style=flat-square)](https://pypistats.org/packages/pygmsh)
[![Slack](https://img.shields.io/static/v1?logo=slack&label=chat&message=on%20slack&color=4a154b&style=flat-square)](https://app.slack.com/client/TTL6Q54A3/CTLGZQFML/)

[Gmsh](https://gmsh.info/) is a powerful mesh generation tool with a scripting language
that is notoriously hard to write.

The goal of pygmsh is to combine the power of Gmsh with the versatility of Python and to
provide useful abstractions from the Gmsh scripting language so you can create complex
geometries more easily.

See [here](https://pygmsh.readthedocs.io/en/latest/index.html) for the full
documentation.

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

mesh = pygmsh.generate_mesh(geom)
# mesh.points, mesh.cells, ...
```
to retrieve all points and cells of the mesh for the specified geometry.  To store the
mesh, you can use [meshio](https://pypi.org/project/meshio); for example
```python
import meshio
meshio.write("test.vtk", mesh)
```
The output file can be visualized with various tools, e.g.,
[ParaView](https://www.paraview.org/).

You will find the above mesh in the directory
[`test/`](https://github.com/nschloe/pygmsh/tree/master/test/) along with other small
examples.

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

mesh = pygmsh.generate_mesh(geom)
```

### Installation

pygmsh is [available from the Python Package Index](https://pypi.org/project/pygmsh/),
so simply type
```
pip install pygmsh
```
to install. Also make sure to have [gmsh](http://gmsh.info/) installed.

### Usage

Just
```
import pygmsh as pg
```
and make use of all the goodies the module provides. The
[documentation](https://pygmsh.readthedocs.org/) and the examples under
[`test/`](https://github.com/nschloe/pygmsh/tree/master/test/) might inspire you.


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

### License

pygmsh is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
