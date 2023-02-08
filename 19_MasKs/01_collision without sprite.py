import pygame, sys

# pygame setup =======================================
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((700,700), vsync=1)

# Game setup =========================================
# player
player_surf = pygame.Surface((50,50))
player_surf.fill('red')
player_rect = player_surf.get_rect(center= (300,300))
player_mask = pygame.mask.from_surface(player_surf)

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
    screen.fill('grey')

    # obstacle
    screen.blit(obstacle_surf, obstacle_pos)
    # border image
    pygame.draw.rect(screen, 'blue', obstacle_surf.get_rect(topleft=obstacle_pos), 2)


    # player
    if pygame.mouse.get_pos():
        player_rect.center = pygame.mouse.get_pos()
    screen.blit(player_surf, player_rect)

    # collision
    offset_x = obstacle_pos[0] - player_rect.left
    ofsset_y = obstacle_pos[1] - player_rect.top
    # if player_mask.overlap(obstacle_mask,(offset_x, ofsset_y)):
    #     print(player_mask.overlap(obstacle_mask,(offset_x, ofsset_y)))

    # Overlap area collision, more than amount of pixels collide
    if player_mask.overlap_area(obstacle_mask,(offset_x, ofsset_y)) >= 100:
        player_surf.fill('green')
    else:
        player_surf.fill('red')

    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption(f'{clock.get_fps():.0f}')