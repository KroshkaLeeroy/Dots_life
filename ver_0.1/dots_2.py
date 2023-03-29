from main import *
from settings import *

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Dots_evolution")
clock = pygame.time.Clock()

main = Main(screen)
DEATH_TIME = pygame.USEREVENT
pygame.time.set_timer(DEATH_TIME, 1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == DEATH_TIME:
            for dot in main.dots:
                dot.hp -= 5

    screen.fill((200, 200, 200))

    main.update_all()

    pygame.display.update()
    clock.tick(60)
