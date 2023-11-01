"""
Prueba de import del paquete geom2d
"""

from geom2d import Point

if __name__ == '__main__':

    point_1 = Point(5,6)
    point_2 = Point(1,2)
    print(point_1.distance(point_2))