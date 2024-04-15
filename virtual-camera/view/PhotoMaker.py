import time

import pygame

from view.Camera import Camera


class PhotoMaker:
    CENTER_CROSS_SIZE = 15
    CROSS_LINE_WIDTH = 3
    FRAME_LINE_WIDTH = 50
    FREEZE_TIME_IN_SECONDS = 0.5
    COLOR = pygame.Color("white")

    __screen: pygame.Surface
    __camera: Camera

    def __init__(self, screen: pygame.Surface, camera: Camera):
        self.__screen = screen
        self.__camera = camera

    def make_photo(self):
        self.__draw_center_cross()
        self.__draw__frame()
        time.sleep(PhotoMaker.FREEZE_TIME_IN_SECONDS)
        self.__camera.render()

    def __draw_center_cross(self):
        pygame.draw.line(
            self.__screen, PhotoMaker.COLOR,
            (self.__screen.get_width() / 2, self.__screen.get_height() / 2 - PhotoMaker.CENTER_CROSS_SIZE),
            (self.__screen.get_width() / 2, self.__screen.get_height() / 2 + PhotoMaker.CENTER_CROSS_SIZE),
            PhotoMaker.CROSS_LINE_WIDTH
        )
        pygame.draw.line(
            self.__screen, PhotoMaker.COLOR,
            (self.__screen.get_width() / 2 - PhotoMaker.CENTER_CROSS_SIZE, self.__screen.get_height() / 2),
            (self.__screen.get_width() / 2 + PhotoMaker.CENTER_CROSS_SIZE, self.__screen.get_height() / 2),
            PhotoMaker.CROSS_LINE_WIDTH
        )
        pygame.display.update()

    def __draw__frame(self):
        pygame.draw.line(
            self.__screen, PhotoMaker.COLOR,
            (0, 0),
            (0, self.__screen.get_height()),
            PhotoMaker.FRAME_LINE_WIDTH
        )
        pygame.draw.line(
            self.__screen, PhotoMaker.COLOR,
            (0, 0),
            (self.__screen.get_width(), 0),
            PhotoMaker.FRAME_LINE_WIDTH
        )
        pygame.draw.line(
            self.__screen, PhotoMaker.COLOR,
            (self.__screen.get_width(), 0),
            (self.__screen.get_width(), self.__screen.get_height()),
            PhotoMaker.FRAME_LINE_WIDTH
        )
        pygame.draw.line(
            self.__screen, PhotoMaker.COLOR,
            (0, self.__screen.get_height()),
            (self.__screen.get_width(), self.__screen.get_height()),
            PhotoMaker.FRAME_LINE_WIDTH
        )
        pygame.display.update()
