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
        walls = self.__create_walls(points, edges_dict)

        return Figure3D(list(edges_dict.values()), walls)

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
                ('bottom_right_front', 'top_right_front'),
                ('bottom_left_back', 'top_left_back'),
                ('bottom_right_back', 'top_right_back'),
            ]
        }

    def __create_walls(self, points: dict[str, Point3D], edges_dict: dict[str, Edge3D]) -> list[Wall3D]:
        return [
            Wall3D([edges_dict[edge] for edge in edge_list], self.__color)
            for edge_list in [
                ['bottom_left_front_to_bottom_right_front', 'bottom_right_front_to_bottom_right_back',
                 'bottom_right_back_to_bottom_left_back', 'bottom_left_back_to_bottom_left_front'],
                ['top_left_front_to_top_right_front', 'top_right_front_to_top_right_back',
                 'top_right_back_to_top_left_back', 'top_left_back_to_top_left_front'],
                ['bottom_left_front_to_top_left_front', 'top_left_front_to_top_right_front',
                 'bottom_right_front_to_top_right_front', 'bottom_right_front_to_bottom_right_back'],
                ['bottom_right_back_to_top_right_back', 'top_right_back_to_top_left_back',
                 'bottom_left_back_to_top_left_back', 'bottom_left_back_to_bottom_left_front'],
            ]
        ]
