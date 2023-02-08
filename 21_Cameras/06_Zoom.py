# 01 sort by Y | 02 Center cam | 03 Box cam | 04 keyboard control
# 05 Mouse + Box | 06 Zoom

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

# 01, 02, 03, 04, 05, 06
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
        self.mouse_speed = 0.3 # 05

        # 06
        self.zoom_scale = 1
        self.internal_surf_size = (2500,2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA) # make transparent
        self.internal_rect = self.internal_surf.get_rect(center= (self.half_w, self.half_h)) 
        self.internal_surf_size_vector = vec2(self.internal_surf_size) 
        self.internal_offset = vec2()
        self.internal_offset.x = self.internal_surf_size[0] //2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] //2 - self.half_h

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

    def zoom_keyboard_control(self): # 06
        keys = pygame.key.get_pressed()
        if self.zoom_scale < 1.5:
            if keys[pygame.K_q]:
                self.zoom_scale += 0.005
        if 0.7 < self.zoom_scale < 2:
            if keys[pygame.K_e]:
                self.zoom_scale -= 0.005
        # print(self.zoom_scale)

    def custom_draw(self, player): # all
        # self.center_target_camera(player) # 02
        # self.box_target_camera(player) # 03
        # self.keyboard_control() # 04
        self.mouse_control() # 05 el mas feo
        self.zoom_keyboard_control()
        
        self.internal_surf.fill('dodgerblue4') # 06 the same color!

        # ground
        ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset # 02, 06
        self.internal_surf.blit(self.ground_surf, ground_offset) # 02, 06

        # cicle for all sprites             and sort by value center Y of each one
        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset # 02, 06
            self.internal_surf.blit(sprite.image, offset_pos) # 02, 06

        # 06 scale surf, vec2 * zoom
        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center= (self.half_w, self.half_h))
        
        self.display_surface.blit(scaled_surf, scaled_rect) # 06
        
        # pygame.draw.rect(self.display_surface, 'green', self.camera_rect, 3)

# pygame setup ========================================
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((640,360), pygame.SCALED, vsync=1)

# Game setup ==========================================
# pygame.event.set_grab(True) # 05 the mouse can't leave the window game 

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
        
        if event.type == pygame.MOUSEWHEEL:
            camera_group.zoom_scale += event.y * 0.03

    # Draw - Update ===================================
    screen.fill('dodgerblue4')
    
    camera_group.update()
    camera_group.custom_draw(player) 

# pygame setup ========================================    
    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption(f'{clock.get_fps():.0f}')