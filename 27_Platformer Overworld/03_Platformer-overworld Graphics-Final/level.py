import pygame
from support import import_csv_layout, import_cut_graphics, import_folder
from settings import *
from tiles import Tile, StaticTile, AnimatedTile
from enemies import Enemy
from decoration import Sky, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels

class Level:
    def __init__(self, current_level, surface, create_overworld):
        # Screen setup
        self.display_surface = surface
        self.world_shift = 0 # fake camera

        # Overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']


        # import data terrain
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        # import grass_small
        grass_layout = import_csv_layout(level_data['grass_small'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass_small')
        # herb
        grass_1_layout = import_csv_layout(level_data['grass'])
        self.grass_1_sprites = self.create_tile_group(grass_1_layout, 'grass')
        # bg_palms
        bg_palms_layout = import_csv_layout(level_data['bg_palms'])
        self.bg_palms_sprites = self.create_tile_group(bg_palms_layout, 'bg_palms')
        # crates
        crates_layout = import_csv_layout(level_data['crates'])
        self.crates_sprites = self.create_tile_group(crates_layout, 'crates')
        # coins
        coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_layout, 'coins')
        # fg_palms
        fg_palms_layout = import_csv_layout(level_data['fg_palms'])
        self.fg_palms_sprites = self.create_tile_group(fg_palms_layout, 'fg_palms')
        # enemies
        enemies_layout = import_csv_layout(level_data['enemies'])
        self.enemies_sprites = self.create_tile_group(enemies_layout, 'enemies')
        # constraints
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.constraints_sprites = self.create_tile_group(constraints_layout, 'constraints')
        # water
        water_layout = import_csv_layout(level_data['water'])
        self.water_sprites = self.create_tile_group(water_layout, 'water')

        # Decoration
        self.sky = Sky(7)
        self.clouds = Clouds(300, 60*TILE_WIDTH, 20)
        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        self.current_x = 0


    def create_tile_group(self, layout, layer):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                x = col_index * TILE_WIDTH
                y = row_index * TILE_HEIGHT
                if value != '-1':
                # empty tile in Tiled is represented -1,
                    if layer == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles.png', TILE_WIDTH, TILE_HEIGHT)
                    # in Tiled program avoid use flipped images because with this method the flipped images aren't flipped
                    # the sprite only has 16 tiles, to avoid error out of range --> use %
                        tiles = terrain_tile_list[int(value)%16]
                        sprite = StaticTile(x, y, tiles)
                    # grass_small
                    if layer == 'grass_small':
                        grass_tile_list = import_cut_graphics('../graphics/decoration/grass/grasss.png', TILE_WIDTH, TILE_HEIGHT)
                        tiles = grass_tile_list[int(value)%5]
                        sprite = StaticTile(x, y, tiles)
                    # grass_1
                    if layer == 'grass':
                        grass_1_tile_list = import_cut_graphics('../graphics/decoration/grass/grass.png', TILE_WIDTH, 56)
                        tiles = grass_1_tile_list[int(value)%5]
                        sprite = StaticTile(x, y+10, tiles)
                    # crates, offset Y because height is 42, then 64 - 42 = 22
                    if layer == 'crates':
                        tiles = pygame.image.load('../graphics/terrain/crate.png')
                        sprite = StaticTile(x, y+22, tiles)
                    # bg palms, offset Y because height is 128, then 64 - 128 = -64
                    if layer == 'bg_palms':
                        tiles = import_folder('../graphics/terrain/palm_bg')                        
                        sprite = AnimatedTile(x, y-64, tiles, 0.1100)
                    # fg palms, offset X,Y because X:64-78=-14, Y:64-136=-72
                    if layer == 'fg_palms':
                        if value == '1':
                            tiles = import_folder('../graphics/terrain/palm_large')                        
                            sprite = AnimatedTile(x-14, y-72, tiles, 0.1050)
                        elif value == '0': # X:64-80=-6 Y:64-103=-39
                            tiles = import_folder('../graphics/terrain/palm_small')                        
                            sprite = AnimatedTile(x-6, y-39, tiles)
                    # coins, offset X,Y because X=32 y=32 ,64-32=32 and /2 to center
                    if layer == 'coins':               
                        if value == '0': tiles = gold = import_folder('../graphics/coins/gold')
                        elif value == '1': tiles = silver = import_folder('../graphics/coins/silver')                      
                        sprite = AnimatedTile(x+16, y+16, tiles, 0.1050)
                    # enemies, offset X,Y because X:64-51=13, Y:64-46=18
                    if layer == 'enemies':
                        path = import_folder('../graphics/enemy/run')
                        sprite = Enemy(x+13, y+18, path)
                    # constraints
                    if layer == 'constraints':
                        sprite = Tile(x, y) 
                    # water
                    if layer == 'water':
                        tiles = import_folder('../graphics/decoration/water')
                        sprite = AnimatedTile(x, y+20, tiles, 0.1100)
                    
                    sprite_group.add(sprite)

        return sprite_group

    def enenmy_collision_reverse(self):
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints_sprites, False):
                enemy.reverse()

    # PLAYER ===========================================
    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                x = col_index * TILE_WIDTH
                y = row_index * TILE_HEIGHT
                if value == '0':
                    sprite = Player((x,y), self.display_surface, self.jump_particles)
                    self.player.add(sprite)
                elif value == '1': 
                    # goal, offset X,Y because X:64-48=16, Y:64-28=36 center--> /2
                    hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(x+8, y+16, hat_surface)
                    self.goal.add(sprite)

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

    # COLLISIONS PLAYER ------------------------------- {#fd9,0
    def horizontal_collisions(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        
        
        for sprite in self.terrain_sprites.sprites():
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
        for sprite in self.terrain_sprites.sprites():
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

    def check_death(self):
        if self.player.sprite.rect.top > screen_heihgt:
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    # Run the entire game / level
    def draw(self):
        # Decoration Background
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface)
        # # objects
        self.bg_palms_sprites.draw(self.display_surface)
        self.terrain_sprites.draw(self.display_surface)
        self.fg_palms_sprites.draw(self.display_surface)
        self.crates_sprites.draw(self.display_surface)
        self.grass_1_sprites.draw(self.display_surface)
        self.coins_sprites.draw(self.display_surface)
        self.grass_sprites.draw(self.display_surface)
        self.enemies_sprites.draw(self.display_surface)
        self.water_sprites.draw(self.display_surface)
        # # debug constraint
        # # self.constraints_sprites.draw(self.display_surface)
        # # Player
        self.goal.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.player.update()
        # dust
        self.dust_sprite.draw(self.display_surface)
        self.dust_sprite.update(self.world_shift)

    def update(self):
        self.clouds.update(self.world_shift)
        self.bg_palms_sprites.update(self.world_shift)
        self.terrain_sprites.update(self.world_shift)
        self.fg_palms_sprites.update(self.world_shift)
        self.crates_sprites.update(self.world_shift)
        self.grass_1_sprites.update(self.world_shift)
        self.coins_sprites.update(self.world_shift)
        self.grass_sprites.update(self.world_shift)
        self.enemies_sprites.update(self.world_shift)
        self.water_sprites.update(self.world_shift)
        # constaints only update
        self.check_death()
        self.check_win()
        self.constraints_sprites.update(self.world_shift)
        self.enenmy_collision_reverse()
        # Player
        self.scroll_x()
        self.goal.update(self.world_shift)
        
        self.horizontal_collisions()
        # vertical update has order 
        self.get_player_on_ground() # 1
        self.vertical_collisions()  # 2
        self.landing_dust()         # 3


        
        