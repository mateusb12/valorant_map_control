import math

import pygame


class CircularSector:
    def __init__(self, center: tuple[float, float], radius: float, start_angle: float, end_angle: float,
                 direction: int,
                 screen: pygame.Surface):
        self.x, self.y = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.color = (0, 255, 0)
        self.screen = screen
        self.triangle_first_corner = (self.x, self.y)
        self.triangle_second_corner = (self.x + self.radius * math.cos(math.radians(direction - 45)),
                                       self.y + self.radius * math.sin(math.radians(direction - 45)))
        self.triangle_third_corner = (self.x + self.radius * math.cos(math.radians(direction + 45)),
                                      self.y + self.radius * math.sin(math.radians(direction + 45)))
        self.direction = direction
        self.draw()

    def draw(self):
        pygame.draw.arc(self.screen, self.color, (self.x - self.radius, self.y - self.radius,
                                                  self.radius * 2, self.radius * 2), self.start_angle, self.end_angle,
                        1)
        # pygame.draw.polygon(self.screen, self.color, [self.triangle_first_corner, self.triangle_second_corner,
        #                                               self.triangle_third_corner])
        pygame.draw.line(self.screen, self.color, self.triangle_first_corner, self.triangle_second_corner, 1)
        pygame.draw.line(self.screen, self.color, self.triangle_first_corner, self.triangle_third_corner, 1)

    def check_collision(self, x: int, y: int) -> bool:
        """ Check if a point is inside a circular sector """
        diff_x = x - self.x
        diff_y = y - self.y
        arc_angle = math.atan2(diff_y, diff_x)
        angle = math.degrees(arc_angle)
        min_angle = self.direction - 45
        max_angle = self.direction + 45
        if min_angle < 0:
            min_angle += 360
        if angle < 0:
            angle += 360
        if min_angle < max_angle:
            first_condition = min_angle <= angle <= max_angle
        else:
            first_condition = min_angle <= angle or angle <= max_angle
        hypotenuse = math.sqrt(diff_x ** 2 + diff_y ** 2)
        second_condition = hypotenuse <= self.radius
        return first_condition and second_condition

    def mouse_detection(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.check_collision(mouse_x, mouse_y):
            pygame.draw.circle(self.screen, (255, 0, 0), (mouse_x, mouse_y), 5)


def __main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True
    circular_sector = CircularSector((400, 300), 100, 0, math.radians(90), 0, screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        circular_sector.draw()
        circular_sector.mouse_detection()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    __main()
