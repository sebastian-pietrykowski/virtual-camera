import math
from typing import List, Optional

import numpy as np

from shapes.threeDimensional.Edge3D import Edge3D
from shapes.threeDimensional.Point3D import Point3D
from shapes.threeDimensional.Wall3D import Wall3D


class BspTree:
    __front: Optional['BspTree']
    __back: Optional['BspTree']
    __value: Wall3D
    __walls: List[Wall3D]

    def __init__(self, walls: List[Wall3D]):
        self.__front = None
        self.__back = None
        self.__walls = walls

    def get_front(self):
        return self.__front

    def get_back(self):
        return self.__back

    def get_value(self):
        return self.__value

    def build_tree(self) -> None:
        if not self.__walls:
            return
        if len(self.__walls) == 1:
            self.__value = self.__walls[0]
            return

        partition_wall = BspTree.__select_wall_for_partition(self.__walls)
        self.__value = partition_wall

        front_walls = []
        back_walls = []
        other_walls = filter(lambda w: w != partition_wall, self.__walls)
        for wall in other_walls:
            if wall.is_in_front_of_partition_wall(partition_wall):
                front_walls.append(wall)
            elif wall.is_behind_partition_wall(partition_wall):
                back_walls.append(wall)
            else:
                front_wall, back_wall = self.split_wall(wall, partition_wall)
                front_walls.append(front_wall)
                back_walls.append(back_wall)

        if len(front_walls) > 0:
            self.__front = BspTree(front_walls)
            self.__front.build_tree()
        if len(back_walls) > 0:
            self.__back = BspTree(back_walls)
            self.__back.build_tree()

    def split_wall(self, wall: Wall3D, partition_wall: Wall3D) -> tuple[Wall3D, Wall3D]:
        front_points = []
        back_points = []

        for index, current_point in enumerate(wall.get_points()):
            next_index = (index + 1) % len(wall.get_points())
            next_point = wall.get_points()[next_index]

            current_dot_product = np.dot(
                current_point.get_vector()[:3] - partition_wall.get_points()[0].get_vector()[:3],
                partition_wall.calculate_normal_vector()
            ).astype(np.float64)

            next_dot_product = np.dot(
                next_point.get_vector()[:3] - partition_wall.get_points()[0].get_vector()[:3],
                partition_wall.calculate_normal_vector()
            ).astype(np.float64)

            if current_dot_product >= 0:
                front_points.append(current_point)
            else:
                back_points.append(current_point)

            if current_dot_product * next_dot_product < 0:
                t = current_dot_product / (current_dot_product - next_dot_product)
                intersection_point = np.round(current_point.get_vector()[:3] + t * (
                            next_point.get_vector()[:3] - current_point.get_vector()[:3])).astype(int)
                front_points.append(Point3D(*intersection_point))
                back_points.append(Point3D(*intersection_point))

        if not (front_points and back_points):
            raise ValueError('Wall was not split correctly.')

        front_wall = Wall3D([Edge3D(front_points[i], front_points[(i + 1) % len(front_points)], None) for i in
                             range(len(front_points))], wall.get_color())
        back_wall = Wall3D([Edge3D(back_points[i], back_points[(i + 1) % len(back_points)], None) for i in
                            range(len(back_points))], wall.get_color())

        return front_wall, back_wall

    def n_nodes(self) -> int:
        if self.__front is None and self.__back is None:
            return 1
        if self.__front is None:
            return 1 + self.__back.n_nodes()
        if self.__back is None:
            return 1 + self.__front.n_nodes()
        return 1 + self.__front.n_nodes() + self.__back.n_nodes()

    def traverse(self) -> list[Wall3D]:
        visible_walls = []
        invisible_walls = []
        camera_position = Point3D(0, 0, 0)

        distance_to_partition_wall = (camera_position.get_vector()[:3] - Point3D.get_center_point(
            self.__value.get_points()).get_vector()[:3]) @ self.__value.calculate_normal_vector()

        if distance_to_partition_wall > 0:
            if self.__front is not None:
                visible_walls.extend(self.__front.traverse())
            visible_walls.append(self.__value)
            if self.__back is not None:
                visible_walls.extend(self.__back.traverse())
        else:
            if self.__back is not None:
                invisible_walls.extend(self.__back.traverse())
            invisible_walls.append(self.__value)
            if self.__front is not None:
                invisible_walls.extend(self.__front.traverse())

        return invisible_walls + visible_walls

    @staticmethod
    def __select_wall_for_partition(walls: List[Wall3D]) -> Wall3D:
        best_result = math.inf
        best_wall = None

        average_distance = np.mean([
            Point3D.get_center_point(wall.get_points()).distance_to(Point3D(0, 0, 0))
            for wall in walls
        ])
        for wall in walls:
            distance = Point3D.get_center_point(wall.get_points()).distance_to(Point3D(0, 0, 0))
            if abs(distance - average_distance) < abs(best_result):
                best_result = distance - average_distance
                best_wall = wall
        if best_wall is None:
            raise ValueError('No wall found for partition.')
        return best_wall