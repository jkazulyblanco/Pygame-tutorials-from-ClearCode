# 01 sort by Y | 02 Center cam | 03 Box cam | 04 keyboard control
# 05 Mouse + Box

import pygame, sys
from random import randrange
from pygame.math import Vector2 as vec2

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

# 01, 02, 03, 04, 05
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        # 02 # Camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # 03 box setup
        self.camera_borders = {'left':200, 'right':200, 'top':100, 'bottom':100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l,t,w,h)

        # 02 Ground
        self.ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft= (0,0))

        # 04 camera speed
        self.keyboard_speed = 5
        self.mouse_speed = 0.5

    def center_target_camera(self, target): # 02
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def box_target_camera(self, target): # 03
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

    def keyboard_control(self): # 04
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.offset.x -= self.keyboard_speed
        if keys[pygame.K_RIGHT]:
            self.offset.x += self.keyboard_speed
        if keys[pygame.K_UP]:
            self.offset.y -= self.keyboard_speed
        if keys[pygame.K_DOWN]:
            self.offset.y += self.keyboard_speed

    def mouse_control(self): # 05
        mouse = vec2(pygame.mouse.get_pos())
        mouse_offset_vector = vec2()
        # borders 
        left_border = self.camera_borders['left']
        top_border = self.camera_borders['top']
        right_border = self.display_surface.get_size()[0] - self.camera_borders['right']
        bottom_border = self.display_surface.get_size()[1] - self.camera_borders['bottom']
        # mouse detection and movement by position
        # if mouse pos is between top and bottom
        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border: # if mouse is on left side
                mouse_offset_vector.x = mouse.x - left_border # get offset
                pygame.mouse.set_pos((left_border, mouse.y)) # update mouse pos
            if mouse.x > right_border: # if mouse is on right side
                mouse_offset_vector.x = mouse.x - right_border # get offset
                pygame.mouse.set_pos((right_border, mouse.y)) # update mouse pos
        
        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - vec2(left_border, top_border)
                pygame.mouse.set_pos((left_border, top_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - vec2(right_border, top_border)
                pygame.mouse.set_pos((right_border, top_border))
        
        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - vec2(left_border, bottom_border)
                pygame.mouse.set_pos((left_border, bottom_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - vec2(right_border, bottom_border)
                pygame.mouse.set_pos((right_border, bottom_border))   
        
        # if mouse pos is between left and right
        if left_border < mouse.x < right_border:
            if mouse.y < top_border: # if mouse is on top side
                mouse_offset_vector.y = mouse.y - top_border # get offset
                pygame.mouse.set_pos((mouse.x, top_border)) # update mouse pos
            if mouse.y > bottom_border: # if mouse is on bottom side
                mouse_offset_vector.y = mouse.y - bottom_border # get offset
                pygame.mouse.set_pos((mouse.x, bottom_border)) # update mouse pos

        self.offset += mouse_offset_vector * self.mouse_speed



    def custom_draw(self, player): # all
        # self.center_target_camera(player) # 02
        # self.box_target_camera(player) # 03
        # self.keyboard_control() # 04
        self.mouse_control() # 05 el mas feo

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
pygame.event.set_grab(True) # the mouse can't leave the window game 

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
        # events # 05
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Draw - Update ===================================
    screen.fill('dodgerblue4')
    
    camera_group.update()
    camera_group.custom_draw(player) 

# pygame setup ========================================    
    pygame.display.update()
    clock.tick(60)