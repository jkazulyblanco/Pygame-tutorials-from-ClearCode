import pygame
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self):

        # level setup
        self.display_surf = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = CameraGroup() # for showing
        self.active_sprites = pygame.sprite.Group() # only update the sprites that need updatating
        self.collision_sprites = pygame.sprite.Group() # for the player collide with

        # Level
        self.setup_level()

    def setup_level(self):
        for row_index, row in enumerate(LEVEL_MAP):
            # print(f'{row_index}:{row}--> {row_index * TILE_SIZE}'.center(50,' ')) # show table
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if col == 'X': # for draw tile
                    Tile((x, y), [self.visible_sprites, self.collision_sprites])
                if col == 'P': # for draw player
                    self.player = Player((x, y), [self.visible_sprites, self.active_sprites], self.collision_sprites)

    def run(self): # run the game (level)
        self.active_sprites.update()
        self.visible_sprites.custom_draw(self.player)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(100,300)

        # camera type 01 # center camera
        # self.half_w = self.display_surf.get_size()[0] // 2
        # self.half_h = self.display_surf.get_size()[1] // 2

        # camera type 02 # bounding box camera
        cam_left = CAMERA_BORDERS['left']
        cam_top = CAMERA_BORDERS['top']
        cam_width = SCREEN_WIDTH -cam_left -CAMERA_BORDERS['right']
        # cam_width = self.display_surf.get_size()[0] - (cam_left + CAMERA_BORDERS['right'])
        cam_height = SCREEN_HEIGHT -cam_top -CAMERA_BORDERS['bottom']
        # cam_height = self.display_surf.get_size()[1] - (cam_top + CAMERA_BORDERS['right'])

        self.camera_rect = pygame.Rect(cam_left, cam_top, cam_width, cam_height)

    def custom_draw(self, player):
        # camera type 01 # get the player offset
        # self.offset.x = player.rect.centerx - self.half_w
        # self.offset.y = player.rect.centery - self.half_h

        # camera type 02 # getting camera position
        if player.rect.left < self.camera_rect.left:
            self.camera_rect.left = player.rect.left
        if player.rect.right > self.camera_rect.right:
            self.camera_rect.right = player.rect.right
        if player.rect.top < self.camera_rect.top:
            self.camera_rect.top = player.rect.top
        if player.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player.rect.bottom

        # camera type 02 # camera offset
        self.offset = pygame.math.Vector2(
            self.camera_rect.left - CAMERA_BORDERS['left'],
            self.camera_rect.top - CAMERA_BORDERS['top']
        )

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surf.blit(sprite.image, offset_pos)       