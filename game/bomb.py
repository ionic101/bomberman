from settings import BOMB_RADIUS


class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def explode(self, blocks):
        cords = [(self.x, self.y)]

        for x in range(1, BOMB_RADIUS + 1):
            cord = (self.x + x, self.y)
            if cord not in blocks:
                cords.append(cord)
            else:
                break

        for x in range(1, BOMB_RADIUS + 1):
            cord = (self.x - x, self.y)
            if cord not in blocks:
                cords.append(cord)
            else:
                break

        for y in range(1, BOMB_RADIUS + 1):
            cord = (self.x, self.y + y)
            if cord not in blocks:
                cords.append(cord)
            else:
                break

        for y in range(1, BOMB_RADIUS + 1):
            cord = (self.x, self.y - y)
            if cord not in blocks:
                cords.append(cord)
            else:
                break

        return cords
