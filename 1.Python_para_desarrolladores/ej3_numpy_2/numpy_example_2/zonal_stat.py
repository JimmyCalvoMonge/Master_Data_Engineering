import numpy as np


def read_data(fname: str, tipo: type) -> np.ndarray:
    """
    Reads a text file containing data and creates a numpy array of the given datatype.
    :param fname: str
        a path containing the .txt file to read
    :param tipo: type
        a data type to create the numpy array

    Examples:
    --------

    >>> read_data('./datos/valores.txt', float)
    array([[5., 3., 4., 4., 4., 2.],
           [2., 1., 4., 2., 6., 3.],
           [8., 4., 3., 5., 3., 1.],
           [4., 2., 4., 3., 2., 2.],
           [6., 3., 3., 7., 4., 2.],
           [5., 5., 2., 3., 1., 3.]])
    >>> read_data('./datos/zonas.txt', int)
    array([[1, 1, 1, 1, 3, 3],
           [1, 1, 1, 1, 3, 1],
           [2, 2, 3, 3, 3, 4],
           [2, 2, 3, 3, 3, 4],
           [2, 2, 3, 3, 2, 2],
           [3, 3, 3, 3, 3, 2]])
    """
    return np.loadtxt(fname=fname).astype(tipo)  # Otra opción es np.loadtxt(fname=fname, dtype=tipo), pero me da un warning de numpy.


def set_of_areas(zonas: np.ndarray)-> set[int]:
    """
    Calculates a set containing the unique zones in the zonas array
    :param zonas:  np.ndarray
        a numpy array of integers containing zone codes as integers.
    :raise TypeError: if cells are not integers in the zonas input.
    Examples:
    --------
    >>> set_of_areas(np.arange(10).reshape(5, 2))
    {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    >>> set_of_areas(np.zeros(10, dtype=np.int_).reshape(5, 2))
    {0}
    >>> set_of_areas(np.array([2, 3, 4, 2, 3, 4], dtype=np.int_).reshape(3, 2))
    {2, 3, 4}
    >>> set_of_areas(np.zeros(3, dtype=np.float_))
    Traceback (most recent call last):
        ...
    TypeError: The elements type must be int, not float64
    """
    if np.issubdtype(zonas.dtype, int):
        return set(np.unique(zonas))
    else:
        raise TypeError("The elements type must be int, not float64")


def mean_areas(zonas: np.ndarray, valores: np.ndarray) -> np.ndarray:

    """
    Calculates new array where the [i,j] entry contains the means of all the entries 
    of valores, whose corresponding entry in zonas equals the zone of the [i,j] array.
    :param zonas:  np.ndarray
        a numpy array of integers containing zone codes as integers.
    :param valores:  np.ndarray
        a numpy array of numbers containing values for each cell as float numbers.
    :raise ndexError: if both input arrays don't have the same size.
    Examples:
    --------
    >>> mean_areas(read_data('./datos/zonas.txt', int), read_data('./datos/valores.txt', float))
    array([[3.1, 3.1, 3.1, 3.1, 3.6, 3.6],
           [3.1, 3.1, 3.1, 3.1, 3.6, 3.1],
           [4. , 4. , 3.6, 3.6, 3.6, 1.5],
           [4. , 4. , 3.6, 3.6, 3.6, 1.5],
           [4. , 4. , 3.6, 3.6, 4. , 4. ],
           [3.6, 3.6, 3.6, 3.6, 3.6, 4. ]])
    >>> mean_areas(read_data('./datos/zonas2.txt', int), read_data('./datos/valores2.txt', float))
    array([[1. , 2. , 2. , 2. , 2. , 2. ],
           [1. , 1.2, 1.2, 1.2, 1.2, 1.2],
           [1. , 5. , 5. , 5. , 5. , 4.4],
           [1. , 5. , 5. , 5. , 5. , 4.4],
           [1. , 6. , 6. , 6. , 6. , 4.4],
           [1. , 0. , 0.8, 0.8, 0.8, 4.4],
           [1. , 0. , 0.8, 0.8, 0.8, 4.4],
           [1. , 0. , 0.8, 0.8, 0.8, 4.4],
           [1. , 0. , 0.8, 0.8, 0.8, 4.4],
           [1. , 0. , 0. , 0. , 0. , 4.4]])
    """

    if zonas.shape != valores.shape:
        raise IndexError("Los arrays proporcionados deben tener las mismas dimensiones")
    else:

        output = np.zeros(zonas.shape)

        # Obtenemos las diferentes zonas que hay en el array de zonas:
        all_zones = np.unique(zonas)

        # Para cada zona obtenemos los indices que tienen esta zona.
        # Y cambiamos estos indices en output.

        for zone in all_zones:
            idx_zone = zonas == zone
            mean_zone = np.around(np.mean(valores[idx_zone]), 1)
            output[idx_zone] = mean_zone

        return output

# ------------ test  --------#
import doctest

def test_doc()-> None:
    """
    The following instructions are to execute the tests of same functions
    If any test is fail, we will receive the notice when executing
    :return: None
    """
    doctest.run_docstring_examples(read_data, globals(), verbose=False)  # vemos los resultados de los test que fallan
    doctest.run_docstring_examples(set_of_areas, globals(), verbose=False)  # vemos los resultados de los test que fallan
    doctest.run_docstring_examples(mean_areas, globals(), verbose=True)  # vemos los resultados de los test que fallan


if __name__ == "__main__":
    test_doc()   # executing tests
