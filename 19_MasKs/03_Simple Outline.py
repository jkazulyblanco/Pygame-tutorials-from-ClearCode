import pygame, sys

# pygame setup =======================================
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((700,700), vsync=1)

# Game setup =========================================
# player


# obstacle
obstacle_surf = pygame.image.load('graphics/alpha.png').convert_alpha()
obstacle_pos = (50,50)
obstacle_mask = pygame.mask.from_surface(obstacle_surf)


# Game Loop ==========================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw - Update
    screen.fill('cyan4')

    # obstacle
    screen.blit(obstacle_surf, obstacle_pos)
   
    # siple way to create an obstacle from mask ==========
    for point in obstacle_mask.outline():
        x = point[0] + obstacle_pos[0]
        y = point[1] + obstacle_pos[1]
        pygame.draw.circle(screen, 'red', (x,y), 1)

    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption(f'{clock.get_fps():.0f}')