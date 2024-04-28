import numpy as np


class Plane:
    # a*x + b*y + c*z + distance = 0
    __x: float
    __y: float
    __z: float
    __distance: float

    def __init__(self, x: float, y: float, z: float, distance: float):
        self.__x = x
        self.__y = y
        self.__z = z
        self.__distance = distance

    def get_x(self) -> float:
        return self.__x

    def get_y(self) -> float:
        return self.__y

    def get_z(self) -> float:
        return self.__z

    def get_distance(self) -> float:
        return self.__distance

    def get_normal(self) -> np.array:
        return np.array([self.__x, self.__y, self.__z])
