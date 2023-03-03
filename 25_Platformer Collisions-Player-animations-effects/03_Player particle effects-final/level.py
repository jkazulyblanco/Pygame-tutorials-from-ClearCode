import pygame
from tiles import Tile
from player import Player
from settings import *
from particles import ParticleEffect

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        # camera
        self.world_shift = 0
        # collision left right fix
        self.current_x = 0

        # Dust Animation ----------------------------------
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.palyer_on_ground = False

    # convert list to level
    def setup_level(self, layout):
        # groups
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                # tiles positions
                x = col_index * TILE_WIDTH
                y = row_index * TILE_HEIGHT

                # to draw level
                if cell == 'X':
                    tile = Tile((x, y), TILE_WIDTH, TILE_HEIGHT)
                    self.tiles.add(tile)
                # to draw player
                if cell == 'P':
                    player_sprite = Player((x, y), self.display_surface, self.jump_particles)
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x        

        if player_x <= 300 and direction_x < 0:
            self.world_shift = 4
            # player.rect.left = 300-16
            player.speed = 0
        elif player_x >= 800 and direction_x > 0:
            self.world_shift = -4
            # player.rect.right = 800+32
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 4

    # COLLISIONS PLAYER ======================================= {#fd9,0
    def horizontal_collisions(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right +3
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left -3
                    player.on_right = True
                    self.current_x = player.rect.right
        
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x >= 0):
            player.on_right = False
    
    def vertical_collisions(self):
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0 # fix increase of gravity
                    player.on_ground = True # fix animation {#dbc,0}
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0 # fix jump below obstacle
                    player.on_ceiling = True # fix animation {#dbc,0}
            
            # fix animation {#dbc,0}
            if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
                player.on_ground = False
            if player.on_ceiling and player.direction.y > 0:
                player.on_ceiling = False

    # ANIMATION ==============================================
    def jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,15)
        else:
            pos += pygame.math.Vector2(10,-15)
        jump_effect = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_effect)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 20)
            else:
                offset = pygame.math.Vector2(-10, 20)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def run(self):
        # First Draw -------------------------------------
        self.tiles.draw(self.display_surface)
        self.player.draw(self.display_surface)        
        # dust particles
        self.dust_sprite.draw(self.display_surface)

        # Second Update ------------------------------
        self.scroll_x()
        self.tiles.update(self.world_shift)
        # player
        self.player.update()
        self.horizontal_collisions()
        # vertical update has order 
        self.get_player_on_ground() # 1
        self.vertical_collisions()  # 2
        self.landing_dust()         # 3
        # dust particle
        self.dust_sprite.update(self.world_shift)
