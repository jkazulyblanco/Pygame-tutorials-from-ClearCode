import pygame, sys, time
from settings import *
from debug import debug
from level import Level
from game_data import level_0
from overworld import Overworld


class Game:
    def __init__(self):
        self.max_level = 0
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.draw()
            self.level.update()


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
    # level.update() 
    game.run()

    debug('press P for FPS', 0, screen_width-250, 15)
    debug('press Enter to play level', 20, screen_width-250, 15)
    if debug_on:
        debug(f'FPS: {clock.get_fps():.0f}')
    
    pygame.display.update()
    clock.tick(60)
