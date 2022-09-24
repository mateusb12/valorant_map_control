import pygame

from mouse_behavior.cursor_changing import CursorBehavior
from agent_behavior.tools import rectangle_parameters_from_coordinates


class ObstacleManipulation:
    def __init__(self, input_cursor_behavior: CursorBehavior):
        self.cursor_behavior = input_cursor_behavior
        self.obstacle_pool = []
        rectangle_points = [(547, 626), (700, 627), (545, 678), (700, 676)]
        rectangle_params = rectangle_parameters_from_coordinates(*rectangle_points)
        new_obstacle = pygame.Rect(rectangle_params)
        self.obstacle_pool.append(new_obstacle)

        self.clicks = 0
        self.click_positions = []

        self.selected_obstacle = None

    def click_event(self):
        if self.cursor_behavior.current_cursor_task == "rectangle_creator":
            self.rectangle_creator_from_clicks()
        if self.cursor_behavior.current_cursor_task == "rectangle_mover":
            self.move_clicked_obstacle()
        if self.cursor_behavior.current_cursor_task == "rectangle_deleter":
            self.delete_selected_obstacle()

    def rectangle_creator_from_clicks(self):
        self.clicks += 1
        self.click_positions.append(pygame.mouse.get_pos())
        if self.clicks == 4:
            print(self.click_positions)
            self.create_obstacle_from_clicks(self.click_positions)
            self.clicks = 0
            self.click_positions = []

    def create_obstacle_from_clicks(self, click_list: list[tuple[int, int]]) -> None:
        rectangle_params = rectangle_parameters_from_coordinates(*click_list)
        new_obstacle = pygame.Rect(rectangle_params)
        self.obstacle_pool.append(new_obstacle)

    def move_clicked_obstacle(self):
        if not self.selected_obstacle:
            self.select_obstacle()
        else:
            self.move_selected_obstacle()

    def select_obstacle(self) -> pygame.Rect:
        mouse_coords = pygame.mouse.get_pos()
        for obstacle in self.obstacle_pool:
            if obstacle.collidepoint(mouse_coords):
                self.selected_obstacle = obstacle
                return obstacle

    def move_selected_obstacle(self):
        mouse_coords = pygame.mouse.get_pos()
        self.selected_obstacle.center = mouse_coords
        self.selected_obstacle = None
        self.cursor_behavior.set_task_to_normal()

    def delete_selected_obstacle(self):
        selected_obstacle = self.select_obstacle()
        self.obstacle_pool.remove(selected_obstacle)
        self.selected_obstacle = None
        self.cursor_behavior.set_task_to_normal()