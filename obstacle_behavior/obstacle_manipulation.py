from pathlib import Path

import pygame

from agent_behavior.corner_object import Corner
from agent_behavior.polygon_obstacle import PolygonObstacle
from mouse_behavior.cursor_changing import CursorBehavior
from agent_behavior.tools import rectangle_parameters_from_coordinates
import json

from references import get_obstacle_behavior_folder


class ObstacleManipulation:
    def __init__(self, input_cursor_behavior: CursorBehavior, input_screen: pygame.Surface):
        self.screen = input_screen
        self.cursor_behavior = input_cursor_behavior
        self.obstacle_pool = []
        self.corner_pool = []

        self.clicks = 0
        self.click_positions = []

        self.pressed_keys = None
        self.selected_obstacle = None

    @staticmethod
    def create_dummy_rectangle():
        rectangle_points = [(547, 626), (700, 627), (545, 678), (700, 676)]
        rectangle_params = rectangle_parameters_from_coordinates(*rectangle_points)
        return pygame.Rect(rectangle_params)

    def create_dummy_polygon(self):
        # polygon_points = [(259, 639), (258, 788), (576, 795), (574, 771), (496, 740), (496, 639)] full_points = [ [
        # (259, 639), (258, 788), (576, 795), (574, 771), (496, 740), (496, 639)], [(545, 626), (699, 626), (699,
        # 676), (545, 676)], [(582, 516), (581, 526), (607, 527), (606, 569), (652, 569), (654, 593), (743, 595),
        # (742, 572), (766, 570), (763, 546), (624, 545), (625, 517), (585, 517)] ]
        obstacle_list_path = Path(get_obstacle_behavior_folder(), "obstacle_point_list.json")

        with open(obstacle_list_path, "r") as file:
            full_points = json.load(file)["lists"]
        for point_list in full_points:
            self.create_obstacle_from_clicks(point_list)

    def create_dummy_corner(self):
        corner_points = (834, 490)
        new_corner = Corner(x=corner_points[0], y=corner_points[1], screen=self.screen)
        self.corner_pool.append(new_corner)

    def click_event(self):
        if self.cursor_behavior.current_cursor_task == "rectangle_creator":
            self.rectangle_creator_from_clicks()
        if self.cursor_behavior.current_cursor_task == "rectangle_finisher":
            self.rectangle_finish_creation()
        if self.cursor_behavior.current_cursor_task == "rectangle_mover":
            self.move_clicked_obstacle()
        if self.cursor_behavior.current_cursor_task == "rectangle_deleter":
            self.delete_selected_obstacle()

    def rectangle_creator_from_clicks(self):
        self.clicks += 1
        print(self.clicks)
        pos = list(pygame.mouse.get_pos())
        self.click_positions.append(pos)

    def rectangle_finish_creation(self):
        self.create_obstacle_from_clicks(self.click_positions)
        self.clicks = 0
        self.click_positions = []

    def create_obstacle_from_clicks(self, click_list: list[tuple[int, int]]) -> None:
        new_obstacle = PolygonObstacle(click_list, self.screen)
        print(click_list)
        self.obstacle_pool.append(new_obstacle)

    def move_clicked_obstacle(self):
        if not self.selected_obstacle:
            self.select_obstacle()
        else:
            self.move_selected_obstacle()

    def select_obstacle(self) -> PolygonObstacle:
        mouse_coords = pygame.mouse.get_pos()
        for obstacle in self.obstacle_pool:
            if obstacle.check_single_point_collision(*mouse_coords):
                self.selected_obstacle = obstacle
                return obstacle

    def move_selected_obstacle(self):
        mouse_coords = pygame.mouse.get_pos()
        self.selected_obstacle.center = mouse_coords
        self.selected_obstacle.draw()
        self.selected_obstacle = None
        self.cursor_behavior.set_task_to_normal()

    def delete_selected_obstacle(self):
        selected_obstacle = self.select_obstacle()
        self.obstacle_pool.remove(selected_obstacle)
        self.selected_obstacle = None
        self.cursor_behavior.set_task_to_normal()
