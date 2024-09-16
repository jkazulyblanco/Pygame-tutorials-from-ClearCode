import pygame, sys

# General setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
resolution = screen_width, screen_height = (640, 360)
screen = pygame.display.set_mode(resolution, pygame.SCALED)
game_name = 'PING PONG'


while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Updating the window
    pygame.display.flip()
    clock.tick(60)
    pygame.display.set_caption(f'{game_name}   FPS: {clock.get_fps() :.2f}')
    