import pygame


class Triangle:
    def __init__(self, p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float],
                 screen: pygame.Surface):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.color = (0, 255, 0)
        self.screen = screen
        self.draw()

    def check_collision(self, x: int, y: int):
        """ Check if a point is inside a triangle """
        x1, y1 = self.p1
        x2, y2 = self.p2
        x3, y3 = self.p3
        denominator = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denominator
        b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denominator
        c = 1 - a - b
        return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1

    def draw(self):
        pygame.draw.polygon(self.screen, self.color, [self.p1, self.p2, self.p3])

    def mouse_detection(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.check_collision(mouse_x, mouse_y):
            pygame.draw.circle(self.screen, (255, 0, 0), (mouse_x, mouse_y), 5)
