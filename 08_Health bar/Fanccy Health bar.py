import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40,40))
        self.image.fill('grey')
        self.rect = self.image.get_rect(center= (400,300))
        self.current_health = 200
        self.maximum_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.target_health = 500
        self.health_change_speed = 2

    def update(self):
        self.basic_health()
        self.advanced_health()

    def get_damage(self, amount): # press key DOWN
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def get_health(self, amount): # press key UP
        if self.target_health < self.maximum_health:
            self.target_health += amount
        if self.target_health >= self.maximum_health:
            self.target_health = self.maximum_health

    def basic_health(self):
        pygame.draw.rect(screen, 'darkgreen', (10,10, self.health_bar_length, 25))
        pygame.draw.rect(screen, 'lightgreen', (10,10, self.target_health/self.health_ratio, 25))
        pygame.draw.rect(screen, 'white', (10,10, self.health_bar_length, 29), 4)

    def advanced_health(self):
        transition_width = 0
        transition_color = 'red'

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = 'cyan'
            
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = -int((self.target_health - self.current_health) / self.health_ratio) # negative value bar go to left
            transition_color = 'yellow'

        # surfaces
        if self.current_health < self.target_health:
            health_bar_rect = pygame.Rect(10,45, self.current_health / self.health_ratio, 25)
        else:
            health_bar_rect = pygame.Rect(10,45, self.target_health / self.health_ratio, 25)

        transition_bar_rect = pygame.Rect(health_bar_rect.right,45, transition_width, 25)
        # Draw
        pygame.draw.rect(screen, 'darkblue', health_bar_rect)
        pygame.draw.rect(screen, transition_color, transition_bar_rect)
        pygame.draw.rect(screen, 'white', (10,45, self.health_bar_length, 29), 4)


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600), vsync=1)    

# Surfaces ===========================================
player = pygame.sprite.GroupSingle(Player())


# Game Loop ==========================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Key events =================================
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.sprite.get_health(100)
            if event.key == pygame.K_DOWN:
                player.sprite.get_damage(100)

    # Draws and Updates ==============================
    screen.fill('black')
    
    player.draw(screen)
    player.update()

    pygame.display.update()
    clock.tick(60)