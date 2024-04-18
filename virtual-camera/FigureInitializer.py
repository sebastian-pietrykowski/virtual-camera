import pygame

from shapes.threeDimensional.BoxCreator import BoxCreator
from shapes.threeDimensional.Point3D import Point3D


class FigureInitializer:
    @staticmethod
    def initialize_figures():
        return [
            BoxCreator(Point3D(100, -50, 100), 100, 100, 100, pygame.Color("burlywood")).create_box(),
            BoxCreator(Point3D(100, -50, 300), 100, 200, 100, pygame.Color("aquamarine1")).create_box(),
            BoxCreator(Point3D(100, -50, 800), 100, 300, 200, pygame.Color("chartreuse")).create_box(),
            BoxCreator(Point3D(-100, -100, 100), -100, 200, 100, pygame.Color("red")).create_box(),
            BoxCreator(Point3D(-100, -30, 300), -100, 200, 100, pygame.Color("yellow")).create_box(),
            BoxCreator(Point3D(-50, -50, 1000), 100, 300, 200, pygame.Color("lightslategrey")).create_box(),
            BoxCreator(Point3D(-5000, -50, 10), 100, 300, 200, pygame.Color("tomato")).create_box(),
            BoxCreator(Point3D(-500, -50, 10), 100, 300, 200, pygame.Color("green")).create_box(),
            BoxCreator(Point3D(500, -50, 10), -100, 300, 200, pygame.Color("purple")).create_box(),
            BoxCreator(Point3D(-100, -100, -100), -100, 200, 100, pygame.Color("pink")).create_box(),
            BoxCreator(Point3D(300, 50, -100), -100, 200, 100, pygame.Color("blue")).create_box(),
        ]
