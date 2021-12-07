class Distance:
    def __init__(self, x1, y1, x2, y2):
        self.x = abs(x1 - x2)
        self.y = abs(y1 - y2)