import pygame
from settings import *
from support import import_folder
from random import choice, randint
from tiles import StaticTile

class Sky:
    def __init__(self, horizon, style= 'level'):
        self.top = pygame.image.load('../graphics/decoration/sky/sky_top.png').convert()
        self.bottom = pygame.image.load('../graphics/decoration/sky/sky_bottom.png').convert()
        self.middle = pygame.image.load('../graphics/decoration/sky/sky_middle.png').convert()
        self.horizon = horizon
        # stretch solid color to screen widht
        self.top = pygame.transform.scale(self.top, (screen_width, TILE_HEIGHT))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, TILE_HEIGHT+64))
        self.middle = pygame.transform.scale(self.middle, (screen_width, TILE_HEIGHT))
        # styling
        self.style = style
        if self.style == 'overworld':
            palm_surfaces = import_folder('../graphics/overworld/palms')
            self.palms = []

            for surface in [choice(palm_surfaces) for image in range(10)]:
                x = randint(0, screen_width)
                y = (self.horizon * TILE_WIDTH) + randint(50,100)
                rect = surface.get_rect(midbottom= (x,y))
                self.palms.append((surface, rect))
            
            cloud_surfaces = import_folder('../graphics/overworld/clouds')
            self.clouds = []
            for surface in [choice(cloud_surfaces) for image in range(10)]:
                x = randint(0, screen_width)
                y = randint(0, (self.horizon * TILE_WIDTH) - 100)
                rect = surface.get_rect(midbottom= (x,y))
                self.clouds.append((surface, rect))

    def draw(self, surface):
        for row in range(VERTICAL_TILES):
            y = row * TILE_HEIGHT
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0,y))
            elif row == self.horizon + 1:
                surface.blit(self.bottom, (0, y))
        
        if self.style == 'overworld':
            for palm in self.palms:
                surface.blit(palm[0], palm[1])
            for cloud in self.clouds:
                surface.blit(cloud[0], cloud[1])

class Clouds:
    def __init__(self, horizon, level_width, cloud_number):
        cloud_surf_list = import_folder('../graphics/decoration/clouds')
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile(x, y, cloud)
            self.cloud_sprites.add(sprite)

    def draw(self, surface):
        self.cloud_sprites.draw(surface)

    def update(self, shift):
        self.cloud_sprites.update(shift)
            