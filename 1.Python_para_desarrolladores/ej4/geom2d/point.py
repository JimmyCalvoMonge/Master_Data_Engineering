from .vector import Vector
import math
from typing import Self

class Point():
    
    def __init__(self, x: float, y:float):
        # _x, _y son atributos privados.
        self._x:float = x
        self._y:float = y
    
    """
    Getters, similares a los de la clase Vector
    """

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    """
    Setters, seguimos la recomendación del ultimo video y agregamos
    un decorador setter
    """

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    @property
    def mod(self) -> float:
        """
        Tiene sentido decir que un punto no tiene longitud (?)
        """
        return 0

    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y

    def __le__(self, other: Self) -> bool:
        return self.mod <= other.mod

    def __hash__(self):
        """
        El hash debe ser modificado para que se
        pueda distinguir un punto de un vector.
        Para ello agregamos una tercera coordenada que los diferencie.
        """
        return hash((self.x, self.y, 'Point'))

    def __sub__(self, other: Self) -> Vector:
        """
        Resta de puntos
        b.__sub__(a) debe ser el vector que va de a a b
        Es decir, el vector con entradas (b.x - a.x, b.y - a.y)
        """
        return Vector(self.x - other.x, self.y - other.y)
    
    def distance(self, other: Self) -> float:
        """
        Distancia entre dos puntos
        """
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    """
    Métodos repr y str
    Similares a los de Vector que hemos visto en clase.
    """

    def __repr__(self) -> str:
        return f'P({self.x}, {self.y})'

    def __str__(self) -> str:
        return f'({self.x:.4f}, {self.y:.4f})'

def str_vs_repr():
    v = Vector(math.pi/2, math.pi)
    print(f'El vector {v} tiene modulo {v.mod}')
    print(repr(v))


def arithmetic():
    v1 = Vector(1, 0)
    v2 = Vector(0, -1)
    lam = 2.0
    print(f'{v1} + {v2} = {v1 + v2}')
    print(f'{v1} - {v2} = {v1 - v2}')
    print(f'-{v1} = {-v1}')
    print(f'{v1} * {v2} = {v1 * v2}')
    print(f'{lam} * {v1} = {lam * v1}')

def test_hash():
    svector = { Vector(1,0), Vector(0,1) }
    print(Vector(1.0, 0.0) == Vector(1, 0), Vector(1.0, 0.0) in svector)
    print(Vector(0, 1.0) == Vector(0, 1),Vector(0, 1.0) in svector)


def comparison():
    pairs = [(Vector(1.0, 1.0), Vector(1.0, 1.0)),
             (Vector(1.0, 0.5), Vector(1.0, 1.0)),
             (Vector(1.0, 1.5), Vector(1.0, 1.0)),
             ]

    for v1, v2 in pairs:
        print(f'{v1}=={v2}: {v1==v2}')
        print(f'{v1}<={v2}: {v1<=v2}')

        try:
            print(f'{v1}<{v2}: {v1<v2}')
        except TypeError as e:
            print(f"excepción capturada: {e}")

def main():
    v = Vector(2.0, 3.0)
    print(f'El vector {v} tiene modulo {v.mod}')
    print(repr(v))

    pairs = [(Vector(1.0, 1.0), Vector(1.0, 1.0)),
             (Vector(1.0, 0.5), Vector(1.0, 1.0)),
             (Vector(1.0, 1.5), Vector(1.0, 1.0)),
             ]

    for v1, v2 in pairs:
        print(f'{v1}=={v2}: {v1==v2}')
        print(f'{v1}<={v2}: {v1<=v2}')

        try:
            print(f'{v1}<{v2}: {v1<v2}')
        except TypeError as e:
            print(f"excepción capturada: {e}")