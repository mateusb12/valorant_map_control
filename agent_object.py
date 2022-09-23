import math

import pygame

from valorant_map_game.pygame_example.rotate_function import rotate


class Agent:
    def __init__(self, x: int = 200, y: int = 250, input_image: str = "sage.png"):
        self.x = x
        self.y = y
        self.pivot = (self.x, self.y)
        self.image = pygame.image.load(input_image)
        self.offset = pygame.math.Vector2(50, 0)
        self.angle = 0
        self.speed = 5
        self.screen = None
        self.box_collider = None
        self.can_move_up = True
        self.can_move_down = True
        self.can_move_left = True
        self.can_move_right = True
        self.can_move_horizontally = True
        self.can_move_vertically = True

    def handle_movement(self, input_keys: pygame.key):
        if input_keys[pygame.K_d]:
            self.rotate_clockwise()
        elif input_keys[pygame.K_a]:
            self.rotate_counter_clockwise()
        if input_keys[pygame.K_w]:
            self.move_forward()
        elif input_keys[pygame.K_s]:
            self.move_backward()

    def rotate_clockwise(self):
        self.angle += 1 * self.speed
        if self.angle >= 360:
            self.angle = self.angle - 360

    def rotate_counter_clockwise(self):
        self.angle -= 1 * self.speed
        if self.angle <= 0:
            self.angle = 360 - self.angle

    def __extract_facing_coords(self) -> tuple[float, float]:
        radian_angle = math.radians(self.angle)
        return math.cos(radian_angle), math.sin(radian_angle)

    def move_forward(self):
        """ Move forward in the direction the agent is facing"""
        delta_x, delta_y = self.__extract_facing_coords()
        if 0 <= self.angle < 90:
            if self.can_move_right:
                self.x += delta_x * self.speed
            if self.can_move_down:
                self.y += delta_y * self.speed
        elif 90 <= self.angle < 180:
            if self.can_move_left:
                self.x += delta_x * self.speed
            if self.can_move_down:
                self.y += delta_y * self.speed
        elif 180 <= self.angle < 270:
            if self.can_move_left:
                self.x += delta_x * self.speed
            if self.can_move_up:
                self.y += delta_y * self.speed
        elif 270 <= self.angle < 360:
            if self.can_move_right:
                self.x += delta_x * self.speed
            if self.can_move_up:
                self.y += delta_y * self.speed

    def move_backward(self):
        """ Move backward in the direction the agent is facing"""
        delta_x, delta_y = self.__extract_facing_coords()
        if self.can_move_horizontally:
            self.x -= delta_x * self.speed
        if self.can_move_vertically:
            self.y -= delta_y * self.speed

    def draw(self, screen):
        self.update_sprite(screen)

    def update_sprite(self, screen):
        self.screen = screen
        pivot = (self.x, self.y)
        new_image, new_rect = rotate(self.image, self.angle, pivot, self.offset)
        screen.blit(new_image, new_rect)
        pygame.draw.circle(screen, (30, 250, 70), pivot, 3)  # Pivot point.
        self.box_collider = pygame.draw.rect(screen, (30, 250, 70), new_rect, 1)
        mouse_x, mouse_y = self.get_mouse_position()
        if self.box_collider:
            side_caption = f"| Top → {self.box_collider.top} | Bottom → {self.box_collider.bottom} | " \
                           f"Left → {self.box_collider.left} | Right → {self.box_collider.right}"
        else:
            side_caption = ""
        pygame.display.set_caption(f'Angle: {self.angle}, x: {mouse_x}, y: {mouse_y}, {side_caption}')
        pygame.display.flip()

    def __get_hit_box_points(self):
        return [self.box_collider.topleft, self.box_collider.topright,
                self.box_collider.bottomleft, self.box_collider.bottomright]

    def check_border_collision(self):
        """Check if the agent has collided with the border of the screen."""
        self.can_move_up, self.can_move_down, self.can_move_right, self.can_move_left = True, True, True, True
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

    def export_self_limits(self):
        return self.box_collider

    def check_collision_with_another_square(self, obstacle: pygame.Rect):
        if not self.box_collider.colliderect(obstacle):
            return
        if obstacle.top - self.box_collider.bottom <= 20:
            self.can_move_down = False
        if obstacle.bottom - self.box_collider.top <= 20:
            self.can_move_up = False
        if obstacle.left - self.box_collider.right <= 20:
            self.can_move_right = False
        if obstacle.right - self.box_collider.left <= 20:
            self.can_move_left = False
        print("collision")
        return True

    @staticmethod
    def get_mouse_position():
        return pygame.mouse.get_pos()
