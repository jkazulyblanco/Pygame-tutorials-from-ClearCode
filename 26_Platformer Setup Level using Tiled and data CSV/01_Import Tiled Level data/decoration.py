import pygame
from settings import *
from support import import_folder
from random import choice, randint
from tiles import StaticTile

class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load('../graphics/decoration/sky/sky_top.png').convert()
        self.bottom = pygame.image.load('../graphics/decoration/sky/sky_bottom.png').convert()
        self.middle = pygame.image.load('../graphics/decoration/sky/sky_middle.png').convert()
        self.horizon = horizon

        # stretch solid color to screen widht
        self.top = pygame.transform.scale(self.top, (screen_width, TILE_HEIGHT))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, TILE_HEIGHT+64))
        self.middle = pygame.transform.scale(self.middle, (screen_width, TILE_HEIGHT))

    def draw(self, surface):
        for row in range(VERTICAL_TILES):
            y = row * TILE_HEIGHT
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0,y))
            elif row == self.horizon + 1:
                surface.blit(self.bottom, (0, y))

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
            