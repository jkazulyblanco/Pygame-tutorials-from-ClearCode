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

# suface and color
test_surface = pygame.Surface((10,20))
test_surface.fill('Red')
# Images, .convert() pygame works more faster
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
# Font Text
text_surface = test_font.render('Alien Runner', False, 'Blue')
# snail, .convert_alpha() to use images whit transparency
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_x_pos = 600


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # draw all out elements
    # Images
    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))
    # blit = transferencia de imagenes en bloque, poner una superficie sobre otra
    screen.blit(test_surface,(200,100))
    #text
    screen.blit(text_surface,(300,50))
    # Snail
    snail_x_pos -= 4
    if snail_x_pos <= -72:
        snail_x_pos = 800
    screen.blit(snail_surface,(snail_x_pos,250))

    # update everything
    pygame.display.update()
    
    
    # frame rate 60 fps
    clock.tick(60)