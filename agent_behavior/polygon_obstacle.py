import math

import pygame


class PolygonObstacle:
    def __init__(self, points: list[tuple[float, float]], screen: pygame.Surface):
        self.points = points
        self.color = pygame.Color('black')
        self.edges = []
        self.create_edges(points)
        self.screen = screen
        self.agent_box_collider = None
        self.polygon = None
        self.draw()

    def get_polygon_size(self):
        max_x = max(self.points, key=lambda x: x[0])[0]
        min_x = min(self.points, key=lambda x: x[0])[0]
        max_y = max(self.points, key=lambda x: x[1])[1]
        min_y = min(self.points, key=lambda x: x[1])[1]
        return max_x - min_x, max_y - min_y

    def draw(self):
        self.polygon = pygame.draw.polygon(self.screen, self.color, self.points)
        # self.create_alpha_transparency()

    def create_edges(self, input_list: list):
        for i, j in zip(input_list, input_list[1:] + input_list[:1]):
            self.edges.append((i, j))

    @staticmethod
    def do_intersect(edge_a: tuple, edge_b: tuple):
        """ Check if two lines intersect """
        x1, y1 = edge_a[0]
        x2, y2 = edge_a[1]
        x3, y3 = edge_b[0]
        x4, y4 = edge_b[1]
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denominator == 0:
            return False
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
        return 0 <= t <= 1 and 0 <= u <= 1

    def check_intersection_with_polygon(self, input_edge: tuple):
        # sourcery skip: use-any, use-next
        for edge in self.edges:
            if self.do_intersect(edge, input_edge):
                return True
        return False

    def check_single_point_collision(self, x: int, y: int):
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
        if self.check_single_point_collision(mouse_x, mouse_y):
            pygame.draw.circle(self.screen, pygame.Color('blue'), (mouse_x, mouse_y), 5)

    def set_agent_box_collider(self, input_box_collider: pygame.Rect):
        self.agent_box_collider = input_box_collider

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
            if self.check_single_point_collision(*point):
                return tag
        return None

    def collision_check(self) -> tuple:  # sourcery skip: assign-if-exp, reintroduce-else
        if self.agent_box_collider is None:
            self.color = pygame.Color('black')
            return False, None
        collision_type = self.get_collision_type()
        if collision_type is None:
            self.color = pygame.Color('black')
            return False, None
        self.color = pygame.Color('red')
        return True, collision_type
