import pygame


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
