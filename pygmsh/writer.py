# -*- coding: utf-8 -*-
#
import numpy
import os
import re


def write(filename,
          points,
          cells,
          point_data=None,
          cell_data=None,
          field_data=None
          ):
    '''Writes mesh together with data to a file.

    :params filename: File to write to.
    :type filename: str

    :params point_data: Named additional point data to write to the file.
    :type point_data: dict
    '''
    extension = os.path.splitext(filename)[1]

    if extension == '.msh':
        _write_gmsh(filename, points, cells)
        return
    else:
        vtk_mesh = _generate_vtk_mesh(points, cells)
        # add point data
        if point_data:
            for name, X in point_data.iteritems():
                # There is a naming inconsistency in VTK when it comes to
                # multivectors in Exodus files:
                # If a vector 'v' has two components, they are called 'v_r',
                # 'v_z' (note the underscore), if it has three, then they are
                # called 'vx', 'vy', 'vz'.  Make this consistent by appending
                # an underscore if needed.  Note that for VTK files, this
                # problem does not occur since the label of a vector is always
                # stored as a string.
                is_exodus_format = extension in ['.ex2', '.exo', '.e']
                if is_exodus_format and len(X.shape) == 2 \
                   and X.shape[1] == 3 and name[-1] != '_':
                    name += '_'
                vtk_mesh.GetPointData() \
                        .AddArray(_create_vtkarray(X, name))

        # add cell data
        if cell_data:
            for key, value in cell_data.iteritems():
                vtk_mesh.GetCellData() \
                        .AddArray(_create_vtkarray(value, key))

        # add field data
        if field_data:
            for key, value in field_data.iteritems():
                vtk_mesh.GetFieldData() \
                        .AddArray(_create_vtkarray(value, key))

        if extension == '.vtu':  # VTK XML format
            from vtk import vtkXMLUnstructuredGridWriter
            writer = vtkXMLUnstructuredGridWriter()
        elif extension == '.pvtu':  # parallel VTK XML format
            from vtk import vtkXMLPUnstructuredGridWriter
            writer = vtkXMLPUnstructuredGridWriter()
        elif extension == '.vtk':  # classical VTK format
            from vtk import vtkUnstructuredGridWriter
            writer = vtkUnstructuredGridWriter()
            writer.SetFileTypeToASCII()
        elif extension in ['.ex2', '.exo', '.e']:  # Exodus II format
            from vtk import vtkExodusIIWriter
            writer = vtkExodusIIWriter()
            # If the mesh contains vtkModelData information, make use of it
            # and write out all time steps.
            writer.WriteAllTimeStepsOn()
        elif re.match('[^\.]*\.e\.\d+\.\d+', filename):
            # TODO handle parallel I/O with vtkPExodusIIWriter
            from vtk import vtkExodusIIWriter
            writer = vtkExodusIIWriter()
            # If the mesh contains vtkModelData information, make use of it
            # and write out all time steps.
            writer.WriteAllTimeStepsOn()
        else:
            raise IOError('Unknown file type \'%s\'.' % filename)
        writer.SetFileName(filename)
        writer.SetInput(vtk_mesh)
        writer.Write()
        return


def _write_gmsh(filename, points, cells):
    raise NotImplementedError()


def _generate_vtk_mesh(points, cellsNodes):
    from vtk import vtkUnstructuredGrid, VTK_TRIANGLE, VTK_TETRA, \
        vtkIdList, vtkPoints
    mesh = vtkUnstructuredGrid()

    # set points
    vtk_points = vtkPoints()
    if len(points[0]) == 2:
        for point in points:
            vtk_points.InsertNextPoint(point[0], point[1], 0.0)
    elif len(points[0]) == 3:
        for point in points:
            vtk_points.InsertNextPoint(point[0], point[1], point[2])
    else:
        raise RuntimeError('???')
    mesh.SetPoints(vtk_points)

    # set cells
    for cellNodes in cellsNodes:
        pts = vtkIdList()
        num_local_nodes = len(cellNodes)
        pts.SetNumberOfIds(num_local_nodes)
        # Get the connectivity for this element.
        for k, node_index in enumerate(cellNodes):
            pts.InsertId(k, node_index)

        if num_local_nodes == 3:
            cell_type = VTK_TRIANGLE
        elif num_local_nodes == 4:
            cell_type = VTK_TETRA
        else:
            raise RuntimeError('???')

        mesh.InsertNextCell(cell_type, pts)
    return mesh


def recreate_cells_with_qhull(nodes):
    '''Remesh using scipy.spatial.Delaunay.
    '''
    import scipy.spatial
    # Create a Delaunay triangulation of the given points.
    delaunay = scipy.spatial.Delaunay(nodes)
    # Use the new cells.
    return delaunay.vertices


def _create_vtkarray(X, name):
    from vtk import vtkBitArray, vtkIntArray, vtkDoubleArray, vtkCharArray

    # If something isn't a Numpy array already, try to make it one.
    if not isinstance(X, numpy.ndarray) and not isinstance(X, str):
        X = numpy.array(X)

    # This could be a lot more fine-grained:
    # vtkLongLongArray, vtkFloatArray,...
    if isinstance(X, str) or X.dtype.kind == 'S':
        array = vtkCharArray()
    elif X.dtype == bool:
        array = vtkBitArray()
    elif X.dtype == int:
        array = vtkIntArray()
    elif X.dtype == float:
        array = vtkDoubleArray()
    elif X.dtype == complex:
        # Convert complex arrays to double.
        Y = numpy.empty((len(X), 2), dtype=float)
        if len(X.shape) == 1:
            Y[:, 0] = X.real
            Y[:, 1] = X.imag
        elif len(X.shape) == 2:
            Y[:, 0] = X[:, 0].real
            Y[:, 1] = X[:, 0].imag
        else:
            raise RuntimeError()
        X = Y
        array = vtkDoubleArray()
    else:
        raise TypeError('Unknown VTK data type', X.dtype, '.')

    # For some reason, setting the number of tuples and then using
    # SetNextTuple() or similar doesn't seem to work:
    # The application segfaults or, worse, yields an irrecoverable
    # glibc memory corruption.
    # Most likely the cause: You have to call SetNumberOfTuples()
    # AFTER SetNumberOfComponents().
    #   array.SetNumberOfTuples(X.shape[0])
    # Special treatment for strings:
    if isinstance(X, str):
        array.SetNumberOfComponents(len(X))
        array.SetNumberOfTuples(1)
        array.SetTupleValue(0, X)
    elif len(X.shape) == 0:
        array.SetNumberOfComponents(1)
        # Set values.
        array.InsertNextValue(X)
    elif len(X.shape) == 1:
        array.SetNumberOfComponents(1)
        # Set values.
        for k in range(X.shape[0]):
            array.InsertNextValue(X[k])
    elif len(X.shape) == 2:
        array.SetNumberOfComponents(X.shape[1])
        # Set values.
        for k in range(X.shape[0]):
            for k2 in range(X.shape[1]):
                array.InsertNextValue(X[k][k2])
    else:
        raise ValueError('Don''t know what to do with '
                         'many-dimensional array ''%s''.' % name
                         )

    array.SetName(name)

    return array
