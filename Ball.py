import const


# Ball is square
class Ball:
    def __init__(self, x, y, length):

        # x and y represent the coordinate of the top left corner of the ball
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.length = length
        self.height = length
        self.width = length

    def is_off_left_side(self):
        if self.x - self.length <= 0:
            return True
        return False

    def is_off_right_side(self):
        if self.x + self.length >= const.WIDTH:
            return True
        return False

    def respawn(self):
        self.x = const.WIDTH//2
        self.y = const.HEIGHT//2
        self.vx = 0
        self.vy = 0

    def move(self):
        self.x += self.vx
        self.y += self.vy
        # past top boundary
        if self.y <= 0:
            self.vy = -self.vy
            self.y = 0
        # past bottom boundary
        elif self.y + self.length >= const.HEIGHT:
            self.vy = -self.vy
            self.y = const.HEIGHT - self.length