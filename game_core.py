import pygame

from agent_object import Agent
from cursor_changing import CursorBehavior
from tools import rectangle_parameters_from_coordinates

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

        self.sage = Agent()
        self.obstacle_pool = []
        rectangle_points = [(547, 626), (700, 627), (545, 678), (700, 676)]
        rectangle_params = rectangle_parameters_from_coordinates(*rectangle_points)
        new_obstacle = pygame.Rect(rectangle_params)
        self.obstacle_pool.append(new_obstacle)

        self.clicks = 0
        self.click_positions = []

        self.selected_obstacle = None

        # Bind F1 to set the cursor to normal.

    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click_event()

            keys = pygame.key.get_pressed()
            self.sage.handle_movement(keys)
            self.cursor_behavior.handle_cursors(keys)
            self.draw_loop()
            self.collision_check()
            self.clock.tick(FPS)
        pygame.quit()

    def draw_loop(self):
        self.screen.fill(BG_COLOR)
        bg_image = pygame.image.load("assets/haven_map.png")
        bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
        self.screen.blit(bg_image, (0, 0))

        for obstacle in self.obstacle_pool:
            pygame.draw.rect(self.screen, pygame.Color('orange'), obstacle)
        self.sage.draw(self.screen)
        # self.chamber.draw(self.screen)

    def collision_check(self):
        self.sage.can_move_up, self.sage.can_move_down, = True, True
        self.sage.can_move_right, self.sage.can_move_left = True, True
        obstacle_list = self.obstacle_pool
        self.sage.collision_pipeline(obstacle_list)
        return 0

    def click_event(self):
        if self.cursor_behavior.current_cursor_task == "rectangle_creator":
            self.rectangle_creator_from_clicks()
        if self.cursor_behavior.current_cursor_task == "rectangle_mover":
            self.move_clicked_obstacle()

    def rectangle_creator_from_clicks(self):
        self.clicks += 1
        self.click_positions.append(pygame.mouse.get_pos())
        if self.clicks == 4:
            print(self.click_positions)
            self.create_obstacle_from_clicks(self.click_positions)
            self.clicks = 0
            self.click_positions = []

    def create_obstacle_from_clicks(self, click_list: list[tuple[int, int]]) -> None:
        rectangle_params = rectangle_parameters_from_coordinates(*click_list)
        new_obstacle = pygame.Rect(rectangle_params)
        self.obstacle_pool.append(new_obstacle)

    def move_clicked_obstacle(self):
        if not self.selected_obstacle:
            self.select_obstacle()
        else:
            self.move_selected_obstacle()
            self.selected_obstacle = None

    def select_obstacle(self) -> pygame.Rect:
        mouse_coords = pygame.mouse.get_pos()
        for obstacle in self.obstacle_pool:
            if obstacle.collidepoint(mouse_coords):
                self.selected_obstacle = obstacle
                print(obstacle)
                return obstacle

    def move_selected_obstacle(self):
        self.selected_obstacle.center = pygame.mouse.get_pos()
        self.selected_obstacle = None


def __main():
    app = App()
    app.game_loop()


if __name__ == "__main__":
    __main()
