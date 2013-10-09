'''
This module contains some convenience functions for building simple geometric
objects with Gmsh.
'''
# -----------------------------------------------------------------------------
import numpy as np
from basic import *
# -----------------------------------------------------------------------------
def rotation_matrix(u, theta):
    '''Return matrix that implements the rotation around the vector u by the
    angle theta, cf.
    <https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle>.
    '''
    # Cross-product matrix.
    cpm = np.array([[  0.0, -u[2],  u[1]],
                    [ u[2],   0.0, -u[0]],
                    [-u[1],  u[0],  0.0]])
    c = np.cos(theta)
    s = np.sin(theta)
    R = np.eye(3) * c \
      + s * cpm \
      + (1.0 - c) * np.outer(u, u)

    return R
# -----------------------------------------------------------------------------
def add_circle(radius, lcar,
               R = np.eye(3),
               x0 = np.array([0.0, 0.0, 0.0]),
               compound = False
               ):
    '''Add circle.
    '''
    # Define points that make the circle (midpoint and the four cardinal
    # directions).
    X = np.array([[0.0, 0.0,     0.0    ],
                  [0.0, radius,  0.0    ],
                  [0.0, 0.0,     radius ],
                  [0.0, 0.0,     -radius],
                  [0.0, -radius, 0.0    ]])
    # Apply the transformation.
    # TODO assert that the transformation preserves circles
    X = [np.dot(R, x) + x0 for x in X]
    # Add Gmsh Points.
    Comment('Points')
    p = [Point(x, lcar) for x in X]

    # Four circle arcs
    Comment('Circle arcs')
    c = [Circle([p[1], p[0], p[2]]),
         Circle([p[2], p[0], p[4]]),
         Circle([p[4], p[0], p[3]]),
         Circle([p[3], p[0], p[1]])
         ]

    if compound:
        c = [CompoundLine(cc)]

    return c
# -----------------------------------------------------------------------------
def add_ball(x0, radius, lcar,
             with_volume = True,
             holes = [],
             label=None
             ):

    # Add points.
    p = [Point(x0, lcar=lcar),
         Point([x0[0]+radius, x0[1],        x0[2]       ], lcar=lcar),
         Point([x0[0],        x0[1]+radius, x0[2]       ], lcar=lcar),
         Point([x0[0],        x0[1],        x0[2]+radius], lcar=lcar),
         Point([x0[0]-radius, x0[1],        x0[2]       ], lcar=lcar),
         Point([x0[0],        x0[1]-radius, x0[2]       ], lcar=lcar),
         Point([x0[0],        x0[1],        x0[2]-radius], lcar=lcar)
         ]

    # Add ball skeleton.
    c = [Circle([p[1], p[0], p[6]]),
         Circle([p[6], p[0], p[4]]),
         Circle([p[4], p[0], p[3]]),
         Circle([p[3], p[0], p[1]]),
         Circle([p[1], p[0], p[2]]),
         Circle([p[2], p[0], p[4]]),
         Circle([p[4], p[0], p[5]]),
         Circle([p[5], p[0], p[1]]),
         Circle([p[6], p[0], p[2]]),
         Circle([p[2], p[0], p[3]]),
         Circle([p[3], p[0], p[5]]),
         Circle([p[5], p[0], p[6]])
         ]

    # Add surfaces (1/8th of the ball surface).
    ll = [LineLoop([c[4],      c[9],     c[3]]),
          LineLoop([c[8],      '-'+c[4], c[0]]),
          LineLoop([c[11],     '-'+c[7], '-'+c[0]]),
          LineLoop([c[7],      '-'+c[3], c[10]]),
          LineLoop(['-'+c[9],  c[5],     c[2]]),
          LineLoop(['-'+c[10], '-'+c[2], c[6]]),
          LineLoop(['-'+c[1],  '-'+c[6], '-'+c[11]]),
          LineLoop(['-'+c[5],  '-'+c[8], c[1]])
          ]

    # Create a surface for each line loop.
    s = [RuledSurface(l) for l in ll]

    # Create the surface loop.
    surface_loop = SurfaceLoop(s)
    if holes:
        # Create an array of surface loops; the first entry is the outer
        # surface loop, the following ones are holes.
        surface_loop = Array([surface_loop] + holes)

    # Create volume.
    if with_volume:
        volume = Volume(surface_loop)
        if label:
            PhysicalVolume(vol, label)
    else:
        volume = None

    return volume, surface_loop
