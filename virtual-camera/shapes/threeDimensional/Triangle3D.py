from typing import List

import pygame

from shapes.threeDimensional.Edge3D import Edge3D
from shapes.threeDimensional.Point3D import Point3D


class Triangle3D:
    __points: List[Point3D]
    __edges: List[Edge3D]
    __color: pygame.Color

    def __init__(self, edges: List[Edge3D], color: pygame.Color):
        self.__edges = edges
        self.__color = color
        self.__points = list({edge.get_point1() for edge in edges} | {edge.get_point2() for edge in edges})
