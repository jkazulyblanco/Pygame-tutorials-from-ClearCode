import pygame, sys
from debug import debug

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600,600), vsync=1)

cat_surf = pygame.image.load('cat.png').convert_alpha()
cat_surf = pygame.transform.scale(cat_surf, (459,500))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill('red4')
    screen.blit(cat_surf, (80,70))
    
    # Debug == info, y, x
    debug(pygame.mouse.get_pos())
    debug(pygame.mouse.get_pressed(), 40)
    debug(pygame.mouse.get_pos(), pygame.mouse.get_pos()[1],pygame.mouse.get_pos()[0])

    pygame.display.update()
    clock.tick(60)