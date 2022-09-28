import pygame

from agent_behavior.agent_object import Agent
from agent_behavior.polygon_obstacle import PolygonObstacle
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
        self.obstacle_manipulation = ObstacleManipulation(self.cursor_behavior, self.screen)
        self.pressed_keys = None

        self.sage = Agent()
        self.obstacle_manipulation.create_dummy_polygon()
        self.obstacle_manipulation.create_dummy_corner()
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
            self.obstacle_manipulation.pressed_keys = self.pressed_keys
            self.sage.handle_movement(self.pressed_keys)
            self.cursor_behavior.handle_cursors(self.pressed_keys)
            self.draw_loop()
            # self.collision_check()
            self.clock.tick(FPS)
        pygame.quit()

    def draw_loop(self):
        self.screen.fill(BG_COLOR)
        bg_image = pygame.image.load("assets/haven_map.png")
        bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
        self.screen.blit(bg_image, (0, 0))

        self.collision_check()
        self.sage.draw(self.screen)

    def collision_check(self):
        self.sage.allow_all_movements()
        self.obstacle_pipeline()
        self.corner_pipeline()
        return 0

    def obstacle_pipeline(self):
        for obstacle in self.obstacle_manipulation.obstacle_pool:
            if self.sage.box_collider is not None:
                obstacle.set_agent_box_collider(self.sage.box_collider)
            collision_result, collision_type = obstacle.collision_check()
            self.sage.set_collision_movement_restrictions(collision_type)
            # if self.sage.vision_field is not None:
            #     edge = self.sage.vision_field.mouse_detection()
            #     if edge_collision := obstacle.check_intersection_with_polygon(edge):
            #         obstacle.color = pygame.Color("red")
            obstacle.draw()

    def corner_pipeline(self):
        for corner in self.obstacle_manipulation.corner_pool:
            if self.sage.vision_field is not None:
                if collision := self.sage.vision_field.check_point_collision(*corner.circle.center):
                    current_color = pygame.Color("green")
                    player_center = self.sage.box_collider.center
                    corner_center = corner.circle.center
                    edge = (player_center, corner_center)
                    for obstacle in self.obstacle_manipulation.obstacle_pool:
                        if obstacle.check_intersection_with_polygon(edge):
                            current_color = pygame.Color("red")
                    pygame.draw.line(self.screen, current_color, player_center, corner_center, 3)
                    corner.color = current_color
                else:
                    corner.color = pygame.Color("red")
            corner.draw()


def __main():
    app = App()
    app.game_loop()


if __name__ == "__main__":
    __main()
