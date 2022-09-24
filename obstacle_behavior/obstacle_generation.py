import pygame

from agent_behavior.tools import rectangle_parameters_from_coordinates


def create_single_obstacles(rectangle_points: list[tuple[int, int]]) -> pygame.Rect:
    rectangle_params = rectangle_parameters_from_coordinates(*rectangle_points)
    return pygame.Rect(rectangle_params)


def create_multiple_obstacles(rectangle_points: list[list[tuple[int, int]]]) -> list[pygame.Rect]:
    return [create_single_obstacles(points) for points in rectangle_points]


def get_obstacle_list() -> list[tuple[int, int]]:
    return [(547, 626), (700, 627), (545, 678), (700, 676),
            (547, 626), (700, 627), (545, 678), (700, 676),]
