'''
https://opengameart.org/content/shooting-gallery

http://pixelartmaker.com/art/7b0362cb47512cb
'''

import pygame, sys, random

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound('audio/gunshot.wav')
    
    def shoot(self):
        self.gunshot.set_volume(0.2)
        self.gunshot.play()
        pygame.sprite.spritecollide(crosshair, target_group, True)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Target(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

class GameState():
    def __init__(self):
        self.state = 'intro'

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # controller Actions
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'main_game'
                
        # Drawing
        pygame.display.flip()
        screen.blit(intro_bg, (0,0))
        crosshair_group.draw(screen)
        crosshair_group.update()

    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # controller
            if event.type == pygame.MOUSEBUTTONDOWN:
                crosshair.shoot()
        
        # Drawing
        pygame.display.flip()
        screen.blit(background, (0,0))
        target_group.draw(screen)
        crosshair_group.draw(screen)
        crosshair_group.update()

    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'main_game':
            self.main_game()

        

# General Setup
pygame.init()
clock = pygame.time.Clock()
game_state = GameState()
# Game Screen
res = screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode(res)

background = pygame.image.load('graphics/BG.jpg')
intro_bg = pygame.image.load('graphics/intro.jpg')
pygame.mouse.set_visible(False) 

# GAME OBJECTS=====================================

# Crosshair
crosshair = Crosshair('graphics/crosshair.png')
# Create a group and put the object
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

# Target
target_group = pygame.sprite.Group()
for target in range(20):
    new_target = Target('graphics/target.png', random.randrange(0,screen_width), random.randrange(0,screen_height))
    target_group.add(new_target)


while True:
    game_state.state_manager()
    clock.tick(60)
    pygame.display.set_caption(f'fps: {clock.get_fps() :.2f}')