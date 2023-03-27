import random


def random_point():
    return random.randint(20, SCREEN_SIZE[0] - 20), random.randint(20, SCREEN_SIZE[1] - 20)


SCREEN_SIZE = (760,1280)
ALL_DIRECTIONS = [(0, 3), (0, -3), (3, 0), (-3, 0), (3, 3), (3, -3), (-3, 3), (-3, -3)]
