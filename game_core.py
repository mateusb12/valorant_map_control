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
        self.bg_image = pygame.image.load("assets/haven_map.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        self.screen.fill(BG_COLOR)
        self.pressed_keys = None

        sage = Agent(input_screen=self.screen)
        # chamber = Agent(x=184, y=590, initial_side="defense", input_screen=self.screen)
        # chamber.controllable = False
        self.agent_pool = [sage]
        self.current_agent = self.agent_pool[0]
        self.obstacle_manipulation.create_dummy_polygon()
        self.obstacle_manipulation.create_dummy_corner()
        self.obstacle_manipulation.create_dummy_painting()

    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.obstacle_manipulation.click_event()

            self.key_loop()
            self.draw_background()
            self.main_pipeline()
            self.clock.tick(FPS)
        pygame.quit()

    def key_loop(self):
        if not self.current_agent.controllable:
            return
        self.pressed_keys = pygame.key.get_pressed()
        self.obstacle_manipulation.pressed_keys = self.pressed_keys
        self.current_agent.handle_movement(self.pressed_keys)
        self.cursor_behavior.handle_cursors(self.pressed_keys)

    def draw_background(self):
        self.screen.blit(self.bg_image, (0, 0))

    def main_pipeline(self):
        self.current_agent.allow_all_movements()
        self.obstacle_pipeline()
        self.corner_pipeline(self.current_agent)
        self.painting_pipeline()
        for agent in self.agent_pool:
            agent.draw()
        return 0

    def obstacle_pipeline(self):
        if not self.current_agent.controllable:
            return
        for obstacle in self.obstacle_manipulation.obstacle_pool:
            if self.current_agent.box_collider is not None:
                obstacle.set_agent_box_collider(self.current_agent.box_collider)
            collision_result, collision_type = obstacle.obstacle_collision_check()
            self.current_agent.set_collision_movement_restrictions(collision_type)
            obstacle.draw()

    def corner_pipeline(self, input_agent: Agent):  # sourcery skip: use-named-expression
        for corner in self.obstacle_manipulation.corner_pool:
            if input_agent.vision_field is not None:
                if collision := input_agent.vision_field.check_point_collision(*corner.circle.center):
                    player_center = input_agent.box_collider.center
                    corner_center = corner.circle.center
                    edge = (player_center, corner_center)
                    intersection_results = [obstacle.check_intersection_with_polygon(edge)
                                            for obstacle in self.obstacle_manipulation.obstacle_pool]
                    if not any(intersection_results):
                        corner.line_of_sight = True
                        if corner.last_seen_by == "neutral":
                            corner.last_seen_by = "discovery"
                        if corner.last_seen_by != input_agent.side:
                            pygame.draw.line(self.screen, pygame.Color("green"), player_center, corner_center, 3)
                        corner.color = pygame.Color("green")
                        corner.line_of_sight = True
                elif corner.line_of_sight is True:
                    corner.last_seen_by = input_agent.side
            corner.draw()

    def painting_pipeline(self):
        for panel in self.obstacle_manipulation.painting_pool:
            panel.draw()


def __main():
    app = App()
    app.game_loop()


if __name__ == "__main__":
    __main()
