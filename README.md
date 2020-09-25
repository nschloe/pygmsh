<p align="center">
  <a href="https://github.com/nschloe/pygmsh"><img alt="pygmsh" src="https://nschloe.github.io/pygmsh/logo-with-text.svg" width="60%"></a>
  <p align="center">Gmsh for Python.</p>
</p>

[![PyPi Version](https://img.shields.io/pypi/v/pygmsh.svg?style=flat-square)](https://pypi.org/project/pygmsh)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pygmsh.svg?style=flat-square)](https://pypi.org/pypi/pygmsh/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1173105.svg?style=flat-square)](https://doi.org/10.5281/zenodo.1173105)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/pygmsh.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/pygmsh)
[![PyPi downloads](https://img.shields.io/pypi/dm/pygmsh.svg?style=flat-square)](https://pypistats.org/packages/pygmsh)

[![Documentation Status](https://readthedocs.org/projects/pygmsh/badge/?version=latest&style=flat-square)](https://pygmsh.readthedocs.org/en/latest/?badge=latest)
[![Slack](https://img.shields.io/static/v1?logo=slack&label=chat&message=on%20slack&color=4a154b&style=flat-square)](https://join.slack.com/t/nschloe/shared_invite/zt-cofhrwm8-BgdrXAtVkOjnDmADROKD7A
)

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/pygmsh/ci?style=flat-square)](https://github.com/nschloe/pygmsh/actions?query=workflow%3Aci)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/pygmsh.svg?style=flat-square)](https://codecov.io/gh/nschloe/pygmsh)
[![LGTM](https://img.shields.io/lgtm/grade/python/github/nschloe/pygmsh.svg?style=flat-square)](https://lgtm.com/projects/g/nschloe/pygmsh)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

pygmsh combines the power of [Gmsh](https://gmsh.info/) with the versatility of Python.
It provides useful abstractions from Gmsh's own Python interface so you can create
complex geometries more easily.

See [here](https://pygmsh.readthedocs.io/en/latest/index.html) for the full
documentation.

#### Flat shapes

<img src="https://nschloe.github.io/pygmsh/polygon.png" width="100%"> | <img src="https://nschloe.github.io/pygmsh/chebyshev1.svg" width="100%"> | <img src="https://nschloe.github.io/pygmsh/chebyshev2.svg" width="100%">
:------------------:|:------------------:|:-------------:|
Polygon             |  Chebyshev 1       |  Chebyshev 2  |

Codes:
```python
import pygmsh

with pygmsh.built_in.Geometry() as geom:
    geom.add_polygon(
        [
            [0.0, 0.0],
            [1.0, -0.2],
            [1.1, 1.2],
            [0.1, 0.7],
        ],
        mesh_size=0.1,
    )
    mesh = pygmsh.generate_mesh(geom)

mesh.write("out.vtk")
```

#### Built-in

![](https://nschloe.github.io/pygmsh/screw.png)

To create the above mesh, simply do
```python
from math import pi
import pygmsh

with pygmsh.built_in.Geometry() as geom:
    # Draw a cross.
    poly = geom.add_polygon(
        [
            [+0.0, +0.5],
            [-0.1, +0.1],
            [-0.5, +0.0],
            [-0.1, -0.1],
            [+0.0, -0.5],
            [+0.1, -0.1],
            [+0.5, +0.0],
            [+0.1, +0.1],
        ],
        mesh_size=0.05,
    )

    geom.twist(
        poly,
        translation_axis=[0, 0, 1],
        rotation_axis=[0, 0, 1],
        point_on_axis=[0, 0, 0],
        angle=pi / 3,
    )

    mesh = pygmsh.generate_mesh(geom)

# mesh.points, mesh.cells, ...
```
to retrieve all points and cells of the mesh for the specified geometry.
The return value is a [meshio](https://pypi.org/project/meshio) mesh, so to store it
to a file you can
<!--exdown-skip-->
```python
mesh.write("test.vtk")
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
```python
import pygmsh

with pygmsh.opencascade.Geometry() as geom:
    geom.characteristic_length_min = 0.1
    geom.characteristic_length_max = 0.1

    rectangle = geom.add_rectangle([-1.0, -1.0, 0.0], 2.0, 2.0)
    disk1 = geom.add_disk([-1.2, 0.0, 0.0], 0.5)
    disk2 = geom.add_disk([+1.2, 0.0, 0.0], 0.5)

    disk3 = geom.add_disk([0.0, -0.9, 0.0], 0.5)
    disk4 = geom.add_disk([0.0, +0.9, 0.0], 0.5)
    flat = geom.boolean_difference(
        geom.boolean_union([rectangle, disk1, disk2]),
        geom.boolean_union([disk3, disk4]),
    )

    geom.extrude(flat, [0, 0, 0.3])

    mesh = pygmsh.generate_mesh(geom)
```

### Installation

pygmsh is [available from the Python Package Index](https://pypi.org/project/pygmsh/),
so simply do
```
pip install pygmsh
```
to install. Also, make sure to have [gmsh](http://gmsh.info/) installed.

### Usage
Just
```
import pygmsh
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

This software is published under the [GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).
