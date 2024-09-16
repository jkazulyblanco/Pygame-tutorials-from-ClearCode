# 00 Create Button | 01 Click Logic | 02 Styling

import pygame, sys

class Button: # 00
    def __init__(self, text, width, height, pos, elevation): # 02
        # 01 Core Attributes
        # Do once 
        self.pressed = False # not pressed
        # 02 elevation values no pressed and pressed
        self.elevation = elevation
        self.pressed_elevation = elevation
        self.original_y_pos = pos[1]
        
        # top rectangle
        self.top_rect = pygame.Rect(pos,(width, height))
        self.top_color = 'cyan4'
        
        # 02 Bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = 'darkslateblue'

        # text
        self.text_surf = gui_font.render(text, True, 'magenta')
        # rect created in the center of top rect
        self.text_rect = self.text_surf.get_rect(center= self.top_rect.center)
    
    def draw(self):
        # 02 elevation Logic
        self.top_rect.y = self.original_y_pos - self.pressed_elevation
        self.text_rect.center = self.top_rect.center
        
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.pressed_elevation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=80)
        # rect
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=80)
        # text
        screen.blit(self.text_surf, self.text_rect)
        self.check_clic() # 01
    
    def check_clic(self): # 01
        mouse_pos = pygame.mouse.get_pos()
        # if mouse touches the button
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = 'cyan3' # # 02 highlight
            # if left mouse was preseed
            if pygame.mouse.get_pressed()[0]:
                self.pressed_elevation = 0 
            # Do once logic
                self.pressed = True # pressed
            else:
                self.pressed_elevation = self.elevation # 02 when release
                if self.pressed: # if was pressed
                    print('click')
                    self.pressed = False # when release
        # 02 if mouse no longer touches the button
        else:
            self.pressed_elevation = self.elevation
            self.top_color = 'cyan4'

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500,500), vsync=1)

# 00
gui_font = pygame.font.Font(None, 30)
button1 = Button('One Click', 200,40, (150,200), 6)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 00
    screen.fill('darkgrey')
    button1.draw()

    pygame.display.update()
    clock.tick(60)