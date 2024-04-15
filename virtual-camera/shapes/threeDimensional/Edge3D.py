from dataclasses import dataclass

import numpy as np
import pygame as pygame

from shapes.threeDimensional.Point3D import Point3D
from shapes.twoDimensional.Edge2D import Edge2D
from shapes.twoDimensional.Point2D import Point2D
from view.Perspective import Perspective


@dataclass
class Edge3D:
    __point1: Point3D
    __point2: Point3D
    __color: pygame.Color

    def get_point1(self):
        return self.__point1

    def get_point2(self):
        return self.__point2

    def get_color(self):
        return self.__color

    def translate(self, vector: np.array([int, int, int])):
        self.__point1.translate(vector)
        self.__point2.translate(vector)

    def rotate(self, degree: float, axis: str):
        self.__point1.rotate(degree, axis)
        self.__point2.rotate(degree, axis)

    def is_visible(self):
        return self.__point1.get_z() > 0 or self.__point2.get_z() > 0

    def __is_partially_invisible(self):
        return self.__point1.get_z() <= 0 or self.__point2.get_z() <= 0

    def transform_to_2d(self, screen: pygame.Surface, perspective: Perspective):
        if not self.is_visible():
            raise ValueError("Edge is not visible")

        point1_2d = self.__point1.transform_to_2d(perspective, screen)
        point2_2d = self.__point2.transform_to_2d(perspective, screen)
        if self.__is_partially_invisible():
            Edge3D.__cut_edge_to_screen_size(point1_2d, point2_2d, screen)
            return Edge2D(point1_2d, point2_2d, self.__color)

        return Edge2D(point1_2d, point2_2d, self.__color)

    # Liang-Barsky algorithm for 2d
    @staticmethod
    def __cut_edge_to_screen_size(point1: Point2D, point2: Point2D, screen: pygame.Surface):
        x1, y1 = point1.get_x(), point1.get_y()
        x2, y2 = point2.get_x(), point2.get_y()
        dx = x2 - x1
        dy = y2 - y1
        x_min, y_min = 0, 0
        x_max, y_max = screen.get_width(), screen.get_height()

        p = [-dx, dx, -dy, dy]
        q = [point1.get_x() - x_min, x_max - point1.get_x(), point1.get_y() - y_min, y_max - point1.get_y()]
        t_enter = 0.0
        t_exit = 1.0

        for i in range(4):
            if p[i] == 0:  # Check if line is parallel to the clipping boundary
                if q[i] < 0:
                    return  # Line is outside and parallel, so completely discarded
            else:
                t = q[i] / p[i]
                if p[i] < 0:
                    if t > t_enter:
                        t_enter = t
                else:
                    if t < t_exit:
                        t_exit = t
        if t_enter > t_exit:
            return  # Line is completely outside

        point1.set_x(x1 + t_enter * dx)
        point1.set_y(y1 + t_enter * dy)
        point2.set_x(x1 + t_exit * dx)
        point2.set_y(y1 + t_exit * dy)
