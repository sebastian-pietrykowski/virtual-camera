import pygame

from BspTree import BspTree
from WorkMode import WorkMode
from view.Perspective import Perspective
from view.World import World


class Camera:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FRAME_RATE = 60

    __world: World
    __perspective: Perspective
    __screen: pygame.Surface
    __work_mode: WorkMode

    def __init__(self, world: World, perspective: Perspective, screen: pygame.Surface, work_mode: WorkMode):
        self.__world = world
        self.__perspective = perspective
        self.__screen = screen
        self.__work_mode = work_mode

    def zoom_in(self):
        self.__perspective.increase_zoom_factor()

    def zoom_out(self):
        self.__perspective.decrease_zoom_factor()

    def render(self):
        self.__screen.fill(pygame.Color("black"))
        if self.__work_mode == WorkMode.EDGES:
            for figure_3d in self.__world.get_figures_3d():
                figure_3d.draw_edges(self.__screen, self.__perspective)
        elif self.__work_mode == WorkMode.WALLS:
            walls = [wall for figure in self.__world.get_figures_3d() for wall in figure.get_walls()]
            print(len(walls))
            bsp_tree = BspTree(walls)
            bsp_tree.build_tree()
            print('nodes', bsp_tree.n_nodes())
            walls = bsp_tree.traverse()[::-1]
            print('\n\n\n\n final')
            print(', '.join([str(wall) for wall in walls]))
            print('\n\n\n\n')
            for wall in walls:
                wall.draw(self.__screen, self.__perspective)
            # print('\nfinal nodes', bsp_tree.n_nodes(), '\n')
            # bsp_tree.draw_tree(self.__screen, self.__perspective)
