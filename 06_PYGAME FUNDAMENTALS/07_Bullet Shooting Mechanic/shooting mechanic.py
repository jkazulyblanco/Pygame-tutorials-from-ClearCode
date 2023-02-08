import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.image = pygame.Surface((100, 100))
        self.image = pygame.image.load('space_ship.png')
        # self.image.fill('blue')
        self.rect = self.image.get_rect(center= (screen_width/2, screen_height/2))

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def create_bullet(self): # vector need x and y
        return Bullet(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        # self.image = pygame.Surface((30, 5))
        self.image = pygame.image.load('bullet.ico')
        # self.image.fill('darkorange')
        self.rect = self.image.get_rect(center= (pos_x, pos_y))

    def update(self):
        self.rect.x += 15
        # Delete things out of screen to prevent crash
        if self.rect.x >= screen_width + 50:
            self.kill()

# Setup ===========================================
pygame.init()    
clock = pygame.time.Clock()
window = screen_width, screen_height = 600, 600
screen = pygame.display.set_mode(window)
pygame.mouse.set_visible(False) # Hide mouse

# SURFACES =========================================
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

bullet_group = pygame.sprite.Group()


while True: # =====================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # key events ==============================
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet_group.add(player.create_bullet())


    # Drawing =====================================
    screen.fill('black') # BG
    bullet_group.draw(screen) # Bullet
    player_group.draw(screen) # Player
    
    # Update ======================================
    player_group.update() # Player
    bullet_group.update() # Bullet


    pygame.display.flip()
    clock.tick(60)