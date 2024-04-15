import numpy as np

from shapes.threeDimensional.Figure3D import Figure3D


class World:
    MOVE_STEP = 10
    ROTATION_DEGREES = 45.

    __figures_3d: list[Figure3D]

    def __init__(self, figures_3d: list[Figure3D]):
        self.__figures_3d = figures_3d

    def get_figures_3d(self):
        return self.__figures_3d

    def move_front(self):
        for figure_3d in self.__figures_3d:
            figure_3d.translate(np.array([0, 0, -self.MOVE_STEP]))

    def move_back(self):
        for figure_3d in self.__figures_3d:
            figure_3d.translate(np.array([0, 0, self.MOVE_STEP]))

    def move_left(self):
        for figure_3d in self.__figures_3d:
            figure_3d.translate(np.array([-self.MOVE_STEP, 0, 0]))

    def move_right(self):
        for figure_3d in self.__figures_3d:
            figure_3d.translate(np.array([self.MOVE_STEP, 0, 0]))

    def move_up(self):
        for figure_3d in self.__figures_3d:
            figure_3d.translate(np.array([0, self.MOVE_STEP, 0]))

    def move_down(self):
        for figure_3d in self.__figures_3d:
            figure_3d.translate(np.array([0, -self.MOVE_STEP, 0]))

    def rotate_up(self):
        for figure_3d in self.__figures_3d:
            figure_3d.rotate(-self.ROTATION_DEGREES, 'x')

    def rotate_down(self):
        for figure_3d in self.__figures_3d:
            figure_3d.rotate(self.ROTATION_DEGREES, 'x')

    def rotate_left(self):
        for figure_3d in self.__figures_3d:
            figure_3d.rotate(-self.ROTATION_DEGREES, 'y')

    def rotate_right(self):
        for figure_3d in self.__figures_3d:
            figure_3d.rotate(self.ROTATION_DEGREES, 'y')
