# 01 sort by Y | 02 Center cam | 03 Box cam

import pygame, sys
from random import randrange

class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('graphics/tree.png').convert_alpha()
        self.rect = self.image.get_rect(topleft= pos)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(center= pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5

    def input(self):
        keys = pygame.key.get_pressed()
        # up, down
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        # right, left 
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed

# 01, 02, 03
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        # 02 # Camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # box setup
        self.camera_borders = {'left':300, 'right':300, 'top':200, 'bottom':200}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l,t,w,h)

        # Ground
        self.ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft= (0,0))

    def center_target_camera(self, target): # 02
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def box_target_camera(self, target):
        # move camera
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']


    def custom_draw(self, player):
        # self.center_target_camera(player) # 02
        self.box_target_camera(player) # 03

        # ground
        ground_offset = self.ground_rect.topleft - self.offset # 02
        self.display_surface.blit(self.ground_surf, ground_offset)

        # cicle for all sprites             and sort by value center Y of each one
        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset # 02
            self.display_surface.blit(sprite.image, offset_pos) 
        
        # pygame.draw.rect(self.display_surface, 'green', self.camera_rect, 3)

# pygame setup ========================================
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720), vsync=1)

# Game setup ==========================================

camera_group = CameraGroup()
player = Player((640,360), camera_group)

# Random trees
for i in range(20):
    random_x = randrange(500,2500,84)
    random_y = randrange(500,2500,84)
    Tree((random_x, random_y), camera_group)

# Game Loop ===========================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw - Update ===================================
    screen.fill('dodgerblue4')
    
    camera_group.update()
    camera_group.custom_draw(player) 

# pygame setup ========================================    
    pygame.display.update()
    clock.tick(60)