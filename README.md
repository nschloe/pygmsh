# PyGmsh

[![Build Status](https://travis-ci.org/nschloe/pygmsh.svg)](https://travis-ci.org/nschloe/pygmsh)
[![Code Health](https://landscape.io/github/nschloe/pygmsh/master/landscape.png)](https://landscape.io/github/nschloe/pygmsh/master)
[![Coverage Status](https://coveralls.io/repos/nschloe/pygmsh/badge.svg?branch=master&service=github)](https://coveralls.io/github/nschloe/pygmsh?branch=master)
[![Documentation Status](https://readthedocs.org/projects/pygmsh/badge/?version=latest)](http://pygmsh.readthedocs.org/en/latest/?badge=latest)
[![PyPi Version](https://img.shields.io/pypi/v/pygmsh.svg)](https://pypi.python.org/pypi/pygmsh)
[![PyPi Downloads](https://img.shields.io/pypi/dm/pygmsh.svg)](https://pypi.python.org/pypi/pygmsh)

[Gmsh](http://geuz.org/gmsh/) is powerful mesh generation tool and its
scripting language is notoriously hard to write.

The goal PyGmsh is to combine the power of Gmsh with the versatility of
Python and to provide useful abstractions from the Gmsh scripting language
so you can create create complex geometries even more easily.

<p align="center">
  <a href="https://github.com/nschloe/pygmsh">
    <img height="257" src="https://nschloe.github.io/pygmsh/screw.png">
  </a>
</p>

To create the above mesh, simply do
```python
import pygmsh as pg
import numpy as np

# Draw a cross.
poly = pg.add_polygon([
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

pg.Extrude(
    'Surface{%s}' % poly,
    translation_axis=axis,
    rotation_axis=axis,
    point_on_axis=[0, 0, 0],
    angle=2.0 / 6.0 * np.pi
    )

print(pg.get_code())
```
and write the output to a file, e.g., `screw.geo`. Then use Gmsh to generate
the mesh
```bash
$ gmsh -3 screw.geo
```

You will find this example in the directory `test/examples/` along with other
small examples.

### Installation

#### Python Package Index

PyGmsh is [available from the Python Package
Index](https://pypi.python.org/pypi/pygmsh/), so simply type
```
pip install pygmsh
```
to install or
```
pip install pygmsh -U
```
to upgrade.

#### Manual installation

Download PyGmsh from [PyPi](https://pypi.python.org/pypi/pygmsh/)
or [GitHub](https://github.com/nschloe/pygmsh) and
install it with
```
python setup.py install
```

### Requirements

PyGmsh depends on

 * [NumPy](http://www.numpy.org/)

and, obviously, [Gmsh](http://geuz.org/gmsh/).

### Usage

Just
```
import pygmsh as pg
```
and make use of all the goodies the module provides. The
[documentation](http://pygmsh.readthedocs.org/) and the examples under
`test/examples/` might inspire you.


### Testing

To run the PyGmsh unit tests, check out this repository and type
```
nosetests
```

### License

PyGmsh is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
