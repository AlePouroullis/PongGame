# This is a sample Python script.
import pygame, sys
from Ball import Ball
import constant

class gameLoop:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pong Game")
        self.screen = pygame.display.set_mode(constant.DIMENSIONS)
        self.player = pygame.Rect(50, constant.HEIGHT//2, constant.paddleWidth, constant.paddleHeight)
        self.opponent = pygame.Rect(constant.WIDTH-50, constant.HEIGHT//2, constant.paddleWidth, constant.paddleHeight)
        self.player_score = 0
        self.opponent_score = 0
        self.ball = Ball(constant.WIDTH//2, constant.HEIGHT//2, 10, 2, 2)
        self.paddle_color = pygame.Color(constant.RED)
        self.run = True

    def draw(self):
        self.screen.fill(constant.BLACK)
        pygame.draw.rect(self.screen, self.paddle_color, self.player)
        pygame.draw.circle(self.screen, constant.GREEN, (self.ball.x, self.ball.y), 10)
        pygame.draw.rect(self.screen, self.paddle_color, self.opponent)
        pygame.display.flip()

    def move_player(self, y):
        if y > constant.HEIGHT - self.player.height:
            self.player.bottom = constant.HEIGHT
        elif y < 0:
            self.player.top = 0
        else:
            self.player.top = y

    def pointInRectangle(self, circleCentre, A, B, C):
        """A represents the top left vertex, B the top right, C the bottom left and all parameters are tuples"""
        return A[0] <= circleCentre[0] <= B[0] and A[1] >= circleCentre[1] >= C[1]

    def Intersect(self, ball_centre, edge):
        return edgeball_centre[0]

    def intersect(self, ball, paddle):
        top_left = (self.paddle.left, self.paddle.top)
        top_right = (self.paddle.right, self.paddle.top)
        bottom_left = (self.paddle.left, self.paddle.bottom)
        bottom_right = (self.paddle.right, self.paddle.bottom)
        ball_centre = (self.ball.x, self.ball.y)
        return self.PointInRectangle(ball_centre, top_left, top_right, bottom_left) or
                self.Intersect(ball_centre, (top_left, top_right)) or
                self.Intersect(ball_centre, (top_right, bottom_right)) or
                self.Intersect(ball_centre, (bottom_left, bottom_right)) or
                self.Intersect(ball_centre, (top_left, bottom_left))

    def move_ball(self):
        self.ball.x += self.ball.vx
        self.ball.y += self.ball.vy
        if self.ball.x <= 0:
            self.opponent_score += 1
            self.respawnBall()
        elif self.ball.x >= constant.WIDTH:
            self.player_score += 1
            self.respawnBall()
        if self.ball.y < 0 or self.ball.y > constant.HEIGHT:
            self.ball.vy = -self.ball.vy

    def respawnBall(self):
        self.ball.x = constant.WIDTH//2
        self.ball.y = constant.HEIGHT//2
        self.vx = 2
        self.vy = 2

if __name__ == "__main__":
    game = gameLoop()
    while game.run:
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game.run = False
        mouse_pos = pygame.mouse.get_pos()
        game.move_player(mouse_pos[1])
        game.move_ball()
        game.draw()

