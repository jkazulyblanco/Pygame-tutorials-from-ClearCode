# 01 # = Setup
# 02 # = Drawing
# 03 # = Animation

# ▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀

# 01 # Imports
import pygame, sys

def ball_animation():   
    # 03 # Movement
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # 03 # Collisions
    # Ball and window
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1
    # ball and paddles
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1


# 01 # General setup
pygame.init()
clock = pygame.time.Clock()

# 01 # Setting up the main window
resolution = screen_width, screen_height = (1280,720)
screen = pygame.display.set_mode(resolution, pygame.SCALED)
game_name = 'PING PONG'

# 02 # Game Rectangles
ball = pygame.Rect(screen_width /2 -15, screen_height /2 -15, 30, 30)
player = pygame.Rect(screen_width -20, screen_height /2 -70, 10, 140)
opponent = pygame.Rect(10, screen_height /2 -70, 10, 140)

# 02 # Colors
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)

# 03 # Speed
ball_speed_x = 7
ball_speed_y = 7

while True:
    # 01 # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ball_animation() # 03 #

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
    