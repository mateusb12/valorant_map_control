import pygame

from valorant_map_game.pygame_example.agent_object import Agent

BG_COLOR = pygame.Color('gray12')
FPS = 60
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


class App:
    def __init__(self):
        pygame.init()
        self.screen = SCREEN
        self.clock = pygame.time.Clock()

        self.sage = Agent()
        # self.chamber = Agent(x=400, y=200, input_image="chamber.png")
        self.obstacle = pygame.Rect(400, 200, 100, 100)

    def game_loop(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            self.sage.handle_movement(keys)
            self.draw_loop()
            self.collision_check()
            self.clock.tick(FPS)
        pygame.quit()

    def draw_loop(self):
        self.screen.fill(BG_COLOR)
        pygame.draw.rect(self.screen, pygame.Color('orange'), self.obstacle)
        self.sage.draw(self.screen)
        # self.chamber.draw(self.screen)

    def collision_check(self):
        self.sage.can_move_up, self.sage.can_move_down,  = True, True
        self.sage.can_move_right, self.sage.can_move_left = True, True
        self.sage.check_border_collision()
        self.sage.check_collision_with_another_square(self.obstacle)
        return 0


def __main():
    app = App()
    app.game_loop()


if __name__ == "__main__":
    __main()
