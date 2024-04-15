import numpy as np
import pygame

from shapes.threeDimensional import Point3D
from shapes.twoDimensional.Point2D import Point2D
from view.Perspective import Perspective


class PointTransformer:

    @staticmethod
    def transform_from_3d_to_2d(point: Point3D, perspective, screen: pygame.Surface):
        z = point.get_z() if point.get_z() > 0 else 0.1
        homogeneous_point = np.array([point.get_x(), point.get_y(), z, 1])

        projection_matrix = PointTransformer.__create_projection_matrix(screen)

        transformed_point = projection_matrix @ homogeneous_point

        normalized_point = transformed_point / transformed_point[3]
        normalized_point *= perspective.get_zoom_factor()

        screen_x = (normalized_point[0] + 1) * 0.5 * screen.get_width()
        screen_y = (1 - normalized_point[1]) * 0.5 * screen.get_height()

        return Point2D(screen_x, screen_y)

    @staticmethod
    def translate(point: Point3D, vector: np.array([int, int, int])):
        return PointTransformer.__create_translation_transformation_matrix(vector) @ point.get_vector()

    @staticmethod
    def rotate(point: Point3D, degree: float, axis: str):
        return PointTransformer.__create_rotation_transformation_matrix(np.deg2rad(degree), axis) @ point.get_vector()

    @staticmethod
    def __create_projection_matrix(screen: pygame.Surface):
        aspect_ratio = screen.get_width() / screen.get_height()
        far = Perspective.FAR
        near = Perspective.NEAR
        field_of_view_rad = np.deg2rad(Perspective.FIELD_OF_VIEW_IN_DEGREES)
        aspect_tan = np.tan(field_of_view_rad / 2.0) * aspect_ratio

        return np.array([
            [1.0 / aspect_tan, 0, 0, 0],
            [0, 1.0 / np.tan(field_of_view_rad / 2.0), 0, 0],
            [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
            [0, 0, -1, 0]
        ])

    @staticmethod
    def __create_translation_transformation_matrix(translation_vector: np.array([int, int, int])):
        return np.array([
            [1, 0, 0, translation_vector[0]],
            [0, 1, 0, translation_vector[1]],
            [0, 0, 1, translation_vector[2]],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def __create_rotation_transformation_matrix(degree, axis):
        match axis:
            case "x":
                return np.array([
                    [1, 0, 0, 0],
                    [0, np.cos(degree), -np.sin(degree), 0],
                    [0, np.sin(degree), np.cos(degree), 0],
                    [0, 0, 0, 1]
                ])
            case "y":
                return np.array([
                    [np.cos(degree), 0, np.sin(degree), 0],
                    [0, 1, 0, 0],
                    [-np.sin(degree), 0, np.cos(degree), 0],
                    [0, 0, 0, 1]
                ])
            case "z":
                return np.array([
                    [np.cos(degree), -np.sin(degree), 0, 0],
                    [np.sin(degree), np.cos(degree), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]
                ])
