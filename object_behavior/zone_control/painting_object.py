from typing import Union, Tuple

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

    def calculate_region_map_control(self) -> Union[int, tuple[float, float, float]]:
        if not self.native_corners:
            return 0, 0, 1
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
        # attack_proportion = attack_corners / (attack_corners + defense_corners + neutral_corners)
        # defense_proportion = defense_corners / (attack_corners + defense_corners + neutral_corners)
        # unknown_proportion = neutral_corners / (attack_corners + defense_corners + neutral_corners)
        atk_def = attack_corners + defense_corners
        # relative_proportion = attack_corners / atk_def if atk_def != 0 else 0
        return attack_corners, defense_corners, neutral_corners

    def draw(self):
        self.draw_with_alpha_transparency()

    def draw_with_alpha_transparency(self):
        attack_corners, defense_corners, neutral_corners = self.calculate_region_map_control()
        total_size = attack_corners + defense_corners + neutral_corners
        neutral_proportion = neutral_corners / total_size if total_size != 0 else 0
        attack_over_defense_proportion = attack_corners / (attack_corners + defense_corners) \
            if attack_corners + defense_corners != 0 else 0
        transparency = int(150 + (35 - 150) * neutral_proportion)
        min_color = (0, 0, 255) if neutral_proportion < 0.9 else (239, 255, 117)
        max_color = (255, 0, 0) if neutral_proportion < 0.9 else (255, 174, 0)
        r, g, b = self.interpolate_colors(min_color, max_color, attack_over_defense_proportion)
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