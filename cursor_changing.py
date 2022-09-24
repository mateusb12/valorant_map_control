import pygame


class CursorBehavior:
    def __init__(self):
        self.cursor_task = "normal"

    def handle_cursors(self, input_keys: pygame.key) -> None:
        if input_keys[pygame.K_F1]:
            self.cursor_task = "normal"
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
        if input_keys[pygame.K_F2]:
            self.cursor_task = "rectangle_creator"
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        if input_keys[pygame.K_F3]:
            self.cursor_task = "rectangle_mover"
            pygame.mouse.set_cursor(*pygame.cursors.diamond)

