import pygame


class PolygonObstacle:
    def __init__(self, points: list[tuple[float, float]], screen: pygame.Surface):
        self.points = points
        self.color = (0, 255, 0)
        self.screen = screen
        self.draw()

    def draw(self):
        pygame.draw.polygon(self.screen, self.color, self.points)