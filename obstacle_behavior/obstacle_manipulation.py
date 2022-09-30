from pathlib import Path

import pygame

from agent_behavior.polygon_obstacle import PolygonObstacle
from mouse_behavior.cursor_changing import CursorBehavior
from agent_behavior.tools import rectangle_parameters_from_coordinates
import json

from obstacle_behavior.corner_object import Corner
from obstacle_behavior.painting_object import Panel
from references import get_obstacle_behavior_folder


class ObstacleManipulation:
    def __init__(self, input_cursor_behavior: CursorBehavior, input_screen: pygame.Surface):
        self.screen = input_screen
        self.cursor_behavior = input_cursor_behavior
        self.obstacle_pool = []
        self.corner_pool = []
        self.painting_pool = []

        self.clicks = 0
        self.click_positions = []

        self.pressed_keys = None
        self.selected_obstacle = None

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
        for area, coord_list in full_points.items():
            for coords in coord_list:
                new_x, new_y = coords
                new_corner = Corner(x=new_x, y=new_y, screen=self.screen, area=area)
                if area.startswith("t_"):
                    new_corner.last_seen_by = "attack"
                    new_corner.radius -= 1
                elif area.startswith("ct_"):
                    new_corner.last_seen_by = "defense"
                    new_corner.radius -= 1
                self.corner_pool.append(new_corner)

    def create_dummy_painting(self):
        corner_list_path = Path(get_obstacle_behavior_folder(), "panel_point_list.json")
        with open(corner_list_path, "r") as file:
            full_points = json.load(file)
        panel_list = ["mid_window", "mid_doors", "a_short", "a_lobby", "a_long", "c_long", "garage"]
        region_table = {}
        for panel_tag in panel_list:
            points = full_points[panel_tag]
            panel = Panel(points, self.screen, area=panel_tag)
            region_table[panel_tag] = panel
            self.painting_pool.append(panel)
        for corner in self.corner_pool:
            region = corner.area
            if region in panel_list:
                dad = region_table[corner.area]
                dad.native_corners.append(corner)
        return region_table

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
        selected_obstacle_points = selected_obstacle.points
        print(selected_obstacle.points)
        self.obstacle_pool.remove(selected_obstacle)
        self.selected_obstacle = None
        self.cursor_behavior.set_task_to_normal()
