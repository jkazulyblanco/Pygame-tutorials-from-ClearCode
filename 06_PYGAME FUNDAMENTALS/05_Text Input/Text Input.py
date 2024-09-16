import pygame, sys
# General Setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,200))

# Text
base_font = pygame.font.Font(None, 60)
user_text = ''
# text surface and color
input_rect = pygame.Rect(10, 50, 300, 95)
input_rect_color = pygame.Color('lightskyblue3') 
color_active = pygame.Color('yellow')
color_pasive = input_rect_color
# State
active = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else: 
                active = False
        # keyboard events
        if event.type == pygame.KEYDOWN:
            if active == True:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1] # delete the las character
                else:
                    user_text += event.unicode # allow write text

    # Drawing
    screen.fill('darkgreen')
    # swithc States color
    if active:
        input_rect_color = color_active
    else:
        input_rect_color = color_pasive

    # text Rectangle
    pygame.draw.rect(screen, input_rect_color, input_rect, 2)
    
    # text
    text_surface = base_font.render(user_text, True, ('darkorange'))
    screen.blit(text_surface, (input_rect.x+25, input_rect.y+25)) # draw the surface at the position of the rect
    input_rect.w = max(200, text_surface.get_width()+10)


    pygame.display.flip()
    clock.tick(60)
