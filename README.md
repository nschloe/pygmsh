<p align="center">
  <a href="https://github.com/nschloe/pygmsh"><img alt="pygmsh" src="https://nschloe.github.io/pygmsh/logo-with-text.svg" width="60%"></a>
  <p align="center">Gmsh for Python.</p>
</p>

[![PyPi Version](https://img.shields.io/pypi/v/pygmsh.svg?style=flat-square)](https://pypi.org/project/pygmsh/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pygmsh.svg?style=flat-square)](https://pypi.org/project/pygmsh/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1173105.svg?style=flat-square)](https://doi.org/10.5281/zenodo.1173105)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/pygmsh.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/pygmsh)
[![PyPi downloads](https://img.shields.io/pypi/dm/pygmsh.svg?style=flat-square)](https://pypistats.org/packages/pygmsh)

[![Discord](https://img.shields.io/static/v1?logo=discord&label=chat&message=on%20discord&color=7289da&style=flat-square)](https://discord.gg/hnTJ5MRX2Y)
[![Documentation Status](https://readthedocs.org/projects/pygmsh/badge/?version=latest&style=flat-square)](https://pygmsh.readthedocs.io/en/latest/?badge=latest)

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/pygmsh/ci?style=flat-square)](https://github.com/nschloe/pygmsh/actions?query=workflow%3Aci)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/pygmsh.svg?style=flat-square)](https://codecov.io/gh/nschloe/pygmsh)
[![LGTM](https://img.shields.io/lgtm/grade/python/github/nschloe/pygmsh.svg?style=flat-square)](https://lgtm.com/projects/g/nschloe/pygmsh)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

pygmsh combines the power of [Gmsh](https://gmsh.info/) with the versatility of Python.
It provides useful abstractions from Gmsh's own Python interface so you can create
complex geometries more easily.

To use, install Gmsh itself and pygmsh from [pypi](https://pypi.org/project/pygmsh/):
```
[sudo] apt install python3-gmsh
pip install pygmsh
```

This document and the [`tests/`](https://github.com/nschloe/pygmsh/tree/main/tests/)
directory contain many small examples. See
[here](https://pygmsh.readthedocs.io/en/latest/index.html) for the full documentation.

#### Flat shapes

<img src="https://nschloe.github.io/pygmsh/polygon.svg" width="100%"> | <img src="https://nschloe.github.io/pygmsh/circle.svg" width="100%"> | <img src="https://nschloe.github.io/pygmsh/splines.svg" width="100%">
:------------------:|:-------------:|:-------------:|
Polygon             |  Circle       |  (B-)Splines  |

Codes:
```python
import pygmsh

with pygmsh.geo.Geometry() as geom:
    geom.add_polygon(
        [
            [0.0, 0.0],
            [1.0, -0.2],
            [1.1, 1.2],
            [0.1, 0.7],
        ],
        mesh_size=0.1,
    )
    mesh = geom.generate_mesh()

# mesh.points, mesh.cells, ...
# mesh.write("out.vtk")
```
```python
import pygmsh

with pygmsh.geo.Geometry() as geom:
    geom.add_circle([0.0, 0.0], 1.0, mesh_size=0.2)
    mesh = geom.generate_mesh()
```
```python
import pygmsh

with pygmsh.geo.Geometry() as geom:
    lcar = 0.1
    p1 = geom.add_point([0.0, 0.0], lcar)
    p2 = geom.add_point([1.0, 0.0], lcar)
    p3 = geom.add_point([1.0, 0.5], lcar)
    p4 = geom.add_point([1.0, 1.0], lcar)
    s1 = geom.add_bspline([p1, p2, p3, p4])

    p2 = geom.add_point([0.0, 1.0], lcar)
    p3 = geom.add_point([0.5, 1.0], lcar)
    s2 = geom.add_spline([p4, p3, p2, p1])

    ll = geom.add_curve_loop([s1, s2])
    pl = geom.add_plane_surface(ll)

    mesh = geom.generate_mesh()
```

The return value is always a [meshio](https://pypi.org/project/meshio/) mesh, so to store
it to a file you can
<!--pytest-codeblocks:skip-->
```python
mesh.write("test.vtk")
```
The output file can be visualized with various tools, e.g.,
[ParaView](https://www.paraview.org/).

With
<!--pytest-codeblocks:skip-->
```python
pygmsh.write("test.msh")
```
you can access Gmsh's native file writer.

#### Extrusions

<img src="https://nschloe.github.io/pygmsh/extrude.png" width="100%"> | <img src="https://nschloe.github.io/pygmsh/revolve.png" width="100%"> | <img src="https://nschloe.github.io/pygmsh/twist.png" width="100%">
:------------------:|:-------------:|:--------:|
`extrude`           |  `revolve`    |  `twist` |

```python
import pygmsh

with pygmsh.geo.Geometry() as geom:
    poly = geom.add_polygon(
        [
            [0.0, 0.0],
            [1.0, -0.2],
            [1.1, 1.2],
            [0.1, 0.7],
        ],
        mesh_size=0.1,
    )
    geom.extrude(poly, [0.0, 0.3, 1.0], num_layers=5)
    mesh = geom.generate_mesh()
```
```python
from math import pi
import pygmsh

with pygmsh.geo.Geometry() as geom:
    poly = geom.add_polygon(
        [
            [0.0, 0.2, 0.0],
            [0.0, 1.2, 0.0],
            [0.0, 1.2, 1.0],
        ],
        mesh_size=0.1,
    )
    geom.revolve(poly, [0.0, 0.0, 1.0], [0.0, 0.0, 0.0], 0.8 * pi)
    mesh = geom.generate_mesh()
```
```python
from math import pi
import pygmsh

with pygmsh.geo.Geometry() as geom:
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

    mesh = geom.generate_mesh()
```

#### OpenCASCADE
<img src="https://nschloe.github.io/pygmsh/intersection.png" width="100%"> | <img src="https://nschloe.github.io/pygmsh/ellipsoid-holes.png" width="100%"> | <img src="https://nschloe.github.io/pygmsh/puzzle.png" width="100%">
:------------------:|:-------------:|:--------:|
 |    |   |

As of version 3.0, Gmsh supports OpenCASCADE (`occ`), allowing for a CAD-style geometry
specification.
```python
from math import pi, cos
import pygmsh

with pygmsh.occ.Geometry() as geom:
    geom.characteristic_length_max = 0.1
    r = 0.5
    disks = [
        geom.add_disk([-0.5 * cos(7 / 6 * pi), -0.25], 1.0),
        geom.add_disk([+0.5 * cos(7 / 6 * pi), -0.25], 1.0),
        geom.add_disk([0.0, 0.5], 1.0),
    ]
    geom.boolean_intersection(disks)

    mesh = geom.generate_mesh()
```
```python
# ellpsoid with holes
import pygmsh

with pygmsh.occ.Geometry() as geom:
    geom.characteristic_length_max = 0.1
    ellipsoid = geom.add_ellipsoid([0.0, 0.0, 0.0], [1.0, 0.7, 0.5])

    cylinders = [
        geom.add_cylinder([-1.0, 0.0, 0.0], [2.0, 0.0, 0.0], 0.3),
        geom.add_cylinder([0.0, -1.0, 0.0], [0.0, 2.0, 0.0], 0.3),
        geom.add_cylinder([0.0, 0.0, -1.0], [0.0, 0.0, 2.0], 0.3),
    ]
    geom.boolean_difference(ellipsoid, geom.boolean_union(cylinders))

    mesh = geom.generate_mesh()
```
```python
# puzzle piece
import pygmsh

with pygmsh.occ.Geometry() as geom:
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

    mesh = geom.generate_mesh()
```


#### Mesh refinement/boundary layers
<img src="https://nschloe.github.io/pygmsh/boundary0.svg" width="100%"> | <img src="https://nschloe.github.io/pygmsh/mesh-refinement-2d.svg" width="100%"> | <img src="https://nschloe.github.io/pygmsh/ball-mesh-refinement.png" width="70%">
:------------------:|:-------------:|:--------:|
 |    |   |

```python
# boundary refinement
import pygmsh

with pygmsh.geo.Geometry() as geom:
    poly = geom.add_polygon(
        [
            [0.0, 0.0],
            [2.0, 0.0],
            [3.0, 1.0],
            [1.0, 2.0],
            [0.0, 1.0],
        ],
        mesh_size=0.3,
    )

    field0 = geom.add_boundary_layer(
        edges_list=[poly.curves[0]],
        lcmin=0.05,
        lcmax=0.2,
        distmin=0.0,
        distmax=0.2,
    )
    field1 = geom.add_boundary_layer(
        nodes_list=[poly.points[2]],
        lcmin=0.05,
        lcmax=0.2,
        distmin=0.1,
        distmax=0.4,
    )
    geom.set_background_mesh([field0, field1], operator="Min")

    mesh = geom.generate_mesh()
```
<!--pytest-codeblocks:skip-->
```python
# mesh refinement with callback
import pygmsh

with pygmsh.geo.Geometry() as geom:
    geom.add_polygon(
        [
            [-1.0, -1.0],
            [+1.0, -1.0],
            [+1.0, +1.0],
            [-1.0, +1.0],
        ]
    )
    geom.set_mesh_size_callback(
        lambda dim, tag, x, y, z: 6.0e-2 + 2.0e-1 * (x ** 2 + y ** 2)
    )

    mesh = geom.generate_mesh()
```
<!--pytest-codeblocks:skip-->
```python
# ball with mesh refinement
from math import sqrt
import pygmsh


with pygmsh.occ.Geometry() as geom:
    geom.add_ball([0.0, 0.0, 0.0], 1.0)

    geom.set_mesh_size_callback(
        lambda dim, tag, x, y, z: abs(sqrt(x ** 2 + y ** 2 + z ** 2) - 0.5) + 0.1
    )
    mesh = geom.generate_mesh()
```

#### Optimization

pygmsh can optimize existing meshes, too.
<!--pytest-codeblocks:skip-->
```python
import meshio

mesh = meshio.read("mymesh.vtk")
optimized_mesh = pygmsh.optimize(mesh, method="")
```
You can also use the command-line utility
```
pygmsh-optimize input.vtk output.xdmf
```
where input and output can be any format supported by
[meshio](https://pypi.org/project/meshio/).

### Testing
To run the pygmsh unit tests, check out this repository and type
```
pytest
```

### Building Documentation
Docs are built using [Sphinx](http://www.sphinx-doc.org/en/stable/).

To build, run
```
sphinx-build -b html doc doc/_build
```

### License

This software is published under the [GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).
