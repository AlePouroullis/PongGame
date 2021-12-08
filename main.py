# This is a sample Python script.
import pygame, sys, const
from Ball import Ball
from Player import Player
from AI import AI
from Point import Point
from Distance import Distance


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pong Game")
        self.screen = pygame.display.set_mode(const.DIMENSIONS)
        self.player = Player()
        self.ai = AI()
        # The order of the constructor parameters is as follows: x, y, vx, vy, radius
        self.ball = Ball(const.WIDTH // 2, const.HEIGHT // 2, 10)
        self.paddle_color = pygame.Color(const.RED)
        self.isStarted = False

        self.font = pygame.font.SysFont("Arial", 32)

    def draw(self):
        self.screen.fill(const.BLACK)
        pygame.draw.rect(self.screen, self.paddle_color, pygame.Rect(self.player.x, self.player.y,
                                                                     const.paddleWidth, const.paddleHeight))
        pygame.draw.rect(self.screen, self.paddle_color, pygame.Rect(self.ai.x, self.ai.y,
                                                                     const.paddleWidth, const.paddleHeight))
        pygame.draw.circle(self.screen, const.GREEN, (self.ball.x, self.ball.y), 10)

        self.screen.blit(self.font.render(str(self.player.score), True, const.WHITE), const.TOP_LEFT)
        self.screen.blit(self.font.render(str(self.ai.score), True, const.WHITE), const.TOP_RIGHT)

        pygame.display.flip()

    def reset_game(self):
        self.ball.respawn()
        self.player.reset()
        self.ai.reset()
        self.isStarted = False

    def check_collision_with_side_walls(self):
        if self.ball.is_off_left_side():
            self.ai.increment_score()
            self.reset_game()
        elif self.ball.is_off_right_side():
            self.player.increment_score()
            self.reset_game()

    def intersects(self, ball, rect_centre):
        dist_between_centres = Distance(ball.x, ball.y, rect_centre.x, rect_centre.y)

        if dist_between_centres.x > const.paddleWidth // 2 + ball.radius: return False
        if dist_between_centres.y > const.paddleHeight // 2 + ball.radius: return False

        if dist_between_centres.x <= const.paddleWidth // 2: return True
        if dist_between_centres.y <= const.paddleHeight // 2: return True

        corner_distance_sq = (dist_between_centres.x - const.paddleWidth // 2) ** 2 + (
                    dist_between_centres.y - const.paddleHeight // 2) ** 2

        return corner_distance_sq <= ball.radius ** 2

    def check_collision_with_paddles(self):
        player_paddle_centre = Point(self.player.x + const.paddleWidth // 2, self.player.y + const.paddleHeight // 2)
        ai_paddle_centre = Point(self.ai.x + const.paddleWidth // 2, self.ai.y + const.paddleHeight // 2)
        if self.intersects(self.ball, player_paddle_centre) or self.intersects(self.ball, ai_paddle_centre):
            self.ball.vx = -self.ball.vx


if __name__ == "__main__":
    game = Game()
    while True:
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not game.isStarted:
            game.isStarted = True
            game.ball.vx = 3
            game.ball.vy = 5

        if game.isStarted:
            mouse_pos = pygame.mouse.get_pos()
            game.player.move(mouse_pos[1])

            if keys[pygame.K_DOWN]:
                game.ai.move(game.ai.y + game.ai.speed)
            elif keys[pygame.K_UP]:
                game.ai.move(game.ai.y - game.ai.speed)

            game.ball.move()
            game.check_collision_with_side_walls()
            game.check_collision_with_paddles()

        game.draw()
