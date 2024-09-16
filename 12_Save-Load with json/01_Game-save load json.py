import pygame, sys, json

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600,400), vsync=1)


# Surfaces ==========================================
game_font = pygame.font.Font(None, 32)

# rectangles =========================================
red_surf = pygame.Surface([200,100])
red_surf.fill('red3')
red_rect = red_surf.get_rect(center= (150,250)) # relative to screen

blue_surf = pygame.Surface([200,100])
blue_surf.fill('blue3')
blue_rect = blue_surf.get_rect(center= (450,250)) # relative to screen

# Reset 
reset_red_surf = pygame.Surface([200,100])
reset_red_surf.fill('orange4')
reset_red_rect = red_surf.get_rect(center= (150,120)) # relative to screen

reset_blue_surf = pygame.Surface([200,100])
reset_blue_surf.fill('cyan2')
reset_blue_rect = blue_surf.get_rect(center= (450,120)) # relative to screen

# Data ***********************************************
data = {'AMD': 0, 'intel': 0 }
click_file = 'clicker_score.txt'
# Load Data from existing file, if not exist give an error, to fix use try - except
try:
    with open(click_file) as score_file:
        data = json.load(score_file)
except:
    print('New file to Save Data Created')

# text ===============================================
red_score_surf = game_font.render(f'CPU AMD: {data["AMD"]}', True, 'black')
red_score_rect = red_score_surf.get_rect(center= (150,320))

blue_score_surf = game_font.render(f'CPU intel: {data["intel"]}', True, 'black')
blue_score_rect = blue_score_surf.get_rect(center= (450,320))

# Reset Text
red_reset_score_surf = game_font.render(f'Reset AMD', True, 'black')
red_reset_score_rect = red_reset_score_surf.get_rect(center= (150,120))

blue_reset_score_surf = game_font.render(f'Reset intel', True, 'black')
blue_reset_score_rect = blue_reset_score_surf.get_rect(center= (450,120))

# Game Loop ===========================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save File
            with open(click_file, 'w') as score_file:
                json.dump(data, score_file)

            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if red_rect.collidepoint(event.pos):
                data['AMD'] += 1
                red_score_surf = game_font.render(f'CPU AMD: {data["AMD"]}', True, 'black')
                red_score_rect = red_score_surf.get_rect(center= (150,320))
                           
            if blue_rect.collidepoint(event.pos):
                data['intel'] += 1                 
                blue_score_surf = game_font.render(f'CPU intel: {data["intel"]}', True, 'black')
                blue_score_rect = blue_score_surf.get_rect(center= (450,320))
            # # Reset
            if reset_red_rect.collidepoint(event.pos):
                data['AMD'] = 0
                red_score_surf = game_font.render(f'CPU AMD: {data["AMD"]}', True, 'black')
                red_score_rect = red_score_surf.get_rect(center= (150,320))
            if reset_blue_rect.collidepoint(event.pos):
                data['intel'] = 0
                blue_score_surf = game_font.render(f'CPU intel: {data["intel"]}', True, 'black')
                blue_score_rect = blue_score_surf.get_rect(center= (450,320))          
            
            


    # Drawing
    screen.fill('cyan4')
    screen.blit(red_surf, red_rect)
    screen.blit(blue_surf, blue_rect)
    screen.blit(red_score_surf, red_score_rect)
    screen.blit(blue_score_surf, blue_score_rect)
    # Reset
    screen.blit(reset_red_surf, reset_red_rect)
    screen.blit(reset_blue_surf, reset_blue_rect)

    screen.blit(red_reset_score_surf, red_reset_score_rect)
    screen.blit(blue_reset_score_surf, blue_reset_score_rect)


    pygame.display.update()
    clock.tick(60)
