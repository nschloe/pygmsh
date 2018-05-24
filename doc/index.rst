.. pygmsh documentation master file, created by
   sphinx-quickstart on Tue Oct 27 19:56:53 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pygmsh's documentation!
==================================

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

Geometry Overview
-----------------

Gmsh’s geometry module provides a simple CAD engine, using a boundary representation 
(“BRep”) approach: you need to first define points (using the Point command: see below), 
then lines (using Line, Circle, Spline, …, commands or by extruding points), then surfaces 
(using for example the Plane Surface or Surface commands, or by extruding lines), 
and finally volumes (using the Volume command or by extruding surfaces).

These geometrical entities are called “elementary” in Gmsh’s jargon, and 
are assigned identification numbers (stricly positive) when they are created:

1. Each elementary point must possess a unique identification number;
2. Each elementary line must possess a unique identification number;
3. Each elementary surface must possess a unique identification number;
4. Each elementary volume must possess a unique identification number.

Elementary geometrical entities can then be manipulated in various ways, for 
example using the Translate, Rotate, Scale or Symmetry commands. 
They can be deleted with the Delete command, provided that no 
higher-dimension entity references them. Zero or negative identification 
numbers are reserved by the system for special uses: do not use them in your scripts.

Groups of elementary geometrical entities can also be defined and are called 
“physical” entities. These physical entities cannot be modified by geometry 
commands: their only purpose is to assemble elementary entities into larger 
groups so that they can be referred to by the mesh module as single entities. 
As is the case with elementary entities, each physical point, physical line, 
physical surface or physical volume must be assigned a unique identification number.

Contents:

.. toctree::
    :maxdepth: 1
    :caption: Table of Contents

    built_in
    opencascade
