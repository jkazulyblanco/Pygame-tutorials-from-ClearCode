import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE//2, TILE_SIZE))
        self.image.fill('yellow')
        self.rect = self.image.get_rect(topleft = pos)

# player movement with vector axis x = -1 or 1, y = -1 or 1
# left right jump gravity
        self.direction = pygame.math.Vector2()
        self.speed = 8
        self.gravity = 0.8 # 0.01 # test value
        self.jump_speed = 16 # 1 # test value
        self.collision_sprites = collision_sprites
        self.on_floor = False
        self.double_jump = False
        

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else: # when no pressing any keys
            self.direction.x = 0

    def jump(self):
        if self.on_floor:
            self.direction.y = -self.jump_speed
            self.double_jump = True
            self.on_floor = False
        elif self.double_jump:
            self.direction.y = -self.jump_speed
            self.double_jump = False

    def horizontal_collisions(self):
        for sprite in self.collision_sprites.sprites():
            # if sprite collide with the rect of the player left right
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left


    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():
            # if sprite collide with rect of the player top bottom
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                     # reset to avoid increment of gravity every frame
                    self.direction.y = 0
                    self.on_floor = True

                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    # reset to avoid increment of jump every frame
                    self.direction.y = 0

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        self.input()
        self.rect.x += self.direction.x * self.speed
        self.horizontal_collisions()
        self.apply_gravity()
        self.vertical_collisions()
        