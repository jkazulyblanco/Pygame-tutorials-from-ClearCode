import pygame, sys
from settings import *

# pygame setup ======================================
pygame.init()
screen = pygame.display.set_mode(RES, vsync=1)
clock = pygame.time.Clock()

# Game setup ========================================
background = pygame.image.load('bg_minecraft.jpg').convert()



# Game Loop =========================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # events ===================================

    # Draw - Update =================================
    screen.blit(background, (0,0))

    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption(f'fps: {clock.get_fps():.0f}         Platformer')