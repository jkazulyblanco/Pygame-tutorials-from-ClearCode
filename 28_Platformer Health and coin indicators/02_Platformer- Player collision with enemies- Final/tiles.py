# for using in level to create sprite

import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tilewidth=TILE_WIDTH, tileheight=TILE_HEIGHT):
        super().__init__()
        self.tilewidth = tilewidth
        self.tileheight = tileheight
        self.image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.rect = self.image.get_rect(topleft= (x, y))

    # movement of tiles simulated screen left or right
    def update(self, shift):
            self.rect.x += shift

class StaticTile(Tile):
    def __init__(self, x, y, surface, tilewidth=TILE_WIDTH, tileheight=TILE_HEIGHT):
        super().__init__(x, y, tilewidth, tileheight)
        self.image = surface

class AnimatedTile(Tile):
    def __init__(self, x, y, path, animspeed=0.15, coin_val=0, tilewidth=TILE_WIDTH, tileheight=TILE_HEIGHT):
        super().__init__(x, y, tilewidth, tileheight)
        self.frames = path
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.anim_speed = animspeed
        self.coin_val = coin_val

    def animate(self):
        self.frame_index += self.anim_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self, shift):
        self.animate()
        self.rect.x += shift
