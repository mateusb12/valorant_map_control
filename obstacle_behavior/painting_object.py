import pygame


class Panel:
    def __init__(self, points: list[list[float, float]], screen: pygame.Surface):
        self.points = points
        self.color = pygame.Color('yellow')
        self.screen = screen
        self.polygon = None
        self.draw()

    def draw(self):
        # self.polygon = pygame.draw.polygon(self.screen, self.color, self.points)
        self.create_alpha_transparency()

    def create_alpha_transparency(self):
        transparency = 100
        r, g, b = (247, 255, 5)
        color_with_transparency = (r, g, b, transparency)
        self.draw_polygon_alpha(self.screen, color_with_transparency, self.points)

    @staticmethod
    def draw_polygon_alpha(surface, color, points):
        lx, ly = zip(*points)
        min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
        target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
        surface.blit(shape_surf, target_rect)