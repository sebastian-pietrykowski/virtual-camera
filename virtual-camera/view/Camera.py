import pygame

from view.Perspective import Perspective
from view.World import World


class Camera:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FRAME_RATE = 60

    __world: World
    __perspective: Perspective
    __screen: pygame.Surface

    def __init__(self, world: World, perspective: Perspective, screen: pygame.Surface):
        self.__world = world
        self.__perspective = perspective
        self.__screen = screen

    def zoom_in(self):
        self.__perspective.increase_zoom_factor()

    def zoom_out(self):
        self.__perspective.decrease_zoom_factor()

    def render(self):
        self.__screen.fill(pygame.Color("black"))
        for figure_3d in self.__world.get_figures_3d():
            figure_3d.draw(self.__screen, self.__perspective)
