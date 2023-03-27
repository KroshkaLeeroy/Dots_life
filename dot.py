import math
import pygame
import random
from settings import SCREEN_SIZE, ALL_DIRECTIONS


class Dot:
    def __init__(self, pos, seed=None):
        if seed is None:
            seed = {'size': random.randint(20, 30), }
            seed.update({'color': [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
                         'speed': 3,
                         'hp': seed.get('size') * 5,
                         'radius': seed.get('size') * random.randint(1, 3), })

        self.seed = seed
        self.size = seed['size']
        self.color = seed['color']
        self.speed = seed['speed']
        self.hp = seed['hp']
        self.radius = seed['radius']
        self.type = 'dot'

        self.set_mutations()
        self.rect = pygame.Rect(pos[0], pos[1], self.size, self.size)
        self.direction = pygame.Vector2(random.choice(ALL_DIRECTIONS))
        self.font = pygame.font.SysFont('arial', 15)

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
        text = self.font.render(str(self.hp), True, (0, 0, 0))
        screen.blit(text, (self.rect.centerx - text.get_width() / 2 + 1, self.rect.centery - text.get_height() / 2))
        pygame.draw.ellipse(screen, (255, 0, 0), self.rect.inflate(self.radius, self.radius), 1)

    def set_mutations(self):
        r_color = random.randint(5, 10)
        g_color = random.randint(5, 10)
        b_color = random.randint(5, 10)

        if self.get_random():
            for key, item in self.seed.items():
                if self.get_random():
                    if self.get_random():
                        if key == 'color':
                            if self.seed[key][0] + r_color > 255:
                                self.seed[key][0] = 255 - self.seed[key][0]
                            else:
                                self.seed[key][0] = self.seed[key][0] + r_color
                            if self.seed[key][1] + r_color > 255:
                                self.seed[key][1] = 255 - self.seed[key][1]
                            else:
                                self.seed[key][1] = self.seed[key][1] + g_color
                            if self.seed[key][2] + r_color > 255:
                                self.seed[key][2] = 255 - self.seed[key][2]
                            else:
                                self.seed[key][2] = self.seed[key][2] + b_color
                        else:
                            self.seed[key] = self.seed[key] + random.randint(1, 3) / 2
                    else:
                        if key == 'color':
                            if self.seed[key][0] - r_color < 0:
                                self.seed[key][0] = 255 - self.seed[key][0]
                            else:
                                self.seed[key][0] = self.seed[key][0] - r_color
                            if self.seed[key][1] - r_color < 0:
                                self.seed[key][1] = 255 - self.seed[key][1]
                            else:
                                self.seed[key][1] = self.seed[key][1] - g_color
                            if self.seed[key][2] - r_color < 0:
                                self.seed[key][2] = 255 - self.seed[key][2]
                            else:
                                self.seed[key][2] = self.seed[key][2] - b_color
                        else:
                            self.seed[key] = self.seed[key] - random.randint(1, 3) / 2

    def respawn(self):
        x = random.randint(0, SCREEN_SIZE[0])
        y = random.randint(0, SCREEN_SIZE[1])
        self.rect.center = (x, y)
        self.direction = pygame.Vector2(random.choice(ALL_DIRECTIONS))

    def update(self, screen):
        self.change_size()
        self.move()
        self.collision_to_walls(True)
        self.draw(screen)

    def change_size(self):
        self.rect.size = (self.hp / 5, self.hp / 5)

    def detect_object(self, unit):
        if unit.type == 'food':
            distance = round(
                math.sqrt(
                    (self.rect.centerx - unit.rect.centerx) ** 2 + (
                            self.rect.centery - unit.rect.centery) ** 2),
                1)
            if distance <= self.radius - 5:
                self.move_to_object(unit)
            if distance <= self.size:
                self.eat_food()
                unit.respawn()

    def eat_food(self):
        self.hp += 20

    def create_child(self):
        if self.hp >= 210:
            self.points = 0
            self.hp -= 100

            return Dot((self.rect.centerx, self.rect.y), self.seed)

    def move_to_object(self, unit):
        vector_x = unit.rect.centerx - self.rect.centerx
        vector_y = unit.rect.centery - self.rect.centery
        if vector_x >= 0:
            self.direction.x = 3
        if vector_x <= 0:
            self.direction.x = -3
        if vector_y >= 0:
            self.direction.y = 3
        if vector_y <= 0:
            self.direction.y = -3

    def move(self):
        self.randomise_speed()
        self.slow_down_speed()

        self.rect.center += self.direction

    def randomise_speed(self):
        if self.get_random():
            self.direction.xy += random.random(), random.random()
        if self.get_random():
            self.direction.xy -= random.random(), random.random()

    def get_random(self):
        if random.randint(0, 20) in range(1, 3):
            return True
        return False

    def slow_down_speed(self):
        if self.direction.x > self.speed:
            self.direction.x = self.speed
        if self.direction.y > self.speed:
            self.direction.y = self.speed
        if self.direction.x < -self.speed:
            self.direction.x = -self.speed
        if self.direction.y < -self.speed:
            self.direction.y = -self.speed

    def teleport(self, position):
        self.rect.center = position

    def collision_to_walls(self, no_clip=False):
        if no_clip:
            if self.rect.left <= 0:
                self.rect.left = 0
                self.direction.xy = (self.direction.x * -1, self.direction.y * -1)
            if self.rect.right >= SCREEN_SIZE[0]:
                self.rect.right = SCREEN_SIZE[0]
                self.direction.xy = (self.direction.x * -1, self.direction.y * -1)
            if self.rect.top <= 0:
                self.rect.top = 0
                self.direction.xy = (self.direction.x * -1, self.direction.y * -1)
            if self.rect.bottom >= SCREEN_SIZE[1]:
                self.rect.bottom = SCREEN_SIZE[1]
                self.direction.xy = (self.direction.x * -1, self.direction.y * -1)
        else:
            if self.rect.x < 0:
                self.teleport((SCREEN_SIZE[0] - self.size, self.rect.y))
            if self.rect.x > SCREEN_SIZE[0]:
                self.teleport((0 + self.size, self.rect.y))
            if self.rect.y < 0:
                self.teleport((self.rect.x, SCREEN_SIZE[1] - self.size))
            if self.rect.y > SCREEN_SIZE[1]:
                self.teleport((self.rect.x, 0 + self.size))
