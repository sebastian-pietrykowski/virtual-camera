import numpy as np


class Point2D:
    __vector: np.array([int, int, int])

    def __init__(self, x: int, y: int):
        self.__vector = np.array([x, y, 1])

    def get_vector(self):
        return self.__vector

    def get_x(self):
        return self.__vector[0]

    def set_x(self, x: int):
        self.__vector[0] = x

    def get_y(self):
        return self.__vector[1]

    def set_y(self, y: int):
        self.__vector[1] = y
