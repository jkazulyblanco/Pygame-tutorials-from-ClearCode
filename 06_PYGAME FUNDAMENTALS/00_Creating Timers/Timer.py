''' Logic of timers
the time check every 17 milliseconds = 60 pfs
pygame.init() # starts the timer

if current_time - static_point > length_of_timer:
    any code needed
'''

import pygame, sys

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

# Timer #
current_time = 0
button_press_time = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            button_press_time = pygame.time.get_ticks()
            screen.fill('white')

    current_time = pygame.time.get_ticks()

    if current_time - button_press_time > 2000:
        screen.fill('black')

    print(f'current time: {current_time} buton press time: {button_press_time}')


    pygame.display.flip()
    clock.tick(60)
    pygame.display.set_caption(f'fps: {clock.get_fps() :.2f}')