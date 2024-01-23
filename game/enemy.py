from random import shuffle


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, blocks, explosions, player_cords):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        shuffle(directions)
        for d in directions:
            dx, dy = d
            if ((self.x + dx, self.y + dy) not in blocks) and ((self.x, self.y) not in explosions):
                self.x += dx
                self.y += dy
                break

        if (self.x, self.y) == player_cords:
            return True
        else:
            return False
