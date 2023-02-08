import pygame

pygame.init() # to use the font
font = pygame.font.Font(None, 20)

def debug(info, y=10, x=10):
    display_surf = pygame.display.get_surface()
    
    # create text
    debug_surf = font.render(str(info), True, 'green')
    # rect
    debug_rect = debug_surf.get_rect(topleft=(x,y))
    pygame.draw.rect(display_surf, 'black', debug_rect)
    # draw
    display_surf.blit(debug_surf, debug_rect)