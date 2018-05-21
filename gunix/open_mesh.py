#!/usr/bin/python
# -*- coding: utf-8 -*-
#
import numpy as np
import pygmsh


def test():
    # Characteristic length
    lcar = 1#e-1

    # Coordinates of lower-left and upper-right vertices of a square domain
    xmin = 0.0
    xmax = 5.0
    ymin = 0.0
    ymax = 5.0

    # Vertices of a square hole
    squareHoleCoordinates = np.array([
        [1, 1, 0],
        [4, 1, 0],
        [4, 4, 0],
        [1, 4, 0]
        ])

    # Create geometric object
    geom = pygmsh.built_in.Geometry()

    # Create square hole
    squareHole = geom.add_polygon(
        squareHoleCoordinates, lcar,
        make_surface=False
        )

    # Create square domain with square hole
    geom.add_rectangle(
        xmin, xmax, ymin, ymax, 0.0, lcar,
        holes=[squareHole.line_loop]
        )

    points, cells, point_data, cell_data, field_data = pygmsh.generate_mesh(geom)
    """
    print 'points'
    print points
    print 'cells'
    print cells
    print 'point data'
    print point_data
    print 'field_data'
    print field_data
    # TODO support for volumes of triangle6
    # ref = 16.0
    # from helpers import compute_volume
    # assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    """
    return points, cells

def view_mesh():
    pass


if __name__ == '__main__':
    import meshio
    meshio.write('hole_in_square.vtu', *test())
    view_mesh()
