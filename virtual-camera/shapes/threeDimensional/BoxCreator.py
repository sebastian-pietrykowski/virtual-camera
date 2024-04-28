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
        x, y, z = self.__start_point.get_x(), self.__start_point.get_y(), self.__start_point.get_z()
        point000 = Point3D(x, y, z)
        point100 = Point3D(x + self.__width, y, z)
        point101 = Point3D(x + self.__width, y, z + self.__depth)
        point001 = Point3D(x, y, z + self.__depth)
        point010 = Point3D(x, y + self.__height, z)
        point110 = Point3D(x + self.__width, y + self.__height, z)
        point111 = Point3D(x + self.__width, y + self.__height, z + self.__depth)
        point011 = Point3D(x, y + self.__height, z + self.__depth)
        # points = [
        #     point000, point100, point101, point001,
        #     point010, point110, point111, point011
        # ]

        edge000to100 = Edge3D(point000, point100, self.__color)
        edge100to101 = Edge3D(point100, point101, self.__color)
        edge101to001 = Edge3D(point101, point001, self.__color)
        edge001to000 = Edge3D(point001, point000, self.__color)
        edge010to110 = Edge3D(point010, point110, self.__color)
        edge110to111 = Edge3D(point110, point111, self.__color)
        edge111to011 = Edge3D(point111, point011, self.__color)
        edge011to010 = Edge3D(point011, point010, self.__color)
        edge100to110 = Edge3D(point100, point110, self.__color)
        edge110to010 = Edge3D(point110, point010, self.__color)
        edge010to000 = Edge3D(point010, point000, self.__color)
        edge000to001 = Edge3D(point000, point001, self.__color)
        edge001to011 = Edge3D(point001, point011, self.__color)
        edge001to101 = Edge3D(point001, point101, self.__color)
        edge101to111 = Edge3D(point101, point111, self.__color)
        edge011to001 = Edge3D(point011, point001, self.__color)
        edge111to110 = Edge3D(point111, point110, self.__color)
        edge110to100 = Edge3D(point110, point100, self.__color)

        edges = [
            edge000to100, edge100to101, edge101to001, edge001to000,
            edge010to110, edge110to111, edge111to011, edge011to010,
            edge000to001, edge100to101, edge011to010, edge110to111,
        ]

        walls = [
            Wall3D([edge000to100, edge100to101, edge101to001, edge001to000], np.random.choice(range(256), size=3)),  # bottom
            Wall3D([edge010to110, edge110to111, edge111to011, edge011to010], np.random.choice(range(256), size=3)),  # top
            Wall3D([edge000to100, edge100to110, edge110to010, edge010to000], np.random.choice(range(256), size=3)),  # front
            Wall3D([edge000to001, edge001to011, edge011to010, edge010to000], np.random.choice(range(256), size=3)),  # left
            Wall3D([edge001to101, edge101to111, edge111to011, edge011to001], np.random.choice(range(256), size=3)),  # back
            Wall3D([edge100to101, edge101to111, edge111to110, edge110to100], np.random.choice(range(256), size=3)),  # right
        ]

        return Figure3D(edges, walls)
        # points = self.__create_points()
        # edges_dict = self.__create_edges_dict(points)
        # walls = self.__create_walls(points, edges_dict)
        #
        # return Figure3D(list(edges_dict.values()), walls)

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
                ('bottom_left_front', 'top_left_front'),
                ('top_right_front', 'bottom_right_front'),
                ('bottom_right_front', 'bottom_left_front'),
                ('bottom_right_back', 'top_right_back'),
                ('top_left_back', 'bottom_left_back'),
                ('bottom_left_back', 'bottom_right_back'),
                ('bottom_left_front', 'bottom_left_back'),
                ('bottom_left_back', 'top_left_back'),
                ('top_left_front', 'bottom_left_front'),
                ('top_right_back', 'top_right_front'),
            ]
        }

    # def __create_walls(self, points: dict[str, Point3D], edges_dict: dict[str, Edge3D]) -> list[Wall3D]:





            # Wall3D([edges_dict[edge] for edge in edge_list], (np.random.choice(range(256), size=3)))
            # for edge_list in [
            #     ['bottom_left_front_to_top_left_front', 'top_left_front_to_top_right_front',
            #      'top_right_front_to_bottom_right_front', 'bottom_right_front_to_bottom_left_front'],
            #     ['top_left_front_to_top_right_front', 'top_right_front_to_top_right_back',
            #      'top_right_back_to_top_left_back', 'top_left_back_to_top_left_front'],
            #     ['bottom_right_back_to_top_right_back', 'top_right_back_to_top_left_back',
            #      'top_left_back_to_bottom_left_back', 'bottom_left_back_to_bottom_right_back'],
            #     ['bottom_left_front_to_bottom_left_back', 'bottom_left_back_to_top_left_back',
            #      'top_left_back_to_top_left_front', 'top_left_front_to_bottom_left_front'],
            #     ['bottom_right_front_to_bottom_right_back', 'bottom_right_back_to_top_right_back',
            #      'top_right_back_to_top_right_front', 'top_right_front_to_bottom_right_front'],
            #     ['bottom_left_front_to_bottom_right_front', 'bottom_right_front_to_bottom_right_back',
            #      'bottom_right_back_to_bottom_left_back', 'bottom_left_back_to_bottom_left_front'],
            # ]

