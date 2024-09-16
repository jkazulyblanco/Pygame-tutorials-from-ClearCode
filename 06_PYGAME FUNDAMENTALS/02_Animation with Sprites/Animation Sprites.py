import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.is_animating = False
        for sprite in range(10):
            images = pygame.image.load(f'graphics/attack_{str(sprite+1)}.png')
            self.sprites.append(images)

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
    
    def animate(self):
        self.is_animating = True

    def update(self):
        if self.is_animating:
            self.current_sprite += 0.2 # animation speed
            
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False

            self.image = self.sprites[int(self.current_sprite)]
        

# General Setup
pygame.init()
clock = pygame.time.Clock()

# Game Screen
res = screen_width, screen_height = 125, 125
screen = pygame.display.set_mode(res, pygame.SCALED, vsync=1)
title = 'Sprite Animation'

# IMPORTS - OBJECTS ==============================
# Sprites and groups
player = Player(5, 10)
moving_sprites = pygame.sprite.Group()
moving_sprites.add(player)

while True: # =====================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # KEYMAP CONTROLLER =======================
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.animate()
    # CALL GAME LOGIC =============================

    # DRAWING =====================================
    pygame.display.flip()
    screen.fill('pink')            
    moving_sprites.draw(screen)
    moving_sprites.update()
    clock.tick(60)
    pygame.display.set_caption(f'{title} fps: {clock.get_fps() :.0f}')

