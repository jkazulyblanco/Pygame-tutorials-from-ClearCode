import pygame, sys, time
from settings import *
from debug import debug
from level import Level
from game_data import levels
from overworld import Overworld

# 1:35:00

class Game:
    def __init__(self, game):
        self.game = game
        self.max_level = 0
        self.overworld = Overworld(0, self.max_level, self.game.screen, self.create_level)
        self.status = 'overworld'

    def create_level(self, current_level):
        self.level = Level(current_level, self.game.screen, self.create_overworld)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, self.game.screen, self.create_level)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.draw()
            self.level.update()

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

    def draw(self):
        self.screen.fill('deepskyblue2')

        debug('press P for FPS', 0, screen_width-250, 15)
        debug('press Enter to play level', 20, screen_width-250, 15)
        if self.debug_on:
            debug(f'FPS: {self.clock.get_fps():.0f}')
       

    def update(self):
        
        # game updates
        self.game.run()

        # pygame setup
        self.clock.tick(60)
        pygame.display.update()


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

    def run(self):
        # Game Loop ==============================================
        while True:
            self.check_events()
            self.draw()
            self.update()

if __name__ == '__main__':
    game = Main()
    game.run()

            

            
            
            
            

