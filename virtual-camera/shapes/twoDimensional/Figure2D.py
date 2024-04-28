from typing import List

from shapes.twoDimensional.Edge2D import Edge2D
from shapes.twoDimensional.Point2D import Point2D


class Figure2D:
    __points: List[Point2D]
    __edges: List[Edge2D]

    def __init__(self, points: List[Point2D], edges: List[Edge2D]):
        self.__points = points
        self.__edges = edges

    def __init__(self, edges: List[Edge2D]):
        self.__points = list({edge.get_point1() for edge in edges} | {edge.get_point2() for edge in edges})
        self.__edges = edges

    def get_points(self):
        return self.__points

    def get_edges(self):
        return self.__edges

    def draw_edges(self, screen):
        for edge in self.__edges:
            edge.draw(screen)
