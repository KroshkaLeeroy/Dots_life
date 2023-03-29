import pygame
import random
from settings import SCREEN_SIZE


class Food:
    def __init__(self, pos, size):
        self.x = pos[0]
        self.y = pos[1]
        self.size = size
        self.type = 'food'
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.color = (0, 255, 0)

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

    def respawn(self):
        x = random.randint(20, SCREEN_SIZE[0] - 20)
        y = random.randint(20, SCREEN_SIZE[1] - 20)
        self.rect.center = (x, y)

    def update(self, screen):
        self.draw(screen)
