# 01 Player | 02 Obstacles | 03 Aliens | 04 Health
# 05 Score | 06 CTR Style

import pygame, sys, math
from player import Player # 01
import obstacle
from random import randrange, choice, randint
from alien import Alien, BonusAlien
from laser import Laser

class Game:
    def __init__(self):
        # 01 Player setup
        player_sprite = Player((screen_width/2,screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # 02 Obstacle Setup ======================================
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4

        # offset x_pos for each new obstacle: [0]= 0, [1]=150, [2]=300, [3]=450
        self.x_pos_offset = [num*(screen_width/self.obstacle_amount) for num in range(self.obstacle_amount)]
        # * unpack lits, when need to use multiple values in one parameter
        self.multiple_obstacles(*self.x_pos_offset, x_pos=40, y_pos=480)

        #other way
        # offset = int(screen_width/self.obstacle_amount)
        # print(offset)
        # for copy in range(self.obstacle_amount):
        #     add_offset = offset * copy
        #     self.create_obstacle(40+add_offset, 50+randrange(-10,10), 0)
        #     print(add_offset)

        # 03 Alien Setup ==================================
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(6, 8)
        self.alien_direction = 1
        # Extra alien
        self.bonus_alien = pygame.sprite.GroupSingle()
        self.bonus_spawn_time = randint(400, 800)

        # 04 Health setup
        self.lives = 3
        self.live_surf = pygame.image.load('../graphics/full_heart.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0]) # get 0 = x size
        # Score setup
        self.score = 0
        self.font = pygame.font.Font('../font/pixeled.ttf', 15)

        # Audio
        self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
        self.explosion_sound.set_volume(0.3)
        music = pygame.mixer.Sound('../audio/music.wav')
        music.set_volume(0.2)
        music.play(loops= -1)

# 02 Obstacles   ======================================           
    def create_obstacle(self, x_pos, y_pos, offset_x): # 02
        # create a index for each row -- list shape separated by ,
        for row_index, row in enumerate(self.shape):
            # create a index in every col in every row
            for col_index, col in enumerate(row):
                if col == 'x':
                    # size of each block == index * size
                    x = x_pos + col_index * self.block_size + offset_x
                    y = y_pos + row_index * self.block_size
                    block = obstacle.Block(self.block_size,'darkgrey', x,y)
                    self.blocks.add(block)
        print(row, col)

    def multiple_obstacles(self, *offset, x_pos, y_pos):
        for offset_x in offset:
            self.create_obstacle(x_pos, y_pos, offset_x)

# 03 Aliens ===========================================
    def alien_setup(self, rows, cols, x_size= 60, y_size=50, x_offset=90, y_offset= 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_size + x_offset # offset all
                y = row_index * y_size + y_offset # offset all
                
                if row_index == 0: alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2: alien_sprite = Alien('green', x, y)
                else: alien_sprite = Alien('red', x, y)

                self.aliens.add(alien_sprite)

    def alien_position_checker(self): # Moving left <--> right
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,-6, screen_height)
            self.alien_lasers.add(laser_sprite)

    def bonus_alien_timer(self):
        self.bonus_spawn_time -= 1
        if self.bonus_spawn_time <= 0:
            self.bonus_alien.add(BonusAlien(choice(['right', 'any']), screen_width))
            self.bonus_spawn_time = randint(400, 800) # reset position

    # Collisions ====================================
    def collision_checks(self):
        # Player Lasers Collision
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # Obstacle collision destroy
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # Aliens collision destroy
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()                    
                # Bonus Alien collision destroy
                if pygame.sprite.spritecollide(laser, self.bonus_alien, True):
                    self.score += 500 # 05
                    laser.kill()
                    self.explosion_sound.play()
                    
        
        # Alien Lasers Collision
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # Obstacle collision destroy
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # Player collision destroy
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1 # 04                     
                    self.explosion_sound.play()
                            
        # Aliens collision, blocks - player
        if self.aliens:
            for alien in self.aliens:
                # when alien collide with block, destroy
                pygame.sprite.spritecollide(alien, self.blocks, True)
                # when alien collide with Player, destroy                
                if pygame.sprite.spritecollide(alien, self.player, False):
                    alien.kill()
                    self.lives -= 1 # 04 
                    self.explosion_sound.play()
                    

# 04 Health Score =======================================
    def display_lives(self):
        for live in range(self.lives):
            x = self.live_x_start_pos - (live * self.live_surf.get_size()[0])
            screen.blit(self.live_surf, (x,8))
        
        if self.lives == 0:
            font = pygame.font.Font('../font/pixeled.ttf', 50)
            text = font.render('GAME OVER', True, 'red')
            text_rect = text.get_rect(center= (screen_width/2, screen_height/2))
            screen.blit(text, text_rect)

    def display_score(self):
        score_surf = self.font.render(f'points: {self.score}', False, 'green')
        text_rect = score_surf.get_rect(topleft= (15,0))
        screen.blit(score_surf, text_rect)

    def victory_message(self):
        if not self.aliens.sprites():
            font = pygame.font.Font('../font/pixeled.ttf', 50)
            text = font.render('YOU WIN', False, 'gold')
            text_rect = text.get_rect(center= (screen_width/2, screen_height/2 -70))
            screen.blit(text, text_rect)


# 00 main setup =========================================
    def Run(self):
        # update all sprite groups
        self.player.update() # 01
        # 03 Aliens
        self.aliens.update(self.alien_direction) # 03
        self.alien_position_checker()
        self.alien_lasers.update()
        self.bonus_alien_timer() 
        self.bonus_alien.update() 
        self.collision_checks()

        # draw all sprite groups ======================
        self.player.sprite.lasers.draw(screen) # 01
        self.player.draw(screen) # 01
        self.blocks.draw(screen) # 02        
        # 03 Aliens
        self.alien_lasers.draw(screen)
        self.aliens.draw(screen) # 03
        self.bonus_alien.draw(screen)

        # 04 Health - Score
        self.display_lives()
        self.display_score()
        self.victory_message()

class CRT: # 06
    def __init__(self):
        self.tv = pygame.image.load('../graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_width,screen_height))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_width/line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0,y_pos), (screen_width, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(45,90)) # flickering effect
        self.create_crt_lines()
        screen.blit(self.tv,(0,0))

# 01 to prevent any error when work with multiple files
if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    window = screen_width, screen_height = 600,600
    screen = pygame.display.set_mode(window, vsync=1)

    # Surfaces ==============================================
    bg = pygame.image.load('../graphics/background.jpg').convert()

    # Object instances
    game = Game()
    crt = CRT()

    # Timer Events =========================================
    ALIEN_LASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIEN_LASER, 800)

    # Game Loop =============================================
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIEN_LASER:
                game.alien_shoot() 

        # Draw ==============================================
        screen.blit(bg, (0,-500))
        
        game.Run()
        crt.draw()

        pygame.display.update()
        clock.tick(60)
        pygame.display.set_caption(f'{clock.get_fps():.0f}')