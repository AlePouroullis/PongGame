# This is a sample Python script.
import pygame, sys, const, random
from Ball import Ball
from Player import Player
from AI import AI
from Point import Point

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pong Game")
        self.screen = pygame.display.set_mode(const.DIMENSIONS)
        self.player = Player()
        self.ai = AI()
        # The order of the constructor parameters is as follows: x, y, length
        # note: ball is square.
        self.ball = Ball(const.WIDTH // 2, const.HEIGHT // 2, 15)
        self.paddle_color = pygame.Color(const.RED)
        self.isStarted = False

        self.font = pygame.font.SysFont("Arial", 32)

    def draw(self):
        self.screen.fill(const.BLACK)
        pygame.draw.rect(self.screen, self.paddle_color, pygame.Rect(self.player.x, self.player.y,
                                                                     const.paddleWidth, const.paddleHeight))
        pygame.draw.rect(self.screen, self.paddle_color, pygame.Rect(self.ai.x, self.ai.y,
                                                                     const.paddleWidth, const.paddleHeight))
        pygame.draw.rect(self.screen, const.GREEN, pygame.Rect(self.ball.x, self.ball.y, self.ball.length, self.ball.length))

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


    def collision(self, rect1, rect2):
        rect1_centre = Point(rect1.x + const.paddleWidth // 2, rect1.y + const.paddleHeight // 2)
        rect2_centre = Point(rect2.x + const.paddleWidth // 2, rect2.y + const.paddleHeight // 2)
        dx = rect1_centre.x - rect2_centre.x
        dy = rect1_centre.y - rect2_centre.y
        width = (rect1.width + rect2.width) / 2
        height = (rect1.height + rect2.height) / 2
        crossWidth = width*dy
        crossHeight = height*dx

        if abs(dx) <= width and abs(dy) <= height:
            if crossWidth > crossHeight:
                return "bottom" if crossWidth > (-crossHeight) else "left"
            else:
                return "right" if crossWidth > (-crossHeight) else "top"

        return "none"

    def check_collision_with_paddles(self):
        collision_with_player = self.collision(self.ball, self.player)
        collision_with_ai = self.collision(self.ball, self.ai)

        if collision_with_player != "none":
            if collision_with_player == "bottom":
                print("bottom of player")
                self.ball.vy = -self.ball.vy
                self.ball.y = self.player.y + self.player.height
            elif collision_with_player == "left":
                print("left of player")
                self.ball.vx = -self.ball.vx
                self.ball.x = self.player.x - self.ball.length
            elif collision_with_player == "right":
                print("right of player")
                self.ball.vx = -self.ball.vx
                self.ball.x = self.player.x + self.player.width
            elif collision_with_player == "top":
                print("top of player")
                self.ball.vy = -self.ball.vy
                self.ball.y = self.player.y - self.ball.length
        elif collision_with_ai != "none":
            if collision_with_ai == "bottom":
                print("bottom of ai")
                self.ball.vy = -self.ball.vy
                self.ball.y = self.ai.y + self.ai.height
            elif collision_with_ai == "left":
                print("left of ai")
                self.ball.vx = -self.ball.vx
                self.ball.x = self.ai.x - self.ball.length
            elif collision_with_ai == "right":
                print("right of ai")
                self.ball.vx = -self.ball.vx
                self.ball.x = self.ai.x + self.ai.width
            elif collision_with_ai == "top":
                print("top of ai")
                self.ball.vy = -self.ball.vy
                self.ball.y = self.ai.y - self.ball.length

    def set_ball_speed(self):
        x_dir_determinant = random.randint(0, 1)
        y_dir_determinant = random.randint(0, 1)
        vx = random.randint(5, 10)
        vy = random.randint(5, 10)
        self.ball.vx = vx if x_dir_determinant == 1 else -vx
        self.ball.vy = vy if y_dir_determinant == 1 else -vy

if __name__ == "__main__":
    game = Game()
    while True:
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not game.isStarted:
            game.isStarted = True
            game.set_ball_speed()

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
