import pygame, sys

def bouncing_rect():
    global x_speed, y_speed, other_speed
    moving_rect.x += x_speed
    moving_rect.y += y_speed
    
    # moving the other rectangle
    other_rect.y += other_speed
    # collision other rect with screen borders
    if other_rect.top <= 0 or other_rect.bottom >= screen_height:
        other_speed *= -1

    # collision with screen borders
    if moving_rect.right >= screen_width or moving_rect.left <= 0:
        x_speed *= -1
    if moving_rect.bottom >= screen_height or moving_rect.top <= 0:
        y_speed *= -1

    # collision with other Rect
    collision_tolerance = 10
    if moving_rect.colliderect(other_rect): # if any collision ocurred
        if abs(other_rect.top - moving_rect.bottom) < collision_tolerance and y_speed > 0: # detect top collision and if is moving down
            y_speed *= -1
        if abs(other_rect.bottom - moving_rect.top) < collision_tolerance and y_speed < 0: # detect bottom collision and if is moving up
            y_speed *= -1
        if abs(other_rect.right - moving_rect.left) < collision_tolerance and x_speed < 0: # detect right collision and if is moving left
            x_speed *= -1
        if abs(other_rect.left - moving_rect.right) < collision_tolerance and x_speed > 0: # detect left collision and if is moving right
            x_speed *= -1

    pygame.draw.rect(screen, 'red', moving_rect, 0, 80)
    pygame.draw.rect(screen, 'blue', other_rect)

# General Setup ====================================
pygame.init()
clock = pygame.time.Clock()
window_size = screen_width, screen_height = 600,600
screen = pygame.display.set_mode(window_size, vsync=1)

# Surfaces =========================================
moving_rect = pygame.Rect(150, 150, 50, 50)
x_speed, y_speed = 5, 4

other_rect = pygame.Rect(200, 300, 200, 50)
other_speed = 2

# Game Loop ========================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # key input ================================


    # Logic, Update ================================


    # Draw on Screen ===============================
    screen.fill('darkgreen')
    
    bouncing_rect()

    pygame.display.flip()
    clock.tick(60)
    pygame.display.set_caption(f'fps: {clock.get_fps():.0f}')