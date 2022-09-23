# import math
#
# import pygame
#
#
# def rotate(surface, input_angle, input_pivot, input_offset):
#     """Rotate the surface around the pivot point.
#
#     Args:
#         surface (pygame.Surface): The surface that is to be rotated.
#         input_angle (float): Rotate by this angle.
#         input_pivot (tuple, list, pygame.math.Vector2): The pivot point.
#         input_offset (pygame.math.Vector2): This vector is added to the pivot.
#     """
#     rotated_image_a = pg.transform.rotozoom(surface, -input_angle, 1)  # Rotate the image.
#     rotated_offset = input_offset.rotate(input_angle)  # Rotate the offset vector.
#     # Add the offset vector to the center/pivot point to shift the rect.
#     transformed_rect = rotated_image_a.get_rect(center=input_pivot + rotated_offset)
#     return rotated_image_a, transformed_rect  # Return the rotated image and shifted rect.
#
#
# BG_COLOR = pg.Color('gray12')
# FPS = 60
# WIDTH, HEIGHT = 800, 600
# SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
#
#
# class App:
#     def __init__(self):
#         pg.init()
#         self.screen = SCREEN
#         self.clock = pg.time.Clock()
#
#         self.agent = Agent()
#
#         self.x = 200
#         self.y = 250
#         self.offset = pg.math.Vector2(50, 0)
#         self.angle = 0
#
#     def game_loop(self):
#
#         running = True
#         while running:
#             for event in pg.event.get():
#                 if event.type == pg.QUIT:
#                     running = False
#
#             keys = pg.key.get_pressed()
#             self.agent.handle_movement(keys)
#             self.screen.fill(BG_COLOR)
#             self.agent.update_sprite(self.screen)
#             self.clock.tick(FPS)
#         pg.quit()
#
#
# class Agent:
#     def __init__(self, input_image: str = "sage.png"):
#         self.x = 200
#         self.y = 250
#         self.pivot = (self.x, self.y)
#         self.image = pygame.image.load(input_image)
#         self.offset = pg.math.Vector2(50, 0)
#         self.angle = 0
#         self.speed = 5
#
#     def handle_movement(self, input_keys: pygame.key):
#         if input_keys[pg.K_d]:
#             self.rotate_clockwise()
#         elif input_keys[pg.K_a]:
#             self.rotate_counter_clockwise()
#         if input_keys[pg.K_w]:
#             self.move_forward()
#         elif input_keys[pg.K_s]:
#             self.move_backward()
#
#     def rotate_clockwise(self):
#         self.angle += 1 * self.speed
#         if self.angle == 360:
#             self.angle = 0
#
#     def rotate_counter_clockwise(self):
#         self.angle -= 1 * self.speed
#         if self.angle == -1:
#             self.angle = 359
#
#     def __extract_facing_coords(self) -> tuple[float, float]:
#         radian_angle = math.radians(self.angle)
#         return math.cos(radian_angle), math.sin(radian_angle)
#
#     def move_forward(self):
#         """ Move forward in the direction the agent is facing"""
#         delta_x, delta_y = self.__extract_facing_coords()
#         self.x += delta_x * self.speed
#         self.y += delta_y * self.speed
#
#     def move_backward(self):
#         """ Move backward in the direction the agent is facing"""
#         delta_x, delta_y = self.__extract_facing_coords()
#         self.x -= delta_x * self.speed
#         self.y -= delta_y * self.speed
#
#     def update_sprite(self, screen):
#         pivot = (self.x, self.y)
#         new_image, new_rect = rotate(self.image, self.angle, pivot, self.offset)
#         screen.blit(new_image, new_rect)
#         pg.draw.circle(screen, (30, 250, 70), pivot, 3)  # Pivot point.
#         pg.draw.rect(screen, (30, 250, 70), new_rect, 1)
#         pg.display.set_caption(f'Angle: {self.angle}')
#         pg.display.flip()
#
#
# def __main():
#     a = App()
#     a.game_loop()
#
#
# if __name__ == '__main__':
#     __main()
