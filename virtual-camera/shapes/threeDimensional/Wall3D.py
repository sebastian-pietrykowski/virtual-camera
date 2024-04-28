import math
from typing import List

import numpy as np
import pygame

from shapes.threeDimensional.Edge3D import Edge3D
from shapes.threeDimensional.Point3D import Point3D
from shapes.threeDimensional.Triangle3D import Triangle3D
from view.Perspective import Perspective


class Wall3D:
    __points: List[Point3D]
    __edges: List[Edge3D]
    __color: pygame.Color

    __TRIANGLE_MAX_DISTANCE = 10

    def __str__(self):
        return f"Wall3D({', '.join(str(edge) for edge in self.__edges)})" \
               f", edges count: {len(self.__edges)}" \
               f", points count: {len(self.__points)})"

    def __init__(self, edges: List[Edge3D], color: pygame.Color):
        if len(edges) < 3:
            print('edges', ''.join(str(edge) for edge in edges))
            raise ValueError("Wall must have at least 3 edges")

        self.__edges = edges
        self.__color = color
        self.__points = list({edge.get_point1() for edge in edges} | {edge.get_point2() for edge in edges})
        print('sorted points', ','.join(str(point) for point in self.__points))

        x_values = [point.get_x() for point in self.__points]
        y_values = [point.get_y() for point in self.__points]
        z_values = [point.get_z() for point in self.__points]

        if not (len(set(x_values)) == 1 or len(set(y_values)) == 1 or len(set(z_values)) == 1):
            raise ValueError("Wall points must not be in one line", ''.join(str(point) for point in self.__points))

    def get_points(self):
        return self.__points

    def get_edges(self):
        return self.__edges

    def get_color(self):
        return self.__color

    def is_visible(self) -> bool:
        print('points', self.__points)
        print('is_visible', any(point.is_visible() for point in self.__points))
        return any(point.is_visible() for point in self.__points)

    def draw(self, screen: pygame.Surface, perspective: Perspective):
        print('\ndrawing\n')
        edges_2d = [edge.transform_to_2d(screen, perspective) for edge in self.__edges]
        print('edges_2d', len(edges_2d))
        points_2d_tuples = list((point.get_x(), point.get_y()) for edge in edges_2d for point in edge.get_points())
        center = (screen.get_width()/2 + screen.get_width()/2)
        # sorted_points = sorted(points_2d_tuples, key=lambda x: math.atan2(x[1] - center, x[0] - center))

        # sorted_points = self.graham_scan(points_2d_tuples)

        print('points_2d_tuples', points_2d_tuples)
        if len(points_2d_tuples) >= 3:
            pygame.draw.polygon(screen, self.__color, points_2d_tuples)
            pygame.draw.aalines(screen, (255, 255, 255), True, points_2d_tuples)
            pygame.display.update()

    # def get_bottom_most_point(self, points):
    #     bottom_most = points[0]
    #     for point in points:
    #         if point[1] < bottom_most[1] or (point[1] == bottom_most[1] and point[0] < bottom_most[0]):
    #             bottom_most = point
    #     return bottom_most
    #
    # def calculate_angle(self, point1, point2):
    #     return math.atan2(point2[1] - point1[1], point2[0] - point1[0])

    # def calculate_distance(self, point1, point2):
    #     return (point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2

    # def orientation(self, point1, point2, point3):
    #     return (point2[1] - point1[1]) * (point3[0] - point2[0]) - (point2[0] - point1[0]) * (point3[1] - point2[1])

    # def graham_scan(self, points):
    #     bottom_most = self.get_bottom_most_point(points)
    #     points.sort(key=lambda point: (self.calculate_angle(bottom_most, point), self.calculate_distance(bottom_most, point)))
    #
    #     hull = points[:2]
    #
    #     for point in points[2:]:
    #         while len(hull) > 1 and self.orientation(hull[-2], hull[-1], point) >= 0:
    #             hull.pop()
    #         hull.append(point)
    #
    #     return hull

    # def get_distance_to_observer(self) -> float:
    #     center_of_gravity = Point3D.get_center_point(self.__points)
    #     observer_point = Point3D(0, 0, 0)
    #     return center_of_gravity.distance_to(observer_point)

    def calculate_normal_vector(self) -> np.array([int, int, int]):
        point1 = self.__points[0].get_vector()[:3]
        point2 = self.__points[1].get_vector()[:3]
        point3 = self.__points[2].get_vector()[:3]

        vector1 = point2 - point1
        vector2 = point3 - point1

        return np.cross(vector1, vector2)
    # def calculate_normal_vector(self) -> np.array([int, int, int]):
    #     center_point = Point3D.get_center_point(self.__points)
    #     normal_vectors = []
    #
    #     # Sort points by x, y and z coordinates
    #     sorted_points = sorted(self.__points, key=lambda point: (point.get_x(), point.get_y(), point.get_z()))
    #
    #     for i in range(len(sorted_points)):
    #         point1 = sorted_points[i].get_vector()[:3]
    #         point2 = sorted_points[(i + 1) % len(sorted_points)].get_vector()[:3]
    #         center_vector = center_point.get_vector()[:3]
    #
    #         vector1 = center_vector - point1
    #         vector2 = center_vector - point2
    #
    #         normal_vectors.append(np.cross(vector1, vector2))
    #
    #     return np.mean(normal_vectors, axis=0)

    # def calculate_intersection_point(self, edge: Edge3D) -> Point3D:
    #     # P = P0 + tD
    #     # t = (N @ P1 - N @ P0) / (N @ D)
    #     direction_vector = edge.get_point2().get_vector()[:3] - edge.get_point1().get_vector()[:3]
    #     normal_vector = self.calculate_normal_vector()
    #
    #     point_on_plane = self.__points[0].get_vector()[:3]
    #     edge_start_point = edge.get_point1().get_vector()[:3]
    #     if normal_vector @ direction_vector == 0:
    #         return None
    #     t = (normal_vector @ (point_on_plane - edge_start_point)) / (normal_vector @ direction_vector)
    #
    #     intersection_point = edge_start_point + t * direction_vector
    #     return Point3D(*intersection_point)

    def is_in_front_of_partition_wall(self, partition_wall: 'Wall3D') -> bool:
        normal_vector = partition_wall.calculate_normal_vector()
        for point in self.__points:
            if (point.get_vector()[:3] - partition_wall.get_points()[0].get_vector()[:3]) @ normal_vector < 0:
                return False
        return True

        # normal_vector = partition_wall.calculate_normal_vector()
        # for point in self.__points:
        #     if self.is_point_on_wall(point):
        #         print('is_point_on_wall', point, partition_wall)
        #         continue
        #     direction_vector = point.get_vector()[:3] - partition_wall.__points[0].get_vector()[:3]
        #     dot_product = normal_vector @ direction_vector
        #     if dot_product < 0:
        #         if point.get_x() == 100 and point.get_y() == 177 and point.get_z() == 247:
        #             print('is_behind_partition_wall')
        #             print('point', point)
        #             print('partition_wall', partition_wall)
        #             print('is_point_on_wall', self.is_point_on_wall(point))
        #             print('dot_product', dot_product)
        #             print('direction_vector', direction_vector)
        #             print('False')
        #         return False
        # return True

    def is_behind_partition_wall(self, partition_wall: 'Wall3D') -> bool:
        normal_vector = partition_wall.calculate_normal_vector()
        for point in self.__points:
            if (point.get_vector()[:3] - partition_wall.get_points()[0].get_vector()[:3]) @ normal_vector > 0:
                return False
        return True
        # normal_vector = partition_wall.calculate_normal_vector()
        # for point in self.__points:
        #     if self.is_point_on_wall(point):
        #         print('is_point_on_wall', point, partition_wall)
        #         continue
        #     direction_vector = point.get_vector()[:3] - Point3D.get_center_point(partition_wall.get_points()).get_vector()[:3]
        #     dot_product = normal_vector @ direction_vector
        #     if dot_product > 0:
        #         return False
        # return True

    # def is_point_on_wall(self, point: 'Point3D') -> bool:
    #     normal_vector = self.calculate_normal_vector()
    #     direction_vector = point.get_vector()[:3] - self.__points[0].get_vector()[:3]
    #     if np.dot(normal_vector, direction_vector) != 0:
    #         return False
    #
    #     min_x = min(point.get_x() for point in self.__points)
    #     max_x = max(point.get_x() for point in self.__points)
    #     min_y = min(point.get_y() for point in self.__points)
    #     max_y = max(point.get_y() for point in self.__points)
    #     min_z = min(point.get_z() for point in self.__points)
    #     max_z = max(point.get_z() for point in self.__points)
    #
    #     return min_x <= point.get_x() <= max_x and min_y <= point.get_y() <= max_y and min_z <= point.get_z() <= max_z

    # def __calculate_intersection_points(self, partition_wall: 'Wall3D') -> List[Point3D]:
    #     return [partition_wall.calculate_intersection_point(edge)
    #             for edge in self.__edges if partition_wall.calculate_intersection_point(edge) is not None]

    # def is_on_same_plane(self, other_wall):
    #     # Sprawdź, czy wektory normalne są równoległe
    #     normal1 = self.calculate_normal_vector()
    #     normal2 = other_wall.calculate_normal_vector()
    #     if not np.allclose(np.cross(normal1, normal2), 0):
    #         return False
    #
    #     # Sprawdź, czy punkt z jednej ściany leży na płaszczyźnie drugiej ściany
    #     point = self.__edges[0].get_point1().get_vector()[:3]
    #     d = -np.dot(normal2, other_wall.__edges[0].get_point1().get_vector()[:3])
    #     return np.allclose(np.dot(normal2, point) + d, 0)

    # def __create_edges_from_points(self, points: List[Point3D]) -> List[Edge3D]:
    #     return [Edge3D(points[i], points[(i + 1) % len(points)], self.__color) for i in range(len(points))]

    # def turn_into_triangles(self):
    #     triangles = []
    #     self.turn_into_triangles_recursively(Wall3D.__TRIANGLE_MAX_DISTANCE, self, triangles)
    #     return triangles

    # def turn_into_triangles_recursively(self, max_distance: int, wall_to_split: 'Wall3D', results: List['Triangle3D']):
    #     distance = max([
    #         edge.get_point1().distance_to(edge.get_point2())
    #         for edge in self.__edges
    #     ])
    #
    #     if distance > max_distance:
    #         for wall in self.__split_into_four_walls():
    #             self.turn_into_triangles_recursively(max_distance, wall, results)
    #     else:
    #         results.append(Triangle3D(wall_to_split.get_edges()[:3], wall_to_split.__color))
    #         results.append(Triangle3D(wall_to_split.get_edges()[1:4], wall_to_split.__color))

    # def __split_into_four_walls(self) -> List['Wall3D']:
    #     n = len(self.__points)
    #     if n != 4:
    #         raise ValueError("Wall must have 4 points")
    #     center_point = Point3D.get_center_point(self.__points)
    #
    #     mid_points = [Point3D.get_center_point([self.__points[i], self.__points[(i + 1) % n]]) for i in range(n)]
    #
    #     walls = []
    #     for i in range(n):
    #         edges = [
    #             Edge3D(self.__points[i], mid_points[i], self.__color),
    #             Edge3D(mid_points[i], center_point, self.__color),
    #             Edge3D(center_point, mid_points[(i - 1) % n], self.__color),
    #             Edge3D(mid_points[(i - 1) % n], self.__points[i], self.__color)
    #         ]
    #         walls.append(Wall3D(edges, self.__color))
    #
    #     return walls