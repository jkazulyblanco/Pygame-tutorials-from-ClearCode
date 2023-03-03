import pygame, sys, time
from settings import *
from level import Level
from debug import debug

# pygame setup ============================================
pygame.init()
screen = pygame.display.set_mode(RES, vsync=1)
clock = pygame.time.Clock()
pygame.display.set_caption(name)



# Game setup =============================================
level = Level(level_map, screen)
on = -1

# Game Loop ==============================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # key events =================================
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                level.player.sprite.jump()
            if event.key == pygame.K_p:
                on *= -1

    screen.fill('deepskyblue2')
    level.run()

    
    debug('press P for Debug', 0, 1100)
    if on == 1:
        debug(f'FPS: {clock.get_fps():.0f}')
        pygame.draw.rect(screen, 'green', level.player.sprite.rect, 2)

    pygame.display.update()
    clock.tick(60)

