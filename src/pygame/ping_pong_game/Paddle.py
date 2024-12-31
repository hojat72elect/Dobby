class Paddle:
    def __init__(self, x, y, width, height, score):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.score = score


    def move_up(self):
        self.y -= 5

    def move_down(self):
        self.y += 5