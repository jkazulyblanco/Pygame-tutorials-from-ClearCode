import pygame, sys

# 01 # General setup
pygame.init()
clock = pygame.time.Clock()

# 01 # Setting up the main window
resolution = screen_width, screen_height = (1200,700)
screen = pygame.display.set_mode(resolution, pygame.SCALED)
game_name = 'PING PONG'

# 02 # Game Rectangles
ball = pygame.Rect(screen_width /2 -15, screen_height /2 -15, 30, 30)
player = pygame.Rect(screen_width -20, screen_height /2 -70, 10, 140)
opponent = pygame.Rect(10, screen_height /2 -70, 10, 140)

# 02 # Colors
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)

while True:
    # 01 # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 02 # Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

    # 01 # Updating the window
    pygame.display.flip()
    clock.tick(60)
    pygame.display.set_caption(f'{game_name}   FPS: {clock.get_fps() :.2f}')
    