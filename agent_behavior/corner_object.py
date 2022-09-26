import pygame


class Corner:
    def __init__(self, x: int, y: int, screen: pygame.Surface):
        self.x = x
        self.y = y
        self.color = (0, 255, 0)
        self.screen = None
        self.radius = 10
        self.circle_color = pygame.Color("red")
        self.screen = screen
        self.draw()

    def draw(self):
        pygame.draw.circle(self.screen, self.circle_color, (self.x, self.y), self.radius)