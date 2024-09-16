import pygame, sys, time
from settings import *
from debug import debug 
from level import Level

class Zelda:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW, vsync=1)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Zelda Setup')
        # Game setup --------------------------------------------
        self.show_debug = False
        self.level = Level()
        # sound
        main_sound = pygame.mixer.Sound('../audio/main.ogg')
        main_sound.set_volume(0.5)
        main_sound.play(loops=-1)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # input
            if event.type == pygame.KEYDOWN:
                self.level.player.attack_once()
                self.level.toggle_menu()
                self.level.upgrade_menu.input_menu()
                if event.key == pygame.K_p:
                    self.show_debug = not self.show_debug
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    self.level.player.hightligh_weapon = False
                if event.key == pygame.K_e:
                    self.level.player.hightligh_magic = False

    def display_info(self):
        debug('press P to show info', 0, screen_width-250, 15)
        if self.show_debug:
            debug(f'{self.clock.get_fps():.0f}', 0, screen_width-50)
            debug('movement: w-a-s-d', 20, screen_width-250, 15)
            debug('Attack: I, change: Q', 40, screen_width-250, 15)
            debug('Magic: O, change: E', 60, screen_width-250, 15)
            debug('Menu: M, navigation: <-, ->', 80, screen_width-250, 15)
            debug('exp in menu: space_bar', 100, screen_width-250, 15)
            
    def draw_update(self):
        self.screen.fill(WATER_COLOR)
        self.level.run()
        self.display_info()

    def run(self):
        while True:
            self.check_events()
            self.draw_update()
            # pygame setup
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Zelda()
    game.run()