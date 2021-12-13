# This is a sample Python script.
import pygame, sys, const, random
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
        # The order of the constructor parameters is as follows: x, y, radius
        self.ball = Ball(const.WIDTH//2, const.HEIGHT//2, 10)
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

    def intersects(self, dist_between_centres):
        if dist_between_centres.x > const.paddleWidth // 2 + self.ball.radius: return False
        if dist_between_centres.y > const.paddleHeight // 2 + self.ball.radius: return False

        if dist_between_centres.x <= const.paddleWidth // 2: return True
        if dist_between_centres.y <= const.paddleHeight // 2: return True

        corner_distance_sq = (dist_between_centres.x - const.paddleWidth // 2)*(dist_between_centres.x - const.paddleWidth // 2) + (
                                dist_between_centres.y - const.paddleHeight // 2)*(dist_between_centres.y - const.paddleHeight//2)
        return corner_distance_sq <= self.ball.radius**2

    def speed_factor(self, ball, paddle):
        # The y-values of both the ball and paddle in this case represent the y-coordinates of their centres.
        # ||  1 <-- top of paddle
        # ||
        # ||  0 <-- middle of paddle
        # ||
        # || -1 <-- bottom of paddle
        return (ball.y - paddle.y) / (const.paddleHeight // 2)


    def check_collision_with_paddles(self):
        player_paddle_centre = Point(self.player.x + const.paddleWidth//2, self.player.y + const.paddleHeight//2)
        ai_paddle_centre = Point(self.ai.x + const.paddleWidth//2, self.ai.y + const.paddleHeight//2)

        dist_between_centres_of_player_and_ball = Distance(self.ball.x, self.ball.y, player_paddle_centre.x, player_paddle_centre.y)
        dist_between_centres_of_ai_and_ball = Distance(self.ball.x, self.ball.y, ai_paddle_centre.x, ai_paddle_centre.y)

        if self.intersects(dist_between_centres_of_player_and_ball):
            if dist_between_centres_of_player_and_ball.y <= const.paddleHeight//2:
                while self.intersects(dist_between_centres_of_player_and_ball):
                    self.ball.x += 1
                    dist_between_centres_of_player_and_ball = Distance(self.ball.x, self.ball.y, player_paddle_centre.x, player_paddle_centre.y)
                self.ball.vx = -self.ball.vx
            elif dist_between_centres_of_player_and_ball.x <= const.paddleHeight//2:
                while self.intersects(dist_between_centres_of_player_and_ball):
                    # if it collides on top
                    if self.ball.y < player_paddle_centre.y:
                        self.ball.y -= 1
                    else:
                        self.ball.y += 1
                    dist_between_centres_of_player_and_ball = Distance(self.ball.x, self.ball.y, player_paddle_centre.x, player_paddle_centre.y)
                self.ball.vy = -self.ball.vy

        elif self.intersects(dist_between_centres_of_ai_and_ball):
            if dist_between_centres_of_ai_and_ball.y <= const.paddleHeight//2:
                while self.intersects(dist_between_centres_of_ai_and_ball):
                    self.ball.x -= 1
                    dist_between_centres_of_ai_and_ball = Distance(self.ball.x, self.ball.y, ai_paddle_centre.x, ai_paddle_centre.y)
                self.ball.vx = -self.ball.vx
            elif dist_between_centres_of_player_and_ball.x <= const.paddleWidth//2:
                while self.intersects(dist_between_centres_of_ai_and_ball):
                    # if it collides on top
                    if self.ball.y < ai_paddle_centre.y:
                        self.ball.y -=1
                    else:
                        self.ball.y += 1
                    dist_between_centres_of_player_and_ball = Distance(self.ball.x, self.ball.y, ai_paddle_centre.x, ai_paddle_centre.y)
                self.ball.vy = -self.ball.vy





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
