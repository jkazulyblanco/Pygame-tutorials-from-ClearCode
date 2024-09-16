import pygame
from sys import exit
from random import randint

def display_score(): # TEXT 2
    # init
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False,(64,64,64))
    score_rect = score_surf.get_rect(center= (400,50))
    # draw
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    # check if the list has elements
    if obstacle_list:
        # draw and movement
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf,obstacle_rect)
                pygame.draw.rect(screen, 'green', obstacle_rect,3)
            else:
                screen.blit(fly_surf, obstacle_rect)
                pygame.draw.rect(screen, 'blue', obstacle_rect,3)
        # delete obstacles out of the screen for performance
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surf, player_index
    # check if player is on floor
    if player_rect.bottom < 300:
        # jump
        player_surf = player_jump
    else:
        # walking on floor
        player_index += 0.07 # for slow speed anim
        # reset if the num is above of 1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

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
#***************************************************

# suface and color
test_surface = pygame.Surface((10,20))
test_surface.fill('Red')
# Images, .convert() pygame works more faster
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Font Text 1
# score_surf = test_font.render('Alien Runner', False, (64, 64, 64))
# score_rect = score_surf.get_rect(center= (400,50))

# OBSTACLES
# snail, .convert_alpha() to use images whit transparency
# snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
# snail_rect = snail_surface.get_rect(midbottom= (600,300))
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# fly_surf = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]


obstacle_rect_list = []

# RECTANGLES
# Player

player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1,player_walk2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
# player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom= (80,300))

# GRAVITY
player_gravity = 0

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

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

#*****************************************************
while True:
    
    if game_active:
        # DRAW ALL - OUT ELEMENTS
        # Images
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        # blit = transferencia de imagenes en bloque, poner una superficie sobre otra
        screen.blit(test_surface,(200,10)) # rect red
        # text 1
        # pygame.draw.rect(screen, 'green', score_rect, 10, 20)
        # pygame.draw.rect(screen, '#c0a8ec', score_rect, 5) # hexadecimal color
        # screen.blit(score_surf,score_rect)
        # TEXT 2
        score = display_score()
    
        # Snail 
        # snail_rect.x -= 4
        # if snail_rect.right <= 0: snail_rect.left = 800
        # pygame.draw.rect(screen, 'blue', snail_rect,3)
        # screen.blit(snail_surface, snail_rect)

        # Player
        # player_rect.left += 1
        pygame.draw.rect(screen, 'gray', player_rect,3)
        screen.blit(player_surf, player_rect)
        # Player gravity
        player_gravity += 1
        player_rect.y += player_gravity
        player_animation() 
        # Player collision, simulate touch the ground with a single point
        if player_rect.bottom >= 300: player_rect.bottom = 300

        # OBSTACLE MOVEMENT
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        

        # collision to game over
        # if snail_rect.colliderect(player_rect):
        #     game_active = False
        game_active = collisions(player_rect,obstacle_rect_list)

        # INPUT KEYS
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print('jump')

        # COLLISION WITH RECTANGLES
        # if player_rect.colliderect(snail_rect): # return 0 or 1, off/on
        #     print('collision')

        # mouse_pos = pygame.mouse.get_pos()
        # if player_rect.collidepoint(mouse_pos):
        #     print('collide')
            # show the mouse button pressed
            # print(pygame.mouse.get_pressed())
    
    else:
        screen.fill((94,129,162)) # rgb
        # Player Transform test
        screen.blit(player_stand, player_stand_rect)
        
        # reset settings
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        # score
        score_message = test_font.render(f'Your Score: {score}', False, 'green')
        score_message_rect = score_message.get_rect(center= (400,330))
        # game name
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            # MOUSE ACTIONS
            # pygame.MOUSEBUTTONDOWN -> cuando se mantiene presionado el boton
            # pygame.MOUSEBUTTONUP   -> cuando se deja de presionar el boton
            # if event.type == pygame.MOUSEMOTION: # this works when moving the mouse
            #     if player_rect.collidepoint(event.pos): print('collision')
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
                player_gravity = -20

            # KEYS ACTIONS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20        
            # if event.type == pygame.KEYUP: print('key up')

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rect.left = 800
                start_time = int(pygame.time.get_ticks()/1000)
        
        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2): # return value 0 or 1
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright= (randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright= (randint(900,1100),210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]




    # update everything
    pygame.display.update()  
    # frame rate 60 fps
    clock.tick(60)