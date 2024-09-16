# from support import import_folder
import pygame
from settings import *
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self, x, y, path, animspeed=0.15, tilewidth= TILE_WIDTH, tileheight= TILE_HEIGHT):
        super().__init__(x, y, path, animspeed, tilewidth, tileheight)
        self.speed = randint(2,4)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1 

    def update(self, shift):
        # inherited class call updates
        self.rect.x += shift
        self.animate()
        # new
        self.move()
        self.reverse_image()
