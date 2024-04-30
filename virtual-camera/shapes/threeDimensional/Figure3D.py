from typing import List

import numpy as np
import pygame

from shapes.threeDimensional.Wall3D import Wall3D
from view.Perspective import Perspective
from shapes.threeDimensional.Edge3D import Edge3D
from shapes.threeDimensional.Point3D import Point3D
from shapes.twoDimensional.Figure2D import Figure2D


class Figure3D:
    __points: List[Point3D]
    __edges: List[Edge3D]
    __walls: List[Wall3D]

    def __init__(self, edges: List[Edge3D], walls: List[Wall3D]):
        self.__points = list({edge.get_point1() for edge in edges} | {edge.get_point2() for edge in edges})
        self.__edges = edges
        self.__walls = walls

    def get_points(self):
        return self.__points

    def get_edges(self):
        return self.__edges

    def get_walls(self):
        return self.__walls

    def translate(self, vector: np.array([int, int, int])):
        for point in self.__points:
            point.translate(vector)

    def rotate(self, degree: float, axis: str):
        for point in self.__points:
            point.rotate(degree, axis)

    def draw_edges(self, screen, perspective):
        print(len(self.__edges))
        print(',\n'.join([str(edge) for edge in self.__edges]))
        figure_2d = self.__transform_to_2d(screen, perspective)
        print(',\n'.join([str(edge) for edge in figure_2d.get_edges()]))
        figure_2d.draw_edges(screen)

    def get_visible_polygons(self):
        return [wall for wall in self.__walls if wall.is_visible()]

    def __transform_to_2d(self, screen: pygame.Surface, perspective: Perspective):
        return Figure2D([edge.transform_to_2d(screen, perspective) for edge in self.__edges if edge.is_visible()])
