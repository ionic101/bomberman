from settings import NUM_BLOCKS_HEIGT, NUM_BLOCKS_WIDTH, MAX_BOXES
from random import sample


def generate_walls():
    walls = []
    for x in range(NUM_BLOCKS_WIDTH):
        for y in range(NUM_BLOCKS_HEIGT):
            if x == 0 or y == 0 or x == (NUM_BLOCKS_WIDTH - 1) or y == (NUM_BLOCKS_HEIGT - 1) or (x % 2 == 0 and y % 2 == 0):
                walls.append((x, y))
    return walls


def generate_boxes():
    boxes = [(x, y) for x in range(NUM_BLOCKS_WIDTH) for y in range(NUM_BLOCKS_HEIGT)]
    walls = generate_walls() + [(1, 1), (1, 2), (2, 1), (23, 1), (22, 1), (23, 2), (1, 13), (2, 13), (1, 12), (23, 13), (22, 13), (23, 12)]
    boxes = [i for i in boxes if i not in walls or walls.remove(i)]
    boxes
    return sample(boxes, MAX_BOXES)
