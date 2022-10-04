import pygame

from agent_behavior.agent_object import Agent
from agent_behavior.polygon_obstacle import PolygonObstacle


class Corner:
    def __init__(self, x: int, y: int, screen: pygame.Surface, last_seen_by: str = "neutral", area: str = "none"):
        self.x = x
        self.y = y
        self.last_seen_by = last_seen_by
        self.color = self.evaluate_color()
        self.screen = None
        self.radius = 4
        self.circle = None
        self.screen = screen
        self.line_of_sight = False
        self.area = area
        self.draw()

    def evaluate_color(self):
        if self.last_seen_by == "neutral":
            return pygame.Color("darkolivegreen2")
        elif self.last_seen_by == "attack":
            return pygame.Color("red")
        elif self.last_seen_by == "defense":
            return pygame.Color("cyan")
        elif self.last_seen_by == "discovery":
            return pygame.Color("green")

    def draw(self):
        self.color = self.evaluate_color()
        self.circle = pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def discovery_method(self, input_agent: Agent, obstacle_pool: list[PolygonObstacle]):
        player_center = input_agent.box_collider.center
        corner_center = self.circle.center
        line_of_sight_ray = (player_center, corner_center)
        intersection_results = [obstacle.check_intersection_with_polygon(line_of_sight_ray)
                                for obstacle in obstacle_pool]
        neutral_corner = self.area.startswith("t_") if input_agent.side == "attack" else self.area.startswith("ct_")
        if not any(intersection_results):
            self.line_of_sight = True
            if self.last_seen_by == "neutral":
                self.last_seen_by = "discovery"
            if not neutral_corner:
                self.color = pygame.Color("green")
                pygame.draw.line(self.screen, pygame.Color("green"), player_center, corner_center, 3)
            self.color = pygame.Color("green")
            self.line_of_sight = True
            self.last_seen_by = input_agent.side

