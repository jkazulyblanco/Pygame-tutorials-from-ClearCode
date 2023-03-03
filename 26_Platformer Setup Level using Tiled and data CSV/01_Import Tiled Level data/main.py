import pygame, sys, time
from settings import *
from debug import debug
from level import Level
from game_data import level_0


# time = 2.25.57

class Main:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(RES, vsync=1)
        self.clock = pygame.time.Clock()
        self.p_time = time.time()
        pygame.display.set_caption(title)
        
        self.debug_on = False
        # Game setup ---------------------------------------------
        self.class_instances() 

    def class_instances(self):        
        self.level = Level(level_0, self.screen)

    def draw(self):
        self.screen.fill('deepskyblue2')
        self.level.draw()

        debug('press P for Debug', 0, screen_width-200)
        if self.debug_on:
            debug(f'FPS: {self.clock.get_fps():.0f}')
            # pygame.draw.rect(screen, 'green', level.player.sprite.rect, 2)
       

    def update(self):
        # pygame setup
        self.clock.tick(60)
        pygame.display.update()

        # game updates
        self.level.update()

    def check_events(self):
        # pygame setup
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # key events =================================
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.level.player.sprite.jump()
                if event.key == pygame.K_p:
                    self.debug_on = not self.debug_on

    def run(self):
        # Game Loop ==============================================
        while True:
            self.dt = time.time() - self.p_time
            self.p_time = time.time()
            if self.dt > 0.05: continue

            self.check_events()
            self.draw()
            self.update()

if __name__ == '__main__':
    game = Main()
    game.run()

            

            
            
            
            

