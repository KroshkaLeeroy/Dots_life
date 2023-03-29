import math
from time import time
import pygame
from random import randint, choice, random, triangular
from settings import SCREEN_SIZE, chance_proc
from colors import RED, BLACK


class Dot:
    def __init__(self, x, y, gap, start_seed=None, color=None):
        self.gap = gap
        self.type = 'dot'
        if start_seed is None:
            start_seed = str({'size': randint(10, 20),
                              'speed': triangular(1, 2),
                              'radius': randint(10, 40),
                              'mutation_chance': randint(10, 30),
                              'split_chance': randint(0, 100),
                              'time_split_try': randint(5, 10),
                              'color': color})

        self.seed = eval(start_seed)
        self.last_time_try_split = 0
        self.font = pygame.font.SysFont('arial', 13)
        self.rect = pygame.Rect(x, y, self.seed['size'], self.seed['size'])

        self.direction = pygame.Vector2(choice([self.seed['speed'], -self.seed['speed'], 0]),
                                        choice([self.seed['speed'], -self.seed['speed'], 0]))

        self.mutation = self.seed_mutation(start_seed)

    def draw(self, screen, dot_eyes):
        if self.seed['speed'] == 0:
            pygame.draw.circle(screen, BLACK, self.rect.center, self.seed['size'])
        else:
            pygame.draw.circle(screen, self.seed['color'], self.rect.center, self.seed['size'])
            pygame.draw.circle(screen, BLACK, self.rect.center, self.seed['size'], 1)
        if dot_eyes:
            pygame.draw.circle(screen, RED, self.rect.center, self.seed['size'] + self.seed['radius'], 1)
            if self.seed['size'] > 7:
                text = self.font.render(str(self.seed['size']), True, BLACK)
                screen.blit(text, (self.rect.centerx - text.get_width() / 2, self.rect.centery - text.get_height() / 2))

    def update(self, dots, foods, ):
        self.move(dots, foods)

    def seed_mutation(self, seed):
        seed = eval(seed)
        if chance_proc(self.seed['mutation_chance']):
            seed['time_split_try'] = choice([-2, 2])
        if chance_proc(self.seed['mutation_chance']):
            seed['split_chance'] = choice([-5, 5])
        if chance_proc(self.seed['mutation_chance']):
            seed['size'] = choice([-5, 5])
        if chance_proc(self.seed['mutation_chance']):
            seed['radius'] = choice([-5, 5])
        if chance_proc(self.seed['mutation_chance']):
            seed['speed'] += triangular(choice([random(), -random()]), choice([random(), -random()]))
        if chance_proc(self.seed['mutation_chance']):
            seed['mutation_chance'] += choice([-2, 2])
        return str(seed)

    def move(self, dots, foods):
        self.randomise_speed()

        self.enumeration_of_objects(foods)
        self.enumeration_of_objects(dots)

        self.speed_limit()
        self.collision()
        self.rect.move_ip(self.direction)

    def enumeration_of_objects(self, objects):
        for object in objects:
            if self.check_distanse(object) < self.seed['size'] + self.seed['radius']:
                kill = self.go_to_or_out(object)
                if kill:
                    objects.remove(object)

    def go_to_or_out(self, object):
        if object.type == 'food':
            self.move_to_or_out_object(object, True)
            if self.rect.colliderect(object.rect):
                object.respawn()
                self.seed['size'] += object.seed['size']
                self.rect.size = (self.seed['size'], self.seed['size'])
        if object.type == 'dot':
            if object != self and object.seed['color'] != self.seed['color']:
                if object.seed['size'] < self.seed['size']:
                    self.move_to_or_out_object(object, True)
                    if self.rect.colliderect(object.rect):
                        self.seed['size'] += object.seed['size'] // 2
                        self.rect.size = (self.seed['size'], self.seed['size'])
                        return True
                else:
                    self.move_to_or_out_object(object, False)

    def move_to_or_out_object(self, object, in_):
        vector_x = object.rect.centerx - self.rect.centerx
        vector_y = object.rect.centery - self.rect.centery
        if in_:
            if vector_x >= 0:
                self.direction.x = self.seed['speed']
            else:
                self.direction.x = -self.seed['speed']
            if vector_y >= 0:
                self.direction.y = self.seed['speed']
            else:
                self.direction.y = -self.seed['speed']
        else:
            if vector_x >= 0:
                self.direction.x = -self.seed['speed']
            else:
                self.direction.x = self.seed['speed']
            if vector_y >= 0:
                self.direction.y = -self.seed['speed']
            else:
                self.direction.y = self.seed['speed']

    def check_distanse(self, object):
        return round(math.sqrt(
            ((self.rect.centerx) - (object.rect.centerx)) ** 2 +
            ((self.rect.centery) - (object.rect.centery)) ** 2))

    def collision(self):
        if self.rect.left <= 10:
            self.rect.left = 10
            self.direction.x *= -1
        if self.rect.right >= SCREEN_SIZE[0] - 10:
            self.rect.right = SCREEN_SIZE[0] - 10
            self.direction.x *= -1
        if self.rect.top <= self.gap + 10:
            self.rect.top = self.gap + 10
            self.direction.y *= -1
        if self.rect.bottom >= SCREEN_SIZE[1] - 10:
            self.rect.bottom = SCREEN_SIZE[1] - 10
            self.direction.y *= -1

    def randomise_speed(self):
        if chance_proc(10):
            self.direction.xy += choice([random(), -random(), ]), choice([random(), -random()])

    def speed_limit(self):
        if self.direction.x > self.seed['speed']:
            self.direction.x = self.seed['speed']
        if self.direction.x < -self.seed['speed']:
            self.direction.x = -self.seed['speed']
        if self.direction.y > self.seed['speed']:
            self.direction.y = self.seed['speed']
        if self.direction.y < -self.seed['speed']:
            self.direction.y = -self.seed['speed']

    def make_child(self):
        if self.seed['size'] >= 30:
            time_to_split = time() - self.last_time_try_split
            if time_to_split > self.seed['time_split_try']:

                self.last_time_try_split = time()
                chance = randint(0, 100)

                if chance in range(self.seed['split_chance'] + 1):
                    mutation = self.seed_mutation(str(self.seed))
                    self.seed['size'] //= 2
                    return Dot(self.rect.centerx, self.rect.centery, self.gap, start_seed=mutation)

    def make_child_100(self):
        self.seed['size'] //= 2
        mutation = self.seed_mutation(str(self.seed))
        return Dot(self.rect.centerx, self.rect.centery, self.gap, start_seed=mutation)

    def death(self):
        self.seed['size'] -= 1
        if self.seed['size'] == 3:
            return True
        return False


class Food:
    def __init__(self, size, color, gap):
        self.gap = gap
        self.size = size
        self.color = color
        self.type = 'food'
        self.seed = {'size': 5, 'radius': size}

        x = randint(20, SCREEN_SIZE[0] - 20)
        y = randint(self.gap + 20, SCREEN_SIZE[1] - 20)

        self.rect = pygame.Rect(x, y, size, size)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.size)

    def respawn(self, x=None, y=None):
        if x is None:
            x = randint(20, SCREEN_SIZE[0] - 20)
        if y is None:
            y = randint(self.gap + 20, SCREEN_SIZE[1] - 20)
        self.rect.center = (x, y)
