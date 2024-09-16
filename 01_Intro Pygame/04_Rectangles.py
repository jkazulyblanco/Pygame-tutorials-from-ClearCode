import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
# window game name
pygame.display.set_caption('Runner')
# limit frame rate
clock = pygame.time.Clock()
# Font
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
#***************************************************

# suface and color
test_surface = pygame.Surface((10,20))
test_surface.fill('Red')
# Images, .convert() pygame works more faster
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Font Text
score_surf = test_font.render('Alien Runner', False, (64, 64, 64))
score_rect = score_surf.get_rect(center= (400,50))

# snail, .convert_alpha() to use images whit transparency
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom= (600,300))
# RECTANGLES, Player
player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom= (80,300))

#*****************************************************
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # pygame.MOUSEBUTTONDOWN -> cuando se mantiene presionado el boton
        # pygame.MOUSEBUTTONUP   -> cuando se deja de presionar el boton
        if event.type == pygame.MOUSEMOTION: # this works when moving the mouse
            if player_rect.collidepoint(event.pos): print('collision')

    # DRAW ALL - OUT ELEMENTS
    # Images
    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))
    # blit = transferencia de imagenes en bloque, poner una superficie sobre otra
    screen.blit(test_surface,(200,10)) # rect red
    # text
    pygame.draw.rect(screen, 'green', score_rect, 10, 20)
    pygame.draw.rect(screen, '#c0e8ec', score_rect, 5) # hexadecimal color
    screen.blit(score_surf,score_rect)
   
    # Snail
    snail_rect.x -= 4
    if snail_rect.right <= 0: snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)

    # Player
    # player_rect.left += 1
    pygame.draw.rect(screen, 'gray', player_rect,3, 20)
    screen.blit(player_surf, player_rect)

    # COLLISION WITH RECTANGLES
    # if player_rect.colliderect(snail_rect): # return 0 or 1, off/on
    #     print('collision')

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     print('collide')
        # show the mouse button pressed
        # print(pygame.mouse.get_pressed())
    # update everything
    pygame.display.update()  
    # frame rate 60 fps
    clock.tick(60)