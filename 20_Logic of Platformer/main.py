import pygame, sys
from settings import *
from level import Level
from player import Player

# pygame setup ======================================
pygame.init()
screen = pygame.display.set_mode(RES, vsync=1)
clock = pygame.time.Clock()

# Game setup ========================================
background = pygame.image.load('bg_minecraft.jpg').convert()

level = Level()

jumps = 1

JUMP_DELAY = pygame.USEREVENT + 1
pygame.time.set_timer(JUMP_DELAY, 1000)

# Game Loop =========================================
while True:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # events ===================================
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and jumps == 1:
                level.player.jump()
                jumps -= 1
        elif jumps == 0:
            if event.type == JUMP_DELAY:
                jumps = 1
        

    # Draw - Update =================================
    screen.blit(background, (0,0))

    level.run()


# pygame setup ======================================
    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption(f'fps: {clock.get_fps():.0f}          Platformer')