import math

import pygame


class PolygonObstacle:
    def __init__(self, points: list[tuple[float, float]], screen: pygame.Surface):
        self.points = points
        self.color = pygame.Color('darkblue')
        self.screen = screen
        self.agent_box_collider = None
        self.polygon = None
        self.draw()

    def draw(self):
        self.polygon = pygame.draw.polygon(self.screen, self.color, self.points)

    def check_point_collision(self, x: int, y: int):
        """ Check if a point is inside a polygon """
        n = len(self.points)
        inside = False
        x_inters = None
        p1x, p1y = self.points[0]
        for i in range(n + 1):
            p2x, p2y = self.points[i % n]
            if min(p1y, p2y) < y <= max(p1y, p2y) and x <= max(p1x, p2x):
                if p1y != p2y:
                    x_inters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x or x <= x_inters:
                    inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def check_mouse_collision(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.check_point_collision(mouse_x, mouse_y):
            pygame.draw.circle(self.screen, pygame.Color('blue'), (mouse_x, mouse_y), 5)

    def set_agent_box_collider(self, input_box_collider: pygame.Rect):
        self.agent_box_collider = input_box_collider

    def check_collision_with_square_corners(self, input_square: pygame.Rect):
        # sourcery skip: use-any, use-next
        """ Check if a square is inside a polygon and change its color """
        self.get_collision_type()
        points = input_square.bottomleft, input_square.bottomright, input_square.topleft, input_square.topright
        for point in points:
            if self.check_point_collision(*point):
                return True
        return False

    def check_agent_collision(self):
        if self.agent_box_collider is None:
            return
        collision_result = self.check_collision_with_square_corners(self.agent_box_collider)
        self.color = pygame.Color('red') if collision_result else pygame.Color('darkblue')
        return collision_result

    def get_collision_type(self):  # sourcery skip: use-next
        """This method raycasts a line in four directions, and returns the length and direction of the first
        collision """
        if self.agent_box_collider is None:
            return
        x, y = self.agent_box_collider.center
        ray_cast_range = 10
        bottom_test = x, y + ray_cast_range
        top_test = x, y - ray_cast_range
        left_test = x - ray_cast_range, y
        right_test = x + ray_cast_range, y
        point_pool = [bottom_test, top_test, left_test, right_test]
        point_tag = ['bottom', 'top', 'left', 'right']
        for point, tag in zip(point_pool, point_tag):
            if self.check_point_collision(*point):
                return tag
        return None
