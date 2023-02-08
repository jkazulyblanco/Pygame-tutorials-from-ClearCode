import pygame, sys

# General Setup
pygame.init()
clock = pygame.time.Clock()

# Create Surfaces
screen = pygame.display.set_mode((600,600)) # main window
second_surface = pygame.Surface([100,200]) # astatic surface
second_surface.fill('darkorange') # static surface color
image = pygame.image.load('target.png') # image
image_rect = image.get_rect(topleft= [90,50])



# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw Surfaces
    screen.fill('darkblue')
    screen.blit(second_surface, (0,50))
    screen.blit(image, image_rect)
    pygame.draw.rect(screen, 'yellow', image_rect, 4, 70) # visible rect

    
    pygame.display.flip() # exec Draw all things inside of loop
    clock.tick(60)