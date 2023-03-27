from settings import random_point, SCREEN_SIZE
from dot import Dot
from food import Food
import pygame

class Main:
    def __init__(self, screen):
        self.screen = screen
        self.dot = Dot(random_point())
        self.foods = []
        self.dots = []

        self.spawn_food(20)
        self.spawn_dot(1)
        self.font = pygame.font.SysFont('arial', 30)
        self.epoch = 0

    def update_all(self):
        for dot in self.dots:
            if dot.hp <= 5:
                self.dots.remove(dot)
                if len(self.dots) <= 1:
                    self.dots.append(Dot(random_point()))
                    self.epoch += 1

        for dot in self.dots:
            dot.update(self.screen)

        for food in self.foods:
            food.update(self.screen)
            for dot in self.dots:
                dot.detect_object(food)
        for dot in self.dots:
            dot_ready = dot.create_child()
            if dot_ready != None:
                self.dots.append(dot_ready)
        self.draw_point_counts()

    def spawn_food(self, count):
        for i in range(count):
            self.foods.append(Food(random_point(), 10))

    def spawn_dot(self, count):
        for i in range(count):
            self.dots.append(Dot(random_point()))

    def draw_point_counts(self):
        epoch_text = self.font.render('Epoch: '+ str(self.epoch), True, (0, 0, 0))
        text = self.font.render('Dot counter: ' + str(len(self.dots)), True, (0, 0, 0))
        self.screen.blit(epoch_text, (10, 10))
        self.screen.blit(text, (SCREEN_SIZE[0] - text.get_width() - 10, 10))
