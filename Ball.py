import const


class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = radius

    def is_off_left_side(self):
        if self.x - self.radius <= 0:
            return True
        return False

    def is_off_right_side(self):
        if self.x + self.radius >= const.WIDTH:
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
        if self.y - self.radius <= 0 or self.y + self.radius >= const.HEIGHT:
            self.vy = -self.vy