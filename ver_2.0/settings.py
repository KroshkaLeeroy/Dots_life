from random import randint


def chance_proc(chance):
    return randint(0, 100) in range(chance + 1)


SCREEN_SIZE = (1280, 720)
