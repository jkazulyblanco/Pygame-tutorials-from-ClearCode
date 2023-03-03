import pygame
from pygame.math import Vector2 as vec2

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill('salmon4')
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, x_shift):
        self.rect.x += x_shift 