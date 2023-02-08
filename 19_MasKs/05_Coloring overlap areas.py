import pygame, sys

# pygame setup =======================================
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((700,700), vsync=1)

# Game setup =========================================
# background
background = pygame.image.load('graphics/background.jpg').convert()

# ship
ship_surf = pygame.image.load('graphics/ship.png').convert_alpha()
ship_rect = ship_surf.get_rect(center= (300,300))
ship_mask = pygame.mask.from_surface(ship_surf)

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

    # Draw - Update ===================================
    screen.blit(background, (-750, 0))

    screen.blit(obstacle_surf, obstacle_pos)
    screen.blit(ship_surf, ship_rect)
    
    # ship update
    if pygame.mouse.get_pos():
        ship_rect.center = pygame.mouse.get_pos()

    # new mask surface coloring
    offset_x = obstacle_pos[0] - ship_rect.left
    offset_y = obstacle_pos[1] - ship_rect.top
    if ship_mask.overlap(obstacle_mask, (offset_x, offset_y)):
        new_mask = ship_mask.overlap_mask(obstacle_mask, (offset_x, offset_y))
        # coloring the mask   
        new_surf = new_mask.to_surface()
        new_surf.set_colorkey('black')

        surf_w, surf_h = new_surf.get_size()
        for x in range(surf_w):
            for y in range(surf_h):
                if new_surf.get_at((x, y))[0] != 0:
                    new_surf.set_at((x, y), 'cyan')

        screen.blit(new_surf, ship_rect)

    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption(f'{clock.get_fps():.0f}')