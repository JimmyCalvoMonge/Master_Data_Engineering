import os
import pytest
from geom2d import *

"""
Testing distance between two points
"""

@pytest.mark.parametrize(
      "x_coord_1, y_coord_1, x_coord_2, y_coord_2, distance", [
          (1,2,1,2,0),
          (2,3,4,5,2.8284271247461903)
      ]
)

def test_point_distance(x_coord_1, y_coord_1, x_coord_2, y_coord_2, distance):
    assert Point(x_coord_1, y_coord_1).distance(Point(x_coord_2, y_coord_2)) == distance

"""
Testing that the hash method is able to diferentiate point from vector
"""

@pytest.mark.parametrize(
      "point, vector", [
          (Point(1,2), Vector(1,2)),
          (Point(2,3), Vector(4,5))
      ]
)

def test_hash(point, vector):
    assert point.__hash__ != vector.__hash__


"""
Testing the difference between two points
"""

@pytest.mark.parametrize(
      "point1, point2, expected", [
          (Point(1,2), Point(1,2), Vector(0,0)),
          (Point(4,5), Point(1,3), Vector(3,2))
      ]
)

def test_point_difference(point1, point2, expected):
    assert point1.__sub__(point2) == expected


"""
Testing vector sizes
"""

@pytest.mark.parametrize(
      "vector1, vector2", [
          (Vector(0,0), Vector(1,4)),
          (Vector(3,2), Vector(3, 10))
      ]
)

def test_vector_sizes(vector1, vector2):
    assert vector1 <= vector2