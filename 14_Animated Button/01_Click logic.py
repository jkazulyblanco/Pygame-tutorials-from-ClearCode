# 00 Create Button | 01 Click Logic |

import pygame, sys

class Button: # 00
    def __init__(self, text, width, height, pos):
        # 01 Core Attributes
        # Do once 
        self.pressed = False # not pressed
        
        # top rectangle
        self.top_rect = pygame.Rect(pos,(width, height))
        self.top_color = 'cyan4'
        # text
        self.text_surf = gui_font.render(text, True, 'white')
        # rect created in the center of top rect
        self.text_rect = self.text_surf.get_rect(center= self.top_rect.center)
    
    def draw(self):
        # rect
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        # text
        screen.blit(self.text_surf, self.text_rect)
        self.check_clic() # 01
    
    def check_clic(self): # 01
        mouse_pos = pygame.mouse.get_pos()
        # if mouse touch the button
        if self.top_rect.collidepoint(mouse_pos):
            # if left mouse was preseed
            if pygame.mouse.get_pressed()[0]:
            # Do once logic
                self.pressed = True # pressed
            else:
                if self.pressed == True: # if was pressed
                    print('click')
                    self.pressed = False # when release

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500,500), vsync=1)

# 00
gui_font = pygame.font.Font(None, 30)
button1 = Button('One Punch', 200,40, (150,200))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 00
    screen.fill('red4')
    button1.draw()

    pygame.display.update()
    clock.tick(60)