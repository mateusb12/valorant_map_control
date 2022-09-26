import pygame


class CursorBehavior:
    def __init__(self):
        self.current_cursor_task = "normal"

    def handle_cursors(self, input_keys: pygame.key) -> None:
        if input_keys[pygame.K_F1]:
            self.set_task_to_normal()
        if input_keys[pygame.K_F2]:
            self.set_task_to_rectangle_creator()
        if input_keys[pygame.K_F3]:
            self.set_task_to_rectangle_mover()
        if input_keys[pygame.K_F4]:
            self.set_task_to_rectangle_deleter()
        if input_keys[pygame.K_ESCAPE]:
            self.set_task_to_rectangle_finisher()

    def set_task_to_normal(self):
        self.current_cursor_task = "normal"
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

    def set_task_to_rectangle_creator(self):
        self.current_cursor_task = "rectangle_creator"
        pygame.mouse.set_cursor(pygame.cursors.diamond)

    def set_task_to_rectangle_mover(self):
        self.current_cursor_task = "rectangle_mover"
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def set_task_to_rectangle_deleter(self):
        self.current_cursor_task = "rectangle_deleter"
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    def set_task_to_rectangle_finisher(self):
        self.current_cursor_task = "rectangle_finisher"
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)

