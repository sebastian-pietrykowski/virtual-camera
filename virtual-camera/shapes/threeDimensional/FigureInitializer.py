import pygame

from shapes.threeDimensional.Edge3D import Edge3D
from shapes.threeDimensional.Figure3D import Figure3D
from shapes.threeDimensional.Point3D import Point3D


class FigureInitializer:
    @staticmethod
    def initialize_figures():
        return [
            FigureInitializer.create_box(Point3D(100, -50, 100), 100, 100, 100, pygame.Color("burlywood")),
            FigureInitializer.create_box(Point3D(100, -50, 300), 100, 200, 100, pygame.Color("aquamarine1")),
            FigureInitializer.create_box(Point3D(100, -50, 800), 100, 300, 200, pygame.Color("chartreuse")),
            FigureInitializer.create_box(Point3D(-100, -100, 100), -100, 200, 100, pygame.Color("red")),
            FigureInitializer.create_box(Point3D(-100, -30, 300), -100, 200, 100, pygame.Color("yellow")),
            FigureInitializer.create_box(Point3D(-50, -50, 1000), 100, 300, 200, pygame.Color("lightslategrey")),
            FigureInitializer.create_box(Point3D(-5000, -50, 10), 100, 300, 200, pygame.Color("tomato")),
            FigureInitializer.create_box(Point3D(-500, -50, 10), 100, 300, 200, pygame.Color("green")),
            FigureInitializer.create_box(Point3D(500, -50, 10), -100, 300, 200, pygame.Color("purple")),
            FigureInitializer.create_box(Point3D(-100, -100, -100), -100, 200, 100, pygame.Color("pink")),
            FigureInitializer.create_box(Point3D(300, 50, -100), -100, 200, 100, pygame.Color("blue")),

        ]

    @staticmethod
    def create_box(start_point: Point3D, width: int, height: int, depth: int, color: pygame.Color):
        bottom_left_front = start_point
        bottom_right_front = Point3D(start_point.get_x() + width, start_point.get_y(), start_point.get_z())
        bottom_left_back = Point3D(start_point.get_x(), start_point.get_y(), start_point.get_z() + depth)
        bottom_right_back = Point3D(start_point.get_x() + width, start_point.get_y(), start_point.get_z() + depth)

        top_left_front = Point3D(start_point.get_x(), start_point.get_y() + height, start_point.get_z())
        top_right_front = Point3D(start_point.get_x() + width, start_point.get_y() + height, start_point.get_z())
        top_left_back = Point3D(start_point.get_x(), start_point.get_y() + height, start_point.get_z() + depth)
        top_right_back = Point3D(start_point.get_x() + width, start_point.get_y() + height, start_point.get_z() + depth)

        return Figure3D([
            Edge3D(bottom_left_front, bottom_right_front, color),
            Edge3D(bottom_right_front, bottom_right_back, color),
            Edge3D(bottom_right_back, bottom_left_back, color),
            Edge3D(bottom_left_back, bottom_left_front, color),

            Edge3D(top_left_front, top_right_front, color),
            Edge3D(top_right_front, top_right_back, color),
            Edge3D(top_right_back, top_left_back, color),
            Edge3D(top_left_back, top_left_front, color),

            Edge3D(bottom_left_front, top_left_front, color),
            Edge3D(bottom_right_front, top_right_front, color),
            Edge3D(bottom_left_back, top_left_back, color),
            Edge3D(bottom_right_back, top_right_back, color),
        ])
