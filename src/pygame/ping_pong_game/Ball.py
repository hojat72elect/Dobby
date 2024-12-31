class Ball:
    def __init__(self, x: float, y: float, speed_x: float, speed_y: float, radius: float):
        self.x: float = x
        self.y: float = y
        self.speed_x: float = speed_x
        self.speed_y: float = speed_y
        self.radius: float = radius

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def bounce_y(self):
        self.speed_y *= -1

    def bounce_x(self):
        self.speed_x *= -1

    def reset(self, x: float, y: float):
        self.x = x
        self.y = y
