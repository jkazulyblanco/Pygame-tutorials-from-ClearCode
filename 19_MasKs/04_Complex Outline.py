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

# MasK to surface
new_obstacle_surf = obstacle_mask.to_surface() # invert color
new_obstacle_surf.set_colorkey('black') # remove color

# filling in the surface with a color
surf_w, surf_h = new_obstacle_surf.get_size()
for x in range(surf_w):
    for y in range(surf_h):
        # get the color white from mask
        if new_obstacle_surf.get_at((x,y))[0] != 0:
            # set the color
            new_obstacle_surf.set_at((x,y), 'darkorange')


# Game Loop ==========================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw - Update
    screen.fill('cyan4')

    # complex way for outline
    offset = 3
    screen.blit(new_obstacle_surf, (obstacle_pos[0] + offset, obstacle_pos[1])) # right
    screen.blit(new_obstacle_surf, (obstacle_pos[0] - offset, obstacle_pos[1])) # left
    screen.blit(new_obstacle_surf, (obstacle_pos[0] ,obstacle_pos[1] - offset)) # top
    screen.blit(new_obstacle_surf, (obstacle_pos[0] ,obstacle_pos[1] + offset)) # bottom

    screen.blit(new_obstacle_surf, (obstacle_pos[0] + offset,obstacle_pos[1] - offset)) # top right
    screen.blit(new_obstacle_surf, (obstacle_pos[0] + offset,obstacle_pos[1] + offset)) # bot tomright
    screen.blit(new_obstacle_surf, (obstacle_pos[0] - offset,obstacle_pos[1] + offset)) # bottom left
    screen.blit(new_obstacle_surf, (obstacle_pos[0] - offset,obstacle_pos[1] - offset)) # bottom ritght
    
    # obstacle
    screen.blit(obstacle_surf, obstacle_pos)



    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption(f'{clock.get_fps():.0f}')