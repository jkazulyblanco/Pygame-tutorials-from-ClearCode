import pygame, sys, time
from debug import debug

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720), vsync=1)

# Game setup ===========================================
test_rect = pygame.Rect(0,300, 100,100)
test_rect_pos = test_rect.x # for precision
test_speed = 200

# current time
previous_time = time.time() # for precision 

# game loop =========================================
while True:
    # dt = clock.tick(60) / 1000 # return miliseconds 0.017 = 60
    
    dt = time.time() - previous_time # for precision
    previous_time = time.time() # for precision

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Draw - Update ===================================
    screen.fill('gray15')

    pygame.draw.rect(screen, 'red', test_rect)
    
    test_rect_pos += test_speed * dt # for precision
    test_rect.x = round(test_rect_pos) # for precision

    
    # debug message
    debug(f'milisecons: {dt}')
    debug(f'FPS :{clock.get_fps():.0f}', 70)

    pygame.display.update()
    clock.tick(60)
    