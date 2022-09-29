import pygame


class Corner:
    def __init__(self, x: int, y: int, screen: pygame.Surface):
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        self.screen = None
        self.radius = 4
        self.circle = None
        self.screen = screen
        self.line_of_sight = False
        self.draw()

    def draw(self):
        self.circle = pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
