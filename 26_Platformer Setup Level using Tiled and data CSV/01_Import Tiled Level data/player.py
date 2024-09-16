import pygame
from pygame.math import Vector2 as vec2
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, jump_particles):
        super().__init__()
        # animation -----------------------------------------
        self.character_status()
        self.frame_index = 0
        self.animation_speed = 0.17
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft= pos)

        # dust particles
        self.character_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.20
        self.display_surface = surface

        # animation status
        self.status = 'idle'
        self.facing_right = True

        # fix animation {#dbc,0}
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        
        # movement ------------------------------------------
        self.direction = vec2(0,0)
        self.speed = 4 # overwrite in level
        # jump
        self.gravity = 0.8
        self.jump_speed = -16
        self.air_jump = False
        # jump particles
        self.jump_particles = jump_particles
        
    # IMPORT IMAGES ==========================================
    def character_status(self):
        character_path = '../graphics/character/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def character_particles(self):
        self.dust_run_path = import_folder('../graphics/character/dust_particles/run/')


    # ANIMATION ==============================================
    # looping animations -------------------------------------
    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def character_animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        # normal and flipped images
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
        
        # Animation and collision
        self.fix_bugs()

    def fix_bugs(self):
        # fix animation, in level for images with different size {#dbc,1}
        # fix collisions left and right
        # set the new rectangle
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright= self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft= self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom= self.rect.midbottom)
        if self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright= self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft= self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop= self.rect.midtop)
 
    def character_particles_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_path):
                self.dust_frame_index = 0
            dust_particle = self.dust_run_path[int(self.dust_frame_index)]
            
            if self.facing_right:
                pos = self.rect.bottomleft - vec2(15, 8) # offset position
                self.display_surface.blit(dust_particle, pos)
            else:
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                pos = self.rect.bottomright - vec2(1, 8) # offset position
                self.display_surface.blit(flipped_dust_particle, pos)


    # MOVEMENT ===============================================
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        # if keys[pygame.K_SPACE]:
        #     self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        if self.on_ground:
            self.direction.y = self.jump_speed
            self.air_jump = True
            self.jump_particles(self.rect.midbottom)
        elif self.air_jump:
            self.direction.y = self.jump_speed
            self.air_jump = False


    def update(self):
        self.get_input()
        self.get_status()
        self.character_animate()
        self.character_particles_animation()
        
        
