import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/link.png').convert_alpha()
        self.rect = self.image.get_rect(center= (300,300))
        self.health = 5
        self.max_healt = 14

    def get_damage(self):
        if self.health > 0:
            self.health -= 1

    def get_health(self):
        if self.health < self.max_healt:
            self.health += 1

    # Draw single image heart by self.health
    def full_hearts(self):
        for heart in range(self.health):
            screen.blit(full_heart, (heart*40, 45))

    # Draw two images: 1 heart by self.health, 1 empty heart by self.max_health
    def empty_hearts(self):
        for heart in range(self.max_healt):
            if heart < self.health:
                screen.blit(full_heart, (heart*40, 5))
            else:
                screen.blit(empty_heart, (heart*40, 5))

    # divide all lives /2 and draw each live as half heart
    def half_hearts(self):
        half_heart_total = self.health /2
        half_heart_exists = half_heart_total - int(half_heart_total) != 0 # return float 0.5 == false

        for heart in range(int(self.max_healt/2)):
            # draw full heart
            if int(half_heart_total) > heart:
                screen.blit(full_heart, (heart*40, 85))
            # draw half heart
            elif half_heart_exists and int(half_heart_total) == heart:
                screen.blit(half_heart, (heart*40, 85))
            # draw empty heart
            else:
                screen.blit(empty_heart, (heart*40, 85))

    def update(self):
        self.full_hearts()
        self.empty_hearts()
        self.half_hearts()

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600,600), vsync=1)

# Surfaces ====================================
link = pygame.sprite.GroupSingle(Player())

full_heart = pygame.image.load('graphics/full_heart.png').convert_alpha()
half_heart = pygame.image.load('graphics/half_heart.png').convert_alpha()
empty_heart = pygame.image.load('graphics/empty_heart.png').convert_alpha()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # key events ==========================
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                link.sprite.get_health()
            if event.key == pygame.K_DOWN:
                link.sprite.get_damage()

    screen.fill('black')

    link.draw(screen)
    link.update()

    pygame.display.update()
    clock.tick(60)