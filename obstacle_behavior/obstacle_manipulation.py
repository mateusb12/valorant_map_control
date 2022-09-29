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
        obstacle_list_path = Path(get_obstacle_behavior_folder(), "obstacle_point_list.json")

        with open(obstacle_list_path, "r") as file:
            full_points = json.load(file)["lists"]
        for point_list in full_points:
            self.create_obstacle_from_clicks(point_list)

    def create_dummy_corner(self):
        corner_list_path = Path(get_obstacle_behavior_folder(), "corner_point_list.json")
        with open(corner_list_path, "r") as file:
            full_points = json.load(file)
        for coord_list in full_points.values():
            for coords in coord_list:
                new_x, new_y = coords
                new_corner = Corner(x=new_x, y=new_y, screen=self.screen)
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
        pos = list(pygame.mouse.get_pos())
        self.click_positions.append(pos)

    def rectangle_finish_creation(self):
        self.create_obstacle_from_clicks(self.click_positions)
        print(self.click_positions)
        self.clicks = 0
        self.click_positions = []

    def create_obstacle_from_clicks(self, click_list: list[tuple[int, int]]) -> None:
        new_obstacle = PolygonObstacle(click_list, self.screen)
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
        print(selected_obstacle.points)
        self.obstacle_pool.remove(selected_obstacle)
        self.selected_obstacle = None
        self.cursor_behavior.set_task_to_normal()
