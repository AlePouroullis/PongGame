import const


class AI:
    def __init__(self):
        self.speed = const.AI_SPEED
        self.x = const.WIDTH - const.DIST_FROM_WALL - const.paddleWidth
        self.y = const.HEIGHT // 2 - const.paddleHeight // 2
        self.score = 0

    def reset(self):
        self.y = const.HEIGHT // 2 - const.paddleHeight // 2

    def move(self, y):
        if y > const.HEIGHT - const.paddleHeight:
            self.y = const.HEIGHT - const.paddleHeight
        elif y < 0:
            self.y = 0
        else:
            self.y = y

    def increment_score(self):
        self.score += 1

