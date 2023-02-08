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
# Images
sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')
# Font Text
text_surface = test_font.render('Alien Runner', False, 'Blue')


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
    

    # update everything
    pygame.display.update()
    # frame rate 60 fps
    clock.tick(60)