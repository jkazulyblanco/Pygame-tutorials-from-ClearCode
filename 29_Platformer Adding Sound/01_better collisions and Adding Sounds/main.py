import pygame, sys, time
from settings import *
from debug import debug
from level import Level
from overworld import Overworld
from ui import UI

class Game:
    def __init__(self, game):
        # game attributes
        self.game = game
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
        self.ui = UI(game.screen)

        # overworld creation
        self.overworld = Overworld(0, self.max_level, self.game.screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops=-1)

    def create_level(self, current_level):
        self.level = Level(current_level, self.game.screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops=-1)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, self.game.screen, self.create_level)
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

class Main:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(RES, vsync=1)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(title)
        
        self.debug_on = False
        # Game setup ---------------------------------------------
        self.class_instances() 

    def class_instances(self):
        self.game = Game(self)

    def display_info(self):
        debug('press P for info and FPS', 0, screen_width-250, 15)
        # debug(pygame.mouse.get_pos(), 40, screen_width-500, 15)
        if self.debug_on:
            debug(f'FPS: {self.clock.get_fps():.0f}')
            debug('press Enter to play level', 20, screen_width-250, 15)
            debug('a,d,space to play', 40, screen_width-250, 15)
            debug('left right to Navigate', 60, screen_width-250, 15)

    def check_events(self):
        # pygame setup
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # key events =================================
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game.level.player.sprite.jump()
                if event.key == pygame.K_p:
                    self.debug_on = not self.debug_on

    def draw(self):
        self.screen.fill('deepskyblue2')

    def update(self):
        # game updates
        self.game.run()
        self.display_info()

        # pygame setup
        pygame.display.update()
        self.clock.tick(60)

    def run(self):
        # Game Loop ==============================================
        while True:
            self.check_events()
            self.draw()
            self.update()

if __name__ == '__main__':
    game = Main()
    game.run()

            

            
            
            
            

