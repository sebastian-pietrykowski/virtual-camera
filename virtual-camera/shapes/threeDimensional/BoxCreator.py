import numpy as np
import pygame

from shapes.threeDimensional.Edge3D import Edge3D
from shapes.threeDimensional.Figure3D import Figure3D
from shapes.threeDimensional.Point3D import Point3D
from shapes.threeDimensional.Wall3D import Wall3D


class BoxCreator:
    __start_point: Point3D
    __width: int
    __height: int
    __depth: int
    __color: pygame.Color

    def __init__(self, start_point: Point3D, width: int, height: int, depth: int, color: pygame.Color):
        self.__start_point = start_point
        self.__width = width
        self.__height = height
        self.__depth = depth
        self.__color = color

    def create_box(self):
        points = self.__create_points()
        edges_dict = self.__create_edges_dict(points)

        edges = [
            edges_dict['bottom_left_front_to_bottom_right_front'],
            edges_dict['bottom_right_front_to_bottom_right_back'],
            edges_dict['bottom_right_back_to_bottom_left_back'],
            edges_dict['bottom_left_back_to_bottom_left_front'],

            edges_dict['top_left_front_to_top_right_front'],
            edges_dict['top_right_front_to_top_right_back'],
            edges_dict['top_right_back_to_top_left_back'],
            edges_dict['top_left_back_to_top_left_front'],

            edges_dict['bottom_left_front_to_top_left_front'],
            edges_dict['bottom_right_front_to_top_right_front'],
            edges_dict['bottom_right_back_to_top_right_back'],
            edges_dict['bottom_left_back_to_top_left_back'],
        ]

        walls = [
            Wall3D([edges_dict['bottom_left_front_to_bottom_right_front'],
                    edges_dict['bottom_right_front_to_bottom_right_back'],
                    edges_dict['bottom_right_back_to_bottom_left_back'],
                    edges_dict['bottom_left_back_to_bottom_left_front']], np.random.choice(range(256), size=3)),
            # bottom
            Wall3D([edges_dict['top_left_front_to_top_right_front'], edges_dict['top_right_front_to_top_right_back'],
                    edges_dict['top_right_back_to_top_left_back'], edges_dict['top_left_back_to_top_left_front']],
                   np.random.choice(range(256), size=3)),  # top
            Wall3D([edges_dict['bottom_left_front_to_bottom_right_front'],
                    edges_dict['bottom_right_front_to_top_right_front'],
                    edges_dict['top_right_front_to_top_left_front'], edges_dict['top_left_front_to_bottom_left_front']],
                   np.random.choice(range(256), size=3)),  # front
            Wall3D(
                [edges_dict['bottom_left_front_to_bottom_left_back'], edges_dict['bottom_left_back_to_top_left_back'],
                 edges_dict['top_left_back_to_top_left_front'], edges_dict['top_left_front_to_bottom_left_front']],
                np.random.choice(range(256), size=3)),  # left
            Wall3D(
                [edges_dict['bottom_left_back_to_bottom_right_back'], edges_dict['bottom_right_back_to_top_right_back'],
                 edges_dict['top_right_back_to_top_left_back'], edges_dict['top_left_back_to_bottom_left_back']],
                np.random.choice(range(256), size=3)),  # back
            Wall3D([edges_dict['bottom_right_front_to_bottom_right_back'],
                    edges_dict['bottom_right_back_to_top_right_back'], edges_dict['top_right_back_to_top_right_front'],
                    edges_dict['top_right_front_to_bottom_right_front']], np.random.choice(range(256), size=3)),
            # right
        ]

        return Figure3D(edges, walls)

    def __create_points(self) -> dict[str, Point3D]:
        x, y, z = self.__start_point.get_x(), self.__start_point.get_y(), self.__start_point.get_z()
        return {
            'bottom_left_front': self.__start_point,
            'bottom_right_front': Point3D(x + self.__width, y, z),
            'bottom_left_back': Point3D(x, y, z + self.__depth),
            'bottom_right_back': Point3D(x + self.__width, y, z + self.__depth),
            'top_left_front': Point3D(x, y + self.__height, z),
            'top_right_front': Point3D(x + self.__width, y + self.__height, z),
            'top_left_back': Point3D(x, y + self.__height, z + self.__depth),
            'top_right_back': Point3D(x + self.__width, y + self.__height, z + self.__depth),
        }

    def __create_edges_dict(self, points: dict[str, Point3D]) -> dict[str, Edge3D]:
        return {
            f'{p1}_to_{p2}': Edge3D(points[p1], points[p2], self.__color)
            for p1, p2 in [
                ('bottom_left_front', 'bottom_right_front'),
                ('bottom_right_front', 'bottom_right_back'),
                ('bottom_right_back', 'bottom_left_back'),
                ('bottom_left_back', 'bottom_left_front'),
                ('top_left_front', 'top_right_front'),
                ('top_right_front', 'top_right_back'),
                ('top_right_back', 'top_left_back'),
                ('top_left_back', 'top_left_front'),
                ('bottom_left_front', 'bottom_left_back'),
                ('top_left_front', 'top_left_back'),
                ('bottom_right_front', 'bottom_right_back'),
                ('bottom_right_front', 'top_right_front'),
                ('top_right_front', 'top_left_front'),
                ('top_left_front', 'bottom_left_front'),
                ('bottom_left_back', 'top_left_back'),
                ('bottom_left_back', 'bottom_right_back'),
                ('bottom_right_back', 'top_right_back'),
                ('top_left_back', 'bottom_left_back'),
                ('top_right_back', 'top_right_front'),
                ('top_right_front', 'bottom_right_front'),
                ('bottom_right_front', 'bottom_right_back'),
                ('bottom_left_front', 'top_left_front'),
            ]
        }

