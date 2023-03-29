import random

import pygame
import sys
from settings import SCREEN_SIZE
from colors import *
from objects import Dot, Food
from random import randint, choice


class Main:
    def __init__(self, food_count=1, dot_count=1):
        self.dot_count = dot_count
        self.food_count = food_count
        self.width, self.height = SCREEN_SIZE
        self.wall_gap = 30
        self.dots_colors = [(randint(0, 255), randint(0, 255), randint(0, 255),) for _ in range(dot_count)]

        self.include_dots_view = False
        self.restart = False
        self.pause = False

        self.epoch = 1

        self.dots_view_button = pygame.Rect(self.width / 2 - 40, 10, 170, 40)
        self.restart_button = pygame.Rect(self.dots_view_button.x + self.dots_view_button.width + 10, 10, 70, 40)
        self.pause_button = pygame.Rect(self.restart_button.x + self.restart_button.width + 10, 10, 60, 40)

        self.font = pygame.sysfont.SysFont('arial', 20)
        self.start_board = pygame.Rect(0, 0, self.width, 70)

        self.foods = self.create_food()
        self.dots = self.create_dots()

    def update(self, display):
        if not self.pause:
            for dot in self.dots:
                dot.update(self.dots, self.foods)
                child = dot.make_child()
                if child is not None:
                    self.dots.append(child)
                if dot.seed['size'] >= 50:
                    self.dots.append(dot.make_child_100())

        self.draw_all(display)

    def create_food(self):
        return [Food(5, GREEN, self.start_board.height) for _ in range(self.food_count)]

    def create_dots(self):
        return [
            Dot(randint(self.wall_gap, self.width - self.wall_gap),
                randint(self.start_board.height + self.wall_gap, self.height - self.wall_gap),
                self.start_board.height,
                color=color) for
            color in
            self.dots_colors]

    def create_dot(self, x, y):
        self.dots.append(Dot(x, y, self.start_board.height, color=choice(self.dots_colors)))

    def death(self):
        if len(self.dots) > 100:
            self.dots.clear()
        for dot in self.dots:
            if dot.death():
                self.dots.remove(dot)
        if len(self.dots) <= 1:
            self.dots_colors = [(randint(0, 255), randint(0, 255), randint(0, 255),) for _ in
                                range(self.dot_count)]
            self.dots = self.create_dots()
            self.epoch += 1

    def switch_dots_view(self):
        self.include_dots_view = not self.include_dots_view

    def switch_pause(self):
        self.pause = not self.pause

    def restart_logic(self):
        self.restart = not self.restart
        self.epoch = 1
        self.dots_colors = [(randint(0, 255), randint(0, 255), randint(0, 255),) for _ in range(self.dot_count)]
        self.foods.clear()
        self.foods = self.create_food()
        self.dots.clear()
        self.dots = self.create_dots()

    def draw_all(self, display):
        for dot in self.dots:
            dot.draw(display, dot_eyes=self.include_dots_view)
        for food in self.foods:
            food.draw(display)
        self.draw_star_board()
        self.draw_board_dots()
        self.draw_view_button()
        self.draw_restart_button()
        self.draw_pause_button()
        self.draw_dots_count()
        self.draw_epoch()

    def spawn_food(self, x, y):
        food = choice(self.foods)
        food.respawn(x, y)

    def draw_board_dots(self):
        for count, color in enumerate(self.dots_colors, 1):
            pygame.draw.circle(screen, color, (count * 25, 25), 10)
            for dot in self.dots:
                if dot.seed['color'] == color:
                    pygame.draw.circle(screen, RED, (count * 25, 25), 5)

    def draw_dots_count(self):
        text = self.font.render('All dots counter: ' + str(len(self.dots)), True, BLACK)
        screen.blit(text, (self.width - text.get_width() - 10, 10))

    def draw_epoch(self):
        text = self.font.render('Epoch: ' + str(self.epoch), True, BLACK)
        screen.blit(text, (self.width - text.get_width() - 10, 35))

    def draw_star_board(self):
        pygame.draw.rect(screen, GRAY, self.start_board)

    def draw_view_button(self):
        if self.include_dots_view:
            pygame.draw.rect(screen, RED, self.dots_view_button)
            text = 'Dots eyes info ON'
        else:
            pygame.draw.rect(screen, WHITE, self.dots_view_button)
            text = 'Dots eyes info OFF'
        text = self.font.render(text, True, BLACK)
        screen.blit(text, (
            self.dots_view_button.centerx - text.get_width() / 2,
            self.dots_view_button.centery - text.get_height() / 2))

    def draw_restart_button(self):
        if self.restart:
            pygame.draw.rect(screen, RED, self.restart_button)
            self.restart = False
        else:
            pygame.draw.rect(screen, WHITE, self.restart_button)
        text = 'Restart'
        text = self.font.render(text, True, BLACK)
        screen.blit(text, (
            self.restart_button.centerx - text.get_width() / 2,
            self.restart_button.centery - text.get_height() / 2))

    def draw_pause_button(self):
        if self.pause:
            pygame.draw.rect(screen, RED, self.pause_button)
        else:
            pygame.draw.rect(screen, WHITE, self.pause_button)
        text = 'Pause'
        text = self.font.render(text, True, BLACK)
        screen.blit(text, (
            self.pause_button.centerx - text.get_width() / 2,
            self.pause_button.centery - text.get_height() / 2))


pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("dots_live")
clock = pygame.time.Clock()

main = Main(dot_count=6, food_count=25)

DEATH_TIMER = pygame.USEREVENT
pygame.time.set_timer(DEATH_TIMER, 1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if main.dots_view_button.collidepoint(event.pos):
                    main.switch_dots_view()
                if main.restart_button.collidepoint(event.pos):
                    main.restart_logic()
                if event.pos[0] in range(SCREEN_SIZE[0]) and event.pos[1] in range(main.start_board.height,
                                                                                   SCREEN_SIZE[1]):
                    main.create_dot(event.pos[0], event.pos[1])
                if main.pause_button.collidepoint(event.pos):
                    main.switch_pause()
            if event.button == 3:
                main.spawn_food(event.pos[0], event.pos[1])
        if event.type == DEATH_TIMER:
            if not main.pause:
                main.death()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        #     if event.key == pygame.K_DOWN:
        #         for dot in main.dots:
        #             dot.direction.y += dot.seed['speed']
        #     if event.key == pygame.K_UP:
        #         for dot in main.dots:
        #             dot.direction.y -= dot.seed['speed']
        #     if event.key == pygame.K_RIGHT:
        #         for dot in main.dots:
        #             dot.direction.x += dot.seed['speed']
        #     if event.key == pygame.K_LEFT:
        #         for dot in main.dots:
        #             dot.direction.x -= dot.seed['speed']
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_DOWN:
        #         for dot in main.dots:
        #             dot.direction.y = 0
        #     if event.key == pygame.K_UP:
        #         for dot in main.dots:
        #             dot.direction.y = 0
        #     if event.key == pygame.K_RIGHT:
        #         for dot in main.dots:
        #             dot.direction.x = 0
        #     if event.key == pygame.K_LEFT:
        #         for dot in main.dots:
        #             dot.direction.x = 0

    screen.fill(LIGHT_GRAY)

    main.update(screen)

    pygame.display.flip()
    clock.tick(60)
