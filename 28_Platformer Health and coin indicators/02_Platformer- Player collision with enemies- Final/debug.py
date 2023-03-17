import pygame.freetype

pygame.init()

def debug(info, y=10, x=10, size=20):
    display_surf = pygame.display.get_surface()
    font = pygame.freetype.SysFont('Verdana', size) # text method 
    font.render_to(display_surf, (x,y), str(info), fgcolor='green', bgcolor='black', style=1)