# -----------------------------------------------------------------------------
def add_box(x0, x1, y0, y1, z0, z1,
            lcar,
            with_volume = True,
            holes = [],
            label = None
            ):
    # Define corner points.
    p = [Point([x1, y1, z1], lcar = lcar),
         Point([x1, y1, z0], lcar = lcar),
         Point([x1, y0, z1], lcar = lcar),
         Point([x1, y0, z0], lcar = lcar),
         Point([x0, y1, z1], lcar = lcar),
         Point([x0, y1, z0], lcar = lcar),
         Point([x0, y0, z1], lcar = lcar),
         Point([x0, y0, z0], lcar = lcar)
         ]

    # Define edges.
    e = [Line(p[0], p[1]),
         Line(p[0], p[2]),
         Line(p[0], p[4]),
         Line(p[1], p[3]),
         Line(p[1], p[5]),
         Line(p[2], p[3]),
         Line(p[2], p[6]),
         Line(p[3], p[7]),
         Line(p[4], p[5]),
         Line(p[4], p[6]),
         Line(p[5], p[7]),
         Line(p[6], p[7])
         ]

    # Define the six line loops.
    ll = [LineLoop([e[0], e[3],  '-'+e[5],  '-'+e[1]]),
          LineLoop([e[0], e[4],  '-'+e[8],  '-'+e[2]]),
          LineLoop([e[1], e[6],  '-'+e[9],  '-'+e[2]]),
          LineLoop([e[3], e[7],  '-'+e[10], '-'+e[4]]),
          LineLoop([e[5], e[7],  '-'+e[11], '-'+e[6]]),
          LineLoop([e[8], e[10], '-'+e[11], '-'+e[9]])
          ]

    # Create a surface for each line loop.
    s = [RuledSurface(l) for l in ll]

    # Create the surface loop.
    surface_loop = SurfaceLoop(s)
    if holes:
        # Create an array of surface loops; the first entry is the outer
        # surface loop, the following ones are holes.
        surface_loop = Array([surface_loop] + holes)

    if with_volume:
        # Create volume
        vol = Volume(surface_loop)
        if label:
            PhysicalVolume(vol, label)
    else:
        vol = None

    return vol, surface_loop
# -----------------------------------------------------------------------------
def add_torus(irad, orad,
              lcar,
              R = np.eye(3),
              x0 = np.array([0.0, 0.0, 0.0]),
              label = None
              ):
    '''Create Gmsh code for torus with

    irad ... inner radius
    orad ... outer radius

    under the coordinate transformation

        x_hat = R*x + x0.
    '''
    Comment(76*'-')
    Comment('Torus')

    # Add circle
    x0t = np.dot(R, np.array([0.0, orad, 0.0]))
    c = add_circle(irad, lcar, R=R, x0=x0+x0t)

    rot_axis = [0.0, 0.0, 1.0]
    rot_axis = np.dot(R, rot_axis)
    point_on_rot_axis = [0.0, 0.0, 0.0]
    point_on_rot_axis = np.dot(R, point_on_rot_axis) + x0

    # Form the torus by extruding the circle three times by 2/3*pi.
    # This works around the inability of Gmsh to extrude by pi or more.  The
    # Extrude() macro returns an array; the first [0] entry in the array is
    # the entity that has been extruded at the far end. This can be used for
    # the following Extrude() step.  The second [1] entry of the array is the
    # surface that was created by the extrusion.
    previous = c
    angle = '2*Pi/3'
    all_names = []
    for i in range(3):
        Comment('Round no. %s' % (i+1))
        for k in range(len(previous)):
            # ts1[] = Extrude {{0,0,1}, {0,0,0}, 2*Pi/3}{Line{tc1};};
            # ...
            name = Extrude_rotate('Line{%s}' % previous[k],
                                  rot_axis,
                                  point_on_rot_axis,
                                  angle
                                  )
            all_names.append(name)
            previous[k] = name + '[0]'

    # Now build surface loop and volume.
    all_surfaces = [name + '[1]' for name in all_names]

    #compound_surface = CompoundSurface(all_surfaces)

    surface_loop = SurfaceLoop(all_surfaces)
    vol = Volume(surface_loop)
    if label:
        PhysicalVolume(vol, label)

    Comment(76*'-')
    return
