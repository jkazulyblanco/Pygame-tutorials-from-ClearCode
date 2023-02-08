import pygame, sys
from random import randrange

class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('graphics/tree.png').convert_alpha()
        self.rect = self.image.get_rect(topleft= pos)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(center= pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5

    def input(self):
        keys = pygame.key.get_pressed()
        # up, down
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        # right, left 
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed

# Drawing order by Y position
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft= (0,0))

    def custom_draw(self):
        # ground
        self.display_surface.blit(self.ground_surf, self.ground_rect)


        # cicle for all sprites             and sort by value center Y of each one
        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            self.display_surface.blit(sprite.image, sprite.rect)


# pygame setup ========================================
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720), vsync=1)

# Game setup ==========================================
camera_group = CameraGroup()
player = Player((640,360), camera_group)

# Random trees
for i in range(20):
    random_x = randrange(0,1000,84)
    random_y = randrange(0,1000,84)
    Tree((random_x, random_y), camera_group)

# Game Loop ===========================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw - Update ===================================
    screen.fill('dodgerblue3')

    camera_group.update()
    camera_group.custom_draw()

    # debug
    pygame.draw.rect(screen, 'white', player.rect, 2)

# pygame setup ========================================    
    pygame.display.update()
    clock.tick(60)