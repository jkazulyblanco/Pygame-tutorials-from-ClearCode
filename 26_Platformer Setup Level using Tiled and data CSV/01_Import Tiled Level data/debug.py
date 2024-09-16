import pygame.freetype

pygame.init()

def debug(info, y=10, x=10):
    display_surf = pygame.display.get_surface()
    font = pygame.freetype.SysFont('Verdana', 20) # text method 
    font.render_to(display_surf, (x,y), str(info), fgcolor='green', bgcolor='black', style=1)
