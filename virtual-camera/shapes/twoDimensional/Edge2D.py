import pygame as pygame

from shapes.twoDimensional.Point2D import Point2D


class Edge2D:
    __point1: Point2D
    __point2: Point2D
    __color: pygame.Color

    def __init__(self, point1: Point2D, point2: Point2D, color: pygame.Color):
        self.__point1 = point1
        self.__point2 = point2
        self.__color = color

    def get_point1(self):
        return self.__point1

    def get_point2(self):
        return self.__point2

    def get_color(self):
        return self.__color

    def draw(self, screen):
        pygame.draw.line(
            screen, self.__color,
            (self.__point1.get_x(), self.__point1.get_y()),
            (self.__point2.get_x(), self.__point2.get_y())
        )
        pygame.display.update()
