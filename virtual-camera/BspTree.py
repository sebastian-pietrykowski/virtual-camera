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

    def get_left(self):
        return self.__front

    def get_right(self):
        return self.__back

    def get_value(self):
        return self.__value

    def build_tree(self) -> None:
        if not self.__walls:
            return
        if len(self.__walls) == 1:
            self.__value = self.__walls[0]
            return

        print('walls!!!', len(self.__walls))
        partition_wall = self.__walls[0]
        # partition_wall = self.select_wall_for_partition(self.__walls)
        # walls = list(filter(lambda w: w != partition_wall, self.__walls))
        self.__value = partition_wall
        print('root', partition_wall)
        # self.split_wall(walls[0], partition_wall)

        front_walls = []
        back_walls = []
        for wall in self.__walls[1:]:
            # if wall.is_on_same_plane(partition_wall):
            #     # self.__value = wall
            #     print('error')
            #     print('wall', wall)
            #     print('partition wall', partition_wall)
            #     front_walls.append(wall)
            if wall.is_in_front_of_partition_wall(partition_wall):
                front_walls.append(wall)
            elif wall.is_behind_partition_wall(partition_wall):
                back_walls.append(wall)
            else:
                front_wall, back_wall = self.split_wall(wall, partition_wall)
                front_walls.append(front_wall)
                back_walls.append(back_wall)

                # If the wall lies on the partition plane, split it into smaller walls
                # split_walls = wall.split(partition_wall)
                # print('split', len(split_walls))
                # if split_walls[0].is_in_front_of_partition_wall(partition_wall):
                #     front_walls.append(split_walls[0])
                #     back_walls.append(split_walls[1])
                # elif split_walls[0].is_behind_partition_wall(partition_wall):
                #     back_walls.append(split_walls[0])
                #     front_walls.append(split_walls[1])
                # else:
                #     print('\n\n\nwall to split', wall)
                #     print('partition wall', partition_wall)
                #     print('split walls', ', '.join(str(wall) for wall in split_walls))
                #     raise ValueError('Split wall is not in front of or behind the partition wall or on the same plate.')
        print()
        print('left walls len', len(front_walls))
        print('right walls len', len(back_walls))
        print('same plate walls len', self.__value)
        print('partition wall', partition_wall)
        print('left walls', ', '.join(str(wall) for wall in front_walls))
        print('right walls', ', '.join(str(wall) for wall in back_walls))
        # print('same plate walls', ', '.join(str(wall) for wall in self.__value))
        print()
        if len(front_walls) > 0:
            self.__front = BspTree(front_walls)
            self.__front.build_tree()
        if len(back_walls) > 0:
            self.__back = BspTree(back_walls)
            self.__back.build_tree()

        # self.__value = partition_wall

    def split_wall(self, wall: Wall3D, partition_wall: Wall3D) -> tuple[Wall3D, Wall3D]:
        front_points = []
        back_points = []

        for index, current_point in enumerate(wall.get_points()):
            next_index = (index + 1) % len(wall.get_points())
            next_point = wall.get_points()[next_index]

            current_dot_product = np.dot(current_point.get_vector()[:3] - partition_wall.get_points()[0].get_vector()[:3], partition_wall.calculate_normal_vector())
            next_dot_product = np.dot(next_point.get_vector()[:3] - partition_wall.get_points()[0].get_vector()[:3], partition_wall.calculate_normal_vector())

            if current_dot_product >= 0:
                front_points.append(current_point)
                print('dodaję do front points', current_point)
            else:
                back_points.append(current_point)
                print('dodaję do back points', current_point)

            if current_dot_product * next_dot_product < 0:
                print('current point', current_point)
                print('current dot product', current_dot_product)
                print('next point', next_point)
                print('next dot product', next_dot_product)
                t = current_dot_product / (current_dot_product - next_dot_product)
                print('t', t)
                intersection_point = (current_point.get_vector()[:3] + t * (
                            next_point.get_vector()[:3] - current_point.get_vector()[:3]))
                print('różne dla', current_point, 'i', next_point, "; dodaję intersection point", intersection_point)
                front_points.append(Point3D(*intersection_point))
                back_points.append(Point3D(*intersection_point))
            # if current_dot_product > 0:
            #     front_points.append(current_point)
            #     print('dodaję do front points', current_point)
            # elif current_dot_product < 0:
            #     back_points.append(current_point)
            #     print('dodaję do back points', current_point)
            #
            # if current_dot_product * next_dot_product < 0:
            #     t = current_dot_product / (current_dot_product - next_dot_product)
            #     intersection_point = (current_point.get_vector()[:3] + t * (
            #                 next_point.get_vector()[:3] - current_point.get_vector()[:3])).astype(int)
            #     front_points.append(Point3D(*intersection_point))
            #     back_points.append(Point3D(*intersection_point))
            #     print('różne dla', current_point, 'i', next_point, "; dodaję intersection point",
            #           Point3D(*intersection_point))
            # elif current_dot_product == 0:
            #     print('ta sama płaszczyzna', current_point)
            #     if next_dot_product > 0:
            #         front_points.append(current_point)
            #     else:
            #         back_points.append(current_point)

        if not (front_points and back_points):
            print('partition wall', partition_wall)
            print('wall', wall)
            print('front points len', len(front_points))
            print('back points len', len(back_points))
            print('all points len', len(wall.get_points()))
            print('front points', ''.join(str(p) for p in front_points))
            print('back points', ''.join(str(p) for p in back_points))
            raise ValueError('Wall was not split correctly.')

        # if len(front_points) == 0:
        #     raise ValueError('No front points found.')
        # if len(back_points) == 0:
        #     raise ValueError('No back points found.')

        print('front points len', len(front_points))
        print('back points len', len(back_points))
        print('all points len', len(wall.get_points()))
        print('front points', ''.join(str(p) for p in front_points))
        print('back points', ''.join(str(p) for p in back_points))
        print('all points', ''.join(str(p) for p in wall.get_points()))
        print('partition wall', partition_wall)
        print('\n\n\n')

        front_wall = Wall3D([Edge3D(front_points[i], front_points[(i + 1) % len(front_points)], None) for i in
                             range(len(front_points))], wall.get_color())
        if not (len(front_wall.get_points()) == 4 or len(front_wall.get_points()) == 0):
            raise ValueError('Front wall has 3 points.')
        back_wall = Wall3D([Edge3D(back_points[i], back_points[(i + 1) % len(back_points)], None) for i in
                            range(len(back_points))], wall.get_color())
        if not (len(back_wall.get_points()) == 4 or len(back_wall.get_points()) == 0):
            raise ValueError('Back wall has 3 points.')

        return front_wall, back_wall

    # def draw_tree(self, screen: pygame.Surface, perspective: Perspective) -> None:
    #     if self.__right is not None:
    #         self.__right.draw_tree(screen, perspective)
    #
    #     self.__value.draw(screen, perspective)
    #
    #     if self.__left is not None:
    #         self.__left.draw_tree(screen, perspective)

    def n_nodes(self) -> int:
        print('tree node value', self.__value)
        if self.__front is None and self.__back is None:
            return 1
        if self.__front is None:
            return 1 + self.__back.n_nodes()
        if self.__back is None:
            return 1 + self.__front.n_nodes()
        return 1 + self.__front.n_nodes() + self.__back.n_nodes()

    # jeżeli ściana nie leży na płaszczyźnie z, to podzielić wzdłuż jej środka w z
    # def select_wall_for_partition(self, walls: List[Wall3D]) -> Wall3D:
    #     best_result = math.inf
    #     best_wall = None
    #
    #     average_distance = np.mean([
    #         Point3D.get_center_point(wall.get_points()).distance_to(Point3D(0, 0, 0))
    #         for wall in walls
    #     ])
    #     for wall in walls:
    #         distance = Point3D.get_center_point(wall.get_points()).distance_to(Point3D(0, 0, 0))
    #         if abs(distance - average_distance) < abs(best_result):
    #             best_result = distance - average_distance
    #             best_wall = wall
    #     if best_wall is None:
    #         raise ValueError('No wall found for partition.')
    #     print('best_result', best_wall)
    #     return best_wall

        # for partition_wall_candidate in walls:
        #     other_walls = list(filter(lambda w: w != partition_wall_candidate, walls))
        #     print('len', len(other_walls))
        #     result = 0
        #     for other_wall in other_walls:
        #         if other_wall.is_in_front_of_partition_wall(partition_wall_candidate):
        #             result += 1
        #         elif other_wall.is_behind_partition_wall(partition_wall_candidate):
        #             result -= 1
        #     print('result', result, 'wall', partition_wall_candidate)
        #     if abs(result) < abs(best_result):
        #         best_result = abs(result)
        #         best_wall = [partition_wall_candidate]
        #     elif abs(result) == abs(best_result):
        #         best_walls.append(partition_wall_candidate)
        # print('best_result', best_result, 'best_walls', best_walls)

        # average_distance = np.mean([
        #     Point3D.get_center_point(wall.get_points()).distance_to(Point3D(0, 0, 0))
        #     for wall in best_walls
        # ])
        # wall_closest_to_center = min(
        #     best_walls,
        #     key=lambda wall: abs(Point3D.get_center_point(wall.get_points()).distance_to(Point3D(0, 0, 0)) - average_distance)
        # )

        # print('best_result', best_result, 'best_wall', wall_closest_to_center)
        # return wall_closest_to_center

    def traverse(self) -> list[Wall3D]:
        visible_walls = []
        invisible_walls = []
        camera_position = Point3D(0, 0, 0)

        distance_to_partition_wall = (camera_position.get_vector()[:3] - Point3D.get_center_point(
            self.__value.get_points()).get_vector()[:3]) @ self.__value.calculate_normal_vector()
        print('camera', camera_position)
        print('partition wall', ', '.join(str(p) for p in self.__value.get_points()))
        print('partition wall center', Point3D.get_center_point(self.__value.get_points()))
        print('normal', self.__value.calculate_normal_vector())
        print('distance', distance_to_partition_wall)

        if distance_to_partition_wall > 0:
            if self.__front is not None:
                print('przod > 0')
                visible_walls.extend(self.__front.traverse())
            print('> 0')
            visible_walls.append(self.__value)
            if self.__back is not None:
                print('tył > 0')
                visible_walls.extend(self.__back.traverse())
        else:
            if self.__back is not None:
                print('tył < 0')
                invisible_walls.extend(self.__back.traverse())
            print('< 0')
            invisible_walls.append(self.__value)
            if self.__front is not None:
                print('przod < 0')
                invisible_walls.extend(self.__front.traverse())

        return invisible_walls + visible_walls
