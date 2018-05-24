#####################
Geometry Construction
#####################

This class provides a Python interface for the Gmsh scripting language. It aims
at working around some of Gmsh's inconveniences (e.g., having to manually
assign an ID for every entity created) and providing access to Python's
features.

In Gmsh, the user must manually provide a unique ID for every point, curve,
volume created. This can get messy when a lot of entities are created and it
isn't clear which IDs are already in use. Some Gmsh commands even create new
entities and silently reserve IDs in that way. This module tries to work around
this by providing routines in the style of add_point(x) which _return_ the ID.
To make variable names in Gmsh unique, keep track of how many points, circles,
etc. have already been created. Variable names will then be p1, p2, etc. for
points, c1, c2, etc. for circles and so on.

.. automodule:: pygmsh.built_in

***************
Built-in Engine
***************

Geometry
========
.. automodule:: pygmsh.built_in.geometry
    :members:
    :undoc-members:
    :show-inheritance:

Bspline
=======
.. automodule:: pygmsh.built_in.bspline
    :members:
    :undoc-members:
    :show-inheritance:

CircleArc
=========
.. automodule:: pygmsh.built_in.circle_arc
    :members:
    :undoc-members:
    :show-inheritance:

CompoundLine
============
.. automodule:: pygmsh.built_in.compound_line
    :members:
    :undoc-members:
    :show-inheritance:

CompoundSurface
===============
.. automodule:: pygmsh.built_in.compound_surface
    :members:
    :undoc-members:
    :show-inheritance:

CompoundVolume
==============
.. automodule:: pygmsh.built_in.compound_volume
    :members:
    :undoc-members:
    :show-inheritance:

EllipseArc
==========
.. automodule:: pygmsh.built_in.ellipse_arc
    :members:
    :undoc-members:
    :show-inheritance:

LineBase
========
.. automodule:: pygmsh.built_in.line_base
    :members:
    :undoc-members:
    :show-inheritance:

LineLoop
========
.. automodule:: pygmsh.built_in.line_loop
    :members:
    :undoc-members:
    :show-inheritance:

Line
====
.. automodule:: pygmsh.built_in.line
    :members:
    :undoc-members:
    :show-inheritance:

PlaneSurface
============
.. automodule:: pygmsh.built_in.plane_surface
    :members:
    :undoc-members:
    :show-inheritance:

Point
=====
.. automodule:: pygmsh.built_in.point
    :members:
    :undoc-members:
    :show-inheritance:

Spline
======
.. automodule:: pygmsh.built_in.spline
    :members:
    :undoc-members:
    :show-inheritance:

SurfaceBase
===========
.. automodule:: pygmsh.built_in.surface_base
    :members:
    :undoc-members:
    :show-inheritance:

SurfaceLoop
===========
.. automodule:: pygmsh.built_in.surface_loop
    :members:
    :undoc-members:
    :show-inheritance:

Surface
=======
.. automodule:: pygmsh.built_in.surface
    :members:
    :undoc-members:
    :show-inheritance:

VolumeBase
==========
.. automodule:: pygmsh.built_in.volume_base
    :members:
    :undoc-members:
    :show-inheritance:

Volume
======
.. automodule:: pygmsh.built_in.volume
    :members:
    :undoc-members:
    :show-inheritance:


******************
openCASCADE Engine
******************

Geometry
========
.. automodule:: pygmsh.opencascade.geometry
    :members:
    :undoc-members:
    :show-inheritance:

Ball
====
.. automodule:: pygmsh.opencascade.ball
    :members:
    :undoc-members:
    :show-inheritance:

Box
===
.. automodule:: pygmsh.opencascade.box
    :members:
    :undoc-members:
    :show-inheritance:

Cone
====
.. automodule:: pygmsh.opencascade.cone
    :members:
    :undoc-members:
    :show-inheritance:

Cylinder
========
.. automodule:: pygmsh.opencascade.cylinder
    :members:
    :undoc-members:
    :show-inheritance:

Disk
====
.. automodule:: pygmsh.opencascade.disk
    :members:
    :undoc-members:
    :show-inheritance:

Rectangle
=========
.. automodule:: pygmsh.opencascade.rectangle
    :members:
    :undoc-members:
    :show-inheritance:

SurfaceBase
===========
.. automodule:: pygmsh.opencascade.surface_base
    :members:
    :undoc-members:
    :show-inheritance:

Torus
=====
.. automodule:: pygmsh.opencascade.torus
    :members:
    :undoc-members:
    :show-inheritance:

VolumeBase
==========
.. automodule:: pygmsh.opencascade.volume_base
    :members:
    :undoc-members:
    :show-inheritance:

Wedge
=====
.. automodule:: pygmsh.opencascade.wedge
    :members:
    :undoc-members:
    :show-inheritance:







