import pygame

from agent_behavior.agent_object import Agent
from mouse_behavior.cursor_changing import CursorBehavior
from obstacle_behavior.obstacle_manipulation import ObstacleManipulation

BG_COLOR = pygame.Color('gray12')
FPS = 60
# WIDTH, HEIGHT = 800, 600
WIDTH, HEIGHT = 1400, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


class App:
    def __init__(self):
        pygame.init()
        self.screen = SCREEN
        self.clock = pygame.time.Clock()
        self.cursor_behavior = CursorBehavior()
        self.obstacle_manipulation = ObstacleManipulation(self.cursor_behavior)
        self.pressed_keys = None

        self.sage = Agent()
        # Bind F1 to set the cursor to normal.

    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # self.click_event()
                    self.obstacle_manipulation.click_event()

            self.pressed_keys = pygame.key.get_pressed()
            self.sage.handle_movement(self.pressed_keys)
            self.cursor_behavior.handle_cursors(self.pressed_keys)
            self.draw_loop()
            self.collision_check()
            self.clock.tick(FPS)
        pygame.quit()

    def draw_loop(self):
        self.screen.fill(BG_COLOR)
        bg_image = pygame.image.load("assets/haven_map.png")
        bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
        self.screen.blit(bg_image, (0, 0))

        for obstacle in self.obstacle_manipulation.obstacle_pool:
            pygame.draw.rect(self.screen, pygame.Color('orange'), obstacle)
        self.sage.draw(self.screen)
        # self.chamber.draw(self.screen)

    def collision_check(self):
        self.sage.can_move_up, self.sage.can_move_down, = True, True
        self.sage.can_move_right, self.sage.can_move_left = True, True
        obstacle_list = self.obstacle_manipulation.obstacle_pool
        self.sage.collision_pipeline(obstacle_list)
        return 0


def __main():
    app = App()
    app.game_loop()


if __name__ == "__main__":
    __main()
