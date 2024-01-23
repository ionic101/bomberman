class Bomberman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.count_bombs = 0
        self.max_bombs = 1

    def move(self, dx, dy, blocks):
        if (self.x + dx, self.y + dy) not in blocks:
            self.x += dx
            self.y += dy
