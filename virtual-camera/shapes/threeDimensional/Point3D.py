import numpy as np
import pygame

from view.Perspective import Perspective
from shapes.PointTransformer import PointTransformer


class Point3D:
    __vector: np.array([int, int, int, int])

    def __init__(self, x: int, y: int, z: int):
        self.__vector = np.array([x, y, z, 1])

    def get_vector(self):
        return self.__vector

    def get_x(self):
        return self.__vector[0]

    def get_y(self):
        return self.__vector[1]

    def get_z(self):
        return self.__vector[2]

    def set_z(self, z: int):
        self.__vector[2] = z

    def translate(self, vector: np.array([int, int, int])):
        self.__vector = PointTransformer.translate(self, vector)

    def rotate(self, degree: float, axis: str):
        self.__vector = PointTransformer.rotate(self, degree, axis)

    def transform_to_2d(self, perspective: Perspective, screen: pygame.Surface):
        return PointTransformer.transform_from_3d_to_2d(self, perspective, screen)