# -----------------------------------------------------------------------------
def add_pipe(outer_radius, inner_radius, length,
             R = np.eye(3),
             x0 = np.array([0.0, 0.0, 0.0]),
             label = None,
             lcar = 0.1
             ):
    '''Hollow cylinder.
    '''
    # Define rectangle which to extrude.
    X = np.array([[0.0, outer_radius, -0.5*length],
                  [0.0, outer_radius,  0.5*length],
                  [0.0, inner_radius,  0.5*length],
                  [0.0, inner_radius, -0.5*length]
                  ])
    # Apply transformation.
    X = [np.dot(R, x) + x0 for x in X]
    # Create points set.
    p = [Point(x, lcar) for x in X]

    # Define edges.
    e = [Line(p[0], p[1]),
         Line(p[1], p[2]),
         Line(p[2], p[3]),
         Line(p[3], p[0])
         ]

    rot_axis = [0.0, 0.0, 1.0]
    rot_axis = np.dot(R, rot_axis)
    point_on_rot_axis = [0.0, 0.0, 0.0]
    point_on_rot_axis = np.dot(R, point_on_rot_axis) + x0

    # Extrude all edges three times by 2*Pi/3.
    previous = e
    angle = '2*Pi/3'
    all_names = []
    for i in range(3):
        Comment('Round no. %s' % (i+1))
        for k in range(4):
            # ts1[] = Extrude {{0,0,1}, {0,0,0}, 2*Pi/3}{Line{tc1};};
            name = Extrude_rotate('Line{%s}' % previous[k],
                                  rot_axis,
                                  point_on_rot_axis,
                                  angle
                                  )
            all_names.append(name)
            previous[k] = name + '[0]'

    # Now just add surface loop and volume.
    all_surfaces = (name + '[1]' for name in all_names)
    surface_loop = SurfaceLoop(all_surfaces)
    vol = Volume(surface_loop)
    if label:
        PhysicalVolume(vol, label)

    return
# -----------------------------------------------------------------------------
def add_pipe2(outer_radius, inner_radius, length,
              R = np.eye(3),
              x0 = np.array([0.0, 0.0, 0.0]),
              label = None,
              lcar = 0.1
              ):

    # Define ring which to Extrude by translation.
    c_inner = add_circle(inner_radius, lcar,
                         R = np.eye(3),
                         x0 = np.array([0.0, 0.0, 0.0])
                         )
    ll_inner = LineLoop(c_inner)

    c_outer = add_circle(outer_radius, lcar,
                         R = np.eye(3),
                         x0 = np.array([0.0, 0.0, 0.0])
                         )
    ll_outer = LineLoop(c_outer)

    surf = PlaneSurface(','.join([ll_outer, ll_inner]))

    # Now Extrude the ring surface.
    name = Extrude_translate('Surface{%s}' % surf, [1, 0, 0])
    vol = name + '[0]'

    return vol
# -----------------------------------------------------------------------------
