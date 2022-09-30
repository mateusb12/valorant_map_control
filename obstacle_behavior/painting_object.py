import pygame


class Panel:
    def __init__(self, points: list[list[float, float]], screen: pygame.Surface, area: str = "none"):
        self.points = points
        self.color = pygame.Color('yellow')
        self.screen = screen
        self.area = area
        self.polygon = None
        self.native_corners = []
        self.draw()

    def calculate_region_map_control(self) -> float:
        if not self.native_corners:
            return 0
        attack_corners = 0
        defense_corners = 0
        neutral_corners = 0
        for corner in self.native_corners:
            if corner.last_seen_by == "attack":
                attack_corners += 1
            elif corner.last_seen_by == "defense":
                defense_corners += 1
            elif corner.last_seen_by in ("neutral", "discovery"):
                neutral_corners += 1
        return attack_corners / (attack_corners + defense_corners + neutral_corners)

    def draw(self):
        self.draw_with_alpha_transparency()

    def draw_with_alpha_transparency(self):
        map_control = self.calculate_region_map_control()
        transparency = 75
        min_color = (0, 0, 255)
        max_color = (255, 0, 0)
        r, g, b = self.interpolate_colors(min_color, max_color, map_control)
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

    @staticmethod
    def interpolate_colors(min_rgb: tuple[int, int, int], max_rgb: tuple[int, int, int], ratio: float):
        """ Interpolate between two colors given a ratio. """
        r = int(min_rgb[0] + ratio * (max_rgb[0] - min_rgb[0]))
        g = int(min_rgb[1] + ratio * (max_rgb[1] - min_rgb[1]))
        b = int(min_rgb[2] + ratio * (max_rgb[2] - min_rgb[2]))
        return r, g, b