import math
from pathlib import Path

import pygame

from agent_behavior.circular_sector_object import CircularSector
from agent_behavior.rotate_function import rotate
from references import get_assets_folder


class Agent:
    def __init__(self, x: int = 897, y: int = 556, input_image: str = "sage.png", initial_angle: int = 272,
                 initial_side: str = "attack", input_screen: pygame.Surface = None):
        self.x = x
        self.y = y
        self.pivot = (self.x, self.y)
        self.controllable = True
        image_ref = Path(get_assets_folder(), input_image)
        self.image = pygame.image.load(image_ref)
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.offset = pygame.math.Vector2(5, 0)
        self.side = initial_side
        self.angle = initial_angle
        self.speed = 3
        self.vision_field = None
        self.screen = input_screen
        self.box_collider = None
        self.can_move_up = True
        self.can_move_down = True
        self.can_move_left = True
        self.can_move_right = True
        self.can_rotate_clockwise = True
        self.can_rotate_counter_clockwise = True

    def handle_movement(self, input_keys: pygame.key):
        if input_keys[pygame.K_d]:
            self.rotate_clockwise()
        elif input_keys[pygame.K_a]:
            self.rotate_counter_clockwise()
        if input_keys[pygame.K_w]:
            self.move(direction="forward")
        elif input_keys[pygame.K_s]:
            self.move(direction="backward")

    def rotate_clockwise(self):
        if not self.can_rotate_clockwise:
            return
        self.angle += 1.7 * self.speed
        if self.angle >= 360:
            self.angle = self.angle - 360

    def rotate_counter_clockwise(self):
        if not self.can_rotate_counter_clockwise:
            return
        self.angle -= 1.7 * self.speed
        if self.angle <= 0:
            self.angle = 360 - self.angle

    def __extract_facing_coords(self) -> tuple[float, float]:
        radian_angle = math.radians(self.angle)
        return math.cos(radian_angle), math.sin(radian_angle)

    def move(self, direction: str = "forward"):
        """ Move forward in the direction the agent is facing"""
        delta_x, delta_y = self.__extract_facing_coords()
        factor = 1 if direction == "forward" else -1
        if 0 <= self.angle < 90:
            if self.can_move_right:
                self.x += delta_x * self.speed * factor
            if self.can_move_down:
                self.y += delta_y * self.speed * factor
        elif 90 <= self.angle < 180:
            if self.can_move_left:
                self.x += delta_x * self.speed * factor
            if self.can_move_down:
                self.y += delta_y * self.speed * factor
        elif 180 <= self.angle < 270:
            if self.can_move_left:
                self.x += delta_x * self.speed * factor
            if self.can_move_up:
                self.y += delta_y * self.speed * factor
        elif 270 <= self.angle < 360:
            if self.can_move_right:
                self.x += delta_x * self.speed * factor
            if self.can_move_up:
                self.y += delta_y * self.speed * factor

    def draw(self):
        self.update_sprite(self.screen)

    def update_sprite(self, screen):
        self.screen = screen
        self.rotate_sprite(screen)
        self.plot_agent_vision_cone()
        mouse_x, mouse_y = self.get_mouse_position()
        pygame.display.set_caption(f'Angle: {self.angle}, x: {mouse_x}, y: {mouse_y}')
        pygame.display.flip()

    def rotate_sprite(self, screen):
        pivot = (self.x, self.y)
        new_image, new_rect = rotate(self.image, self.angle, pivot, self.offset)
        screen.blit(new_image, new_rect)
        pygame.draw.circle(screen, (30, 250, 70), pivot, 3)  # Pivot point.
        self.box_collider = pygame.draw.rect(screen, (30, 250, 70), new_rect, 1)

    def check_border_collision(self):
        """Check if the agent has collided with the border of the screen."""
        self.can_rotate_clockwise, self.can_rotate_counter_clockwise = True, True
        height = self.screen.get_height() - 3
        width = self.screen.get_width() - 3
        top, bottom = self.box_collider.top, self.box_collider.bottom
        left, right = self.box_collider.left, self.box_collider.right
        if bottom >= height:
            self.can_move_down = False
        if top <= 0:
            self.can_move_up = False
        if right >= width:
            self.can_move_right = False
        if left <= 0:
            self.can_move_left = False
        return 0

    @staticmethod
    def get_mouse_position():
        return pygame.mouse.get_pos()

    def plot_agent_vision_cone(self):
        """Plot the vision cone of the agent. The vision cone is a 90 degrees arc"""
        direction = self.angle
        adjusted_direction = 360 - self.angle
        start_angle = math.radians(adjusted_direction - 45)
        stop_angle = math.radians(adjusted_direction + 45)
        self.vision_field = CircularSector(center=(self.x, self.y), radius=550, start_angle=start_angle,
                                           end_angle=stop_angle, direction=direction, screen=self.screen)
        self.vision_field.mouse_detection()
        return 0

    def allow_all_movements(self):
        self.can_move_down, self.can_move_up, self.can_move_right, self.can_move_left = True, True, True, True

    def set_collision_movement_restrictions(self, collision_type: str):
        if collision_type == "bottom":
            self.can_move_down = False
        elif collision_type == "top":
            self.can_move_up = False
        elif collision_type == "right":
            self.can_move_right = False
        elif collision_type == "left":
            self.can_move_left = False
