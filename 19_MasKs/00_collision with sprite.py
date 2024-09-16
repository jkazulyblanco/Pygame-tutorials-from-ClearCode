import pygame, sys

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40,40))
        self.image.fill('red')
        self.rect = self.image.get_rect(center= (350,350))
        # create mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if pygame.mouse.get_pos():
            self.rect.center = pygame.mouse.get_pos()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/alpha.png').convert_alpha()
        self.rect = self.image.get_rect(center= (350,350))

        # create mask
        self.mask = pygame.mask.from_surface(self.image)

# pygame setup =======================================
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((700,700), vsync=1)

# Game setup =========================================
player = pygame.sprite.GroupSingle(Player())
obstacle = pygame.sprite.GroupSingle(Obstacle())

# Game Loop ==========================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw - Update
    screen.fill('white')
    player.update()
    obstacle.draw(screen)
    player.draw(screen)

    # border image
    pygame.draw.rect(screen, 'blue', obstacle.sprite.rect, 2)

    # collision only activate the mask when collide with the bound of the sprite
    # for best performace, use mask is heavy
    if pygame.sprite.spritecollide(player.sprite, obstacle, False):
        if pygame.sprite.spritecollide(player.sprite, obstacle, False, pygame.sprite.collide_mask):
            player.sprite.image.fill('green')
        else:
            player.sprite.image.fill('red')

    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption(f'{clock.get_fps():.0f}')