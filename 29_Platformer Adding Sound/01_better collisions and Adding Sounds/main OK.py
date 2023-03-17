import pygame, sys, time
from settings import *
from debug import debug
from level import Level
from game_data import level_0
from overworld import Overworld
from ui import UI


class Game:
    def __init__(self):
        # game attributes
        self.max_level = 0
        # audio
        self.level_bg_music = pygame.mixer.Sound('../audio/level_music.wav')
        self.level_bg_music.set_volume(0.3)
        self.overworld_bg_music = pygame.mixer.Sound('../audio/overworld_music.wav')
        self.overworld_bg_music.set_volume(0.3)

        # UI
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0
        self.ui = UI(screen)

        # overworld creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops=-1)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops=-1)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.level_bg_music.stop()
        self.overworld_bg_music.play(loops=-1)
    
    # User interface 
    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.cur_health += amount
        
    def check_game_over(self):
        if self.cur_health <= 0:
            self.cur_health = 100
            self.coins = 0
            # self.max_level = 0
            # self.overworld = Overworld(0, self.max_level, self.game.screen, self.create_level)
            self.status = 'overworld'
            self.level_bg_music.stop()
            self.overworld_bg_music.play(loops=-1)

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.draw()
            self.level.update()
            self.ui.show_health(self.cur_health, self.max_health)
            self.ui.show_coins(self.coins, 22, 'black', 2)
            self.ui.show_coins(self.coins, 20, 'orange2')
            self.check_game_over()


# pygame setup
pygame.init()
screen = pygame.display.set_mode(RES, vsync=1)
clock = pygame.time.Clock()
pygame.display.set_caption(title)

# Game setup ---------------------------------------------
debug_on = False

# level = Level(level_0, screen) 
game = Game()


# Game Loop ==============================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # key events =================================
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.level.player.sprite.jump()
            if event.key == pygame.K_p:
                debug_on = not debug_on

    screen.fill('deepskyblue2')
    # level.draw() 
    # level.update() da 
    game.run()

    debug('press P for info and FPS', 0, screen_width-250, 15)
    # debug(pygame.mouse.get_pos(), 40, screen_width-500, 15)
    if debug_on:
        debug(f'FPS: {clock.get_fps():.0f}')
        debug('press Enter to play level', 20, screen_width-250, 15)
        debug('a,d,space to play', 40, screen_width-250, 15)
        debug('left right to Navigate', 60, screen_width-250, 15)
    
    pygame.display.update()
    clock.tick(60)
