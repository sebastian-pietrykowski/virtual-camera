from typing import List

import numpy as np
import pygame

from shapes.threeDimensional.Edge3D import Edge3D
from shapes.threeDimensional.Point3D import Point3D
from view.Perspective import Perspective


class Wall3D:
    __points: List[Point3D]
    __edges: List[Edge3D]
    __color: pygame.Color

    __TRIANGLE_MAX_DISTANCE = 10

    def __str__(self):
        return f"Wall3D({', '.join(str(edge) for edge in self.__edges)})" \
               f", edges count: {len(self.__edges)}" \
               f", points count: {len(self.__points)})"

    def __init__(self, edges: List[Edge3D], color: pygame.Color):
        if len(edges) < 3:
            raise ValueError("Wall must have at least 3 edges")

        self.__edges = edges
        self.__color = color
        self.__points = Point3D.get_points_from_edges(edges)

    def get_points(self):
        return self.__points

    def get_edges(self):
        return self.__edges

    def get_color(self):
        return self.__color

    def is_visible(self) -> bool:
        return any(point.is_visible() for point in self.__points)

    def draw(self, screen: pygame.Surface, perspective: Perspective):
        edges_2d = [edge.transform_to_2d(screen, perspective) for edge in self.__edges]
        points_2d_tuples = list((point.get_x(), point.get_y()) for edge in edges_2d for point in edge.get_points())
        center = (screen.get_width()/2 + screen.get_width()/2)

        if len(points_2d_tuples) >= 3:
            pygame.draw.polygon(screen, self.__color, points_2d_tuples)
            pygame.draw.aalines(screen, (255, 255, 255), True, points_2d_tuples)
            pygame.display.update()

    def calculate_normal_vector(self) -> np.array([int, int, int]):
        point1 = self.__points[0].get_vector()[:3]
        point2 = self.__points[1].get_vector()[:3]
        point3 = self.__points[2].get_vector()[:3]

        vector1 = point2 - point1
        vector2 = point3 - point1

        return np.cross(vector1, vector2)

    def is_in_front_of_partition_wall(self, partition_wall: 'Wall3D') -> bool:
        normal_vector = partition_wall.calculate_normal_vector()
        for point in self.__points:
            if (point.get_vector()[:3] - partition_wall.get_points()[0].get_vector()[:3]) @ normal_vector < 0:
                return False
        return True

    def is_behind_partition_wall(self, partition_wall: 'Wall3D') -> bool:
        normal_vector = partition_wall.calculate_normal_vector()
        for point in self.__points:
            if (point.get_vector()[:3] - partition_wall.get_points()[0].get_vector()[:3]) @ normal_vector > 0:
                return False
        return True
