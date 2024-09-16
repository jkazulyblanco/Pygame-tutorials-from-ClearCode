import pygame
from sys import exit
from random import randint, choice

# class object
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1,player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom= (80,300))
        self.gravity = 0
        # sound
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.07
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom= (randint(900,1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.07
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score(): # TEXT 2
    # init
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False,(64,64,64))
    score_rect = score_surf.get_rect(center= (400,50))
    # draw
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
# window game name
pygame.display.set_caption('Runner')
# limit frame rate
clock = pygame.time.Clock()
# Font
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
# Game State
game_active = False
# reset Time
start_time = 0
score = 0
# sound
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops= -1) # forever loop

# Group Sprite # class object
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#***************************************************

# Images, .convert() pygame works more faster
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Intro Screen
# Player Transform test
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
# rotozoom = scale and rotate
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center= (400,200))
# Title
game_name = test_font.render('Martian Runner',False,'blue')
game_name_rect = game_name.get_rect(center= (400,80))
game_message = test_font.render('Press space to run', False, 'blue')
game_message_rect = game_message.get_rect(center= (400,330))

# Timer
# USEREVENT is only used for pygame but to avoid any issue add +1 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

#*****************************************************
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                # class
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail']))) # fly: 25%, snail: 75%
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)
    
    if game_active:
        # DRAW ALL - OUT ELEMENTS
# Images # blit = transferencia de imagenes en bloque, poner una superficie sobre otra
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        # TEXT 2
        score = display_score()
        
        # Player       
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()
        
        # collision to game over
        game_active = collision_sprite()
                
    else:
        screen.fill((94,129,162)) # rgb
        # Player Transform test
        screen.blit(player_stand, player_stand_rect)

        # score
        score_message = test_font.render(f'Your Score: {score}', False, 'green')
        score_message_rect = score_message.get_rect(center= (400,330))
        # game name
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
    


    # update everything
    pygame.display.update()  
    # frame rate 60 fps
    clock.tick(60)