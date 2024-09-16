# 01 # Setup | # 02 # Drawing | # 03 # Animation |
# 04 # Input | # 05 # Score | # 06 # timer |
# 07 # Sound |

# ▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀

# 01 # Imports
import pygame, sys, random

def ball_animation(): # 03 #
    # Movement
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # 03 # Collisions
    # Ball and window
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound) # 07 #
        ball_speed_y *= -1
    
    # 05 # add point to score
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound) # 07 #
        score_time = pygame.time.get_ticks() # 06 # only run once 
        player_score += 1

    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound) # 07 #
        score_time = pygame.time.get_ticks() # 06 # only run once
        opponent_score += 1

    # ball and paddles
    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(paddle_sound) # 07 #
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 10:
            ball_speed_y *= -1
            
    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(paddle_sound) # 07 #
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 10:
            ball_speed_y *= -1          

def player_animation(): # 04 #
    player.y += player_speed
    # player limits
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_ai(): # 04 #
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    # limits
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart(): # 04 #
    global ball_speed_x, ball_speed_y, score_time
    # 06 # run all time
    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)

    if current_time - score_time < 700: # 06 # seconds
        count_number3 = counter_font.render('3', False, light_grey)
        screen.blit(count_number3, (screen_width/2 -25, screen_height - 220))
    
    if 700 < current_time - score_time < 1400: # 06 # seconds
        count_number2 = counter_font.render('2', False, light_grey)
        screen.blit(count_number2, (screen_width/2 -25, screen_height - 220))
    
    if 1400 < current_time - score_time < 2100: # 06 # seconds
        count_number1 = counter_font.render('1', False, light_grey)
        screen.blit(count_number1, (screen_width/2 -25, screen_height - 220))
    
    if current_time - score_time < 2100: # 06 # 2.1 seconds
        ball_speed_x, ball_speed_y = 0,0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None

# 01 # General setup
pygame.init()
# pygame.mixer.pre_init(44100,-16,2,512) # 07 #
clock = pygame.time.Clock()

# 01 # Setting up the main window
resolution = screen_width, screen_height = (1280,720)
screen = pygame.display.set_mode(resolution, pygame.SCALED)
game_name = 'PING PONG'

# 02 # Colors
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)

# 02 # Game Rectangles
ball = pygame.Rect(screen_width /2 -15, screen_height /2 -15, 30, 30)
player = pygame.Rect(screen_width -20, screen_height /2 -70, 10, 100)
opponent = pygame.Rect(10, screen_height /2 -70, 10, 100)

# 03 # Speed - Game Variables
ball_speed_x = 7 * random.choice((1, -1)) # 04 #
ball_speed_y = 7 * random.choice((1, -1)) # 04 #
player_speed = 0 # 04 #
opponent_speed = 7 # 04 #

# 05 # Text Variables
player_score = 0 
opponent_score = 0
game_font = pygame.font.Font('graphics/Doom.ttf', 42)
counter_font = pygame.font.Font('graphics/Doom.ttf', 162)

# 06 # Score Timer
score_time = True

# 07 # Sound
pong_sound = pygame.mixer.Sound('audio/pong.wav')
score_sound = pygame.mixer.Sound('audio/score.wav')
paddle_sound = pygame.mixer.Sound('audio/paddle.wav')


while True:
    # 01 # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # 04 # Input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed -= 7
            if event.key == pygame.K_DOWN:
                player_speed += 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed += 7
            if event.key == pygame.K_DOWN:
                player_speed -= 7       

    # Game Logic
    ball_animation() # 03 #
    player_animation() # 04 #
    opponent_ai() # 04 #
    

    # 02 # Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

    if score_time:
        ball_restart()

    # 05 # Text Surface
    player_text = game_font.render(f'{player_score}', False, light_grey)
    screen.blit(player_text, (screen_width/2 + 10,screen_height/10 - 8))

    opponent_text = game_font.render(f'{opponent_score}', False, light_grey)
    screen.blit(opponent_text, (screen_width/2 - 23,screen_height/10 - 8))
    
    # 01 # Updating the window
    pygame.display.flip()
    clock.tick(60)
    pygame.display.set_caption(f'{game_name}   FPS: {clock.get_fps() :.2f}')
    