import pygame, sys
from pytmx.util_pygame import load_pygame
from pygame import freetype

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720), vsync=1)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft= pos)

# Surfaces ==============================================
tmx_data = load_pygame('../data/tmx/basic.tmx')
sprite_group = pygame.sprite.Group()

# cycle through all layers
for layer in tmx_data.visible_layers:
    # if layer.name in ('Floor', 'Plants and Rock', 'Pipes', 'Ground'): # manual way
    if hasattr(layer, 'data'):
        for x, y, surf in layer.tiles():
            pos = (x*128, y*128)
            Tile(pos= pos, surf= surf, groups= sprite_group)

# cycle through all objects
for obj in tmx_data.objects:
    pos = obj.x, obj.y
    if obj.Type in ('Building', 'Vegetation'):
        Tile(pos= pos, surf= obj.image, groups= sprite_group)
        # print(obj.Type)

# Game Loop =============================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Draw - Update =====================================
    screen.fill('black')
    sprite_group.draw(screen)

    for obj in tmx_data.objects:
        pos = obj.x, obj.y
        if obj.Type in 'Shapes':
            
            if obj.name == 'Marker':
                pygame.draw.circle(screen, 'red', (obj.x, obj.y), 5)
            
            if obj.name == 'Rectangle':
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                pygame.draw.rect(screen, 'blue', rect)

            if obj.name == 'Ellipse':
                rect_ellipse = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                pygame.draw.ellipse(screen, 'red4', rect_ellipse)

            if obj.name == 'Polygon':
                points = [(point.x, point.y) for point in obj.points]
                pygame.draw.polygon(screen, 'darkgrey', points)

            # if obj.name == 'Texto':
                # font = pygame.freetype.SysFont('Verdana', obj.) # text method 
                # font.render_to(screen, (obj.x, obj.y), str(obj.Text), fgcolor='white', bgcolor=None, style=1, rotation=0, size=0)
                # print(obj.)

    pygame.display.update()
    clock.tick(60)