from typing import List

import pygame

from shapes.threeDimensional.Edge3D import Edge3D
from shapes.threeDimensional.Point3D import Point3D


class Wall3D:
    __points: set[Point3D]
    __edges: List[Edge3D]
    __color: pygame.Color

    def __str__(self):
        return f"Wall3D({', '.join(str(edge) for edge in self.__edges)})" \
               f", edges count: {len(self.__edges)}" \
               f", points count: {len(self.__points)})"

    def __init__(self, edges: List[Edge3D], color: pygame.Color):
        self.__edges = edges
        self.__color = color
        self.__points = set({edge.get_point1() for edge in edges} | {edge.get_point2() for edge in edges})

    def get_points(self):
        return self.__points

    def get_edges(self):
        return self.__edges

    def get_color(self):
        return self.__color
