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

        if dist_between_centres.x <= const.paddleWidth // 2:
            return True
        if dist_between_centres.y <= const.paddleHeight // 2:
            return True

        corner_distance_sq = (dist_between_centres.x - const.paddleWidth // 2) ** 2 + (
                    dist_between_centres.y - const.paddleHeight // 2) ** 2

        return corner_distance_sq <= ball.radius**2

    def collides_with_top_or_bottom(self, dist_between_centres):
        if dist_between_centres.x <= const.paddleWidth // 2:
            return True

    def collides_with_side(self, dist_between_centres):
        if dist_between_centres.y <= const.paddleHeight // 2:
            return True

    def collides_with_corner(self, dist_between_centres):
        corner_distance_sq = (dist_between_centres.x - const.paddleWidth//2)**2 + (
                                dist_between_centres.y - const.paddleHeight//2)**2

        return corner_distance_sq <= self.ball.radius**2

    def check_collision_with_paddles(self):
        player_paddle_centre = Point(self.player.x + const.paddleWidth // 2, self.player.y + const.paddleHeight // 2)
        ai_paddle_centre = Point(self.ai.x + const.paddleWidth // 2, self.ai.y + const.paddleHeight // 2)
        dist_between_ai_and_ball_centres = Distance(self.ball.x, self.ball.y, ai_paddle_centre.x, ai_paddle_centre.y)
        dist_between_player_and_ball_centres = Distance(self.ball.x, self.ball.y,
                                                        player_paddle_centre.x, player_paddle_centre.y)

        if (dist_between_player_and_ball_centres.x > const.paddleWidth // 2 + self.ball.radius) and (
                dist_between_ai_and_ball_centres.x > const.paddleWidth // 2 + self.ball.radius): return
        if (dist_between_player_and_ball_centres.y > const.paddleHeight // 2 + self.ball.radius) and (
                dist_between_ai_and_ball_centres.y > const.paddleHeight // 2 + self.ball.radius): return

        if self.collides_with_top_or_bottom(dist_between_player_and_ball_centres):
            self.ball.vy = -self.ball.vy
            # if the ball collides with the top of the paddle
            if self.ball.y > player_paddle_centre.y:
                print("collided with the bottom of the player")
                self.ball.y = self.player.y + const.paddleHeight + self.ball.radius
            else:
                print('collided with the top of the player')
                self.ball.y = self.player.y - self.ball.radius

        if self.collides_with_top_or_bottom(dist_between_ai_and_ball_centres):
            self.ball.vy = -self.ball.vy
            # if the ball collides with the top of the paddle
            if self.ball.y > ai_paddle_centre.y:
                print("collided with the bottom of ai")
                self.ball.y = self.ai.y + const.paddleHeight + self.ball.radius
            else:
                print("collided with the top of the ai")
                self.ball.y = self.ai.y - self.ball.radius

        if self.collides_with_corner(dist_between_player_and_ball_centres):
            print("collided with the corner of the player")
            self.ball.vy = -self.ball.vy
            self.ball.vx = -self.ball.vx
            # if the ball collides with the top corner.
            if self.ball.y > player_paddle_centre.y:
                self.ball.y = self.player.y - self.ball.radius
                self.ball.x = self.player.x + const.paddleWidth + self.ball.radius
            else:
                self.ball.y = self.player.y + const.paddleHeight + self.ball.radius
                self.ball.x = self.player.x + const.paddleWidth + self.ball.radius

        if self.collides_with_corner(dist_between_ai_and_ball_centres):
            print("collided with the corner of the ai")
            self.ball.vy = -self.ball.vy
            self.ball.vx = -self.ball.vx
            # if the ball collides with the top corner.
            if self.ball.y < ai_paddle_centre.y:
                self.ball.y = self.ai.y + self.ball.radius
                self.ball.x = self.ai.x + const.paddleWidth + self.ball.radius
            else:
                self.ball.y = self.ai.y + const.paddleHeight + self.ball.radius
                self.ball.x = self.ai.x - self.ball.radius

        if self.collides_with_side(dist_between_player_and_ball_centres):
            print("collided with the side of the player")
            self.ball.vx = -self.ball.vx
            self.ball.x = self.player.x + const.paddleWidth + self.ball.radius

        if self.collides_with_side(dist_between_ai_and_ball_centres):
            print("collided with the side of the ai")
            self.ball.vx = -self.ball.vx
            self.ball.x = self.ai.x - self.ball.radius



if __name__ == "__main__":
    game = Game()
    while True:
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not game.isStarted:
            game.isStarted = True
            game.ball.vx = 6
            game.ball.vy = 8

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
