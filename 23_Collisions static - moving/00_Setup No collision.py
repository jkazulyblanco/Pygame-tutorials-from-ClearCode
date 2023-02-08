import pygame, sys, time
from pygame.math import Vector2 as vec2
from debug import debug

class StaticObstacle(pygame.sprite.Sprite):
    def __init__(self, pos, size, color, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft= pos)

class MovingVerticalObstacle(StaticObstacle):
    def __init__(self, pos, size, color, groups):
        super().__init__(pos, size, color, groups)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.pos = vec2(self.rect.topleft)
        self.direction = vec2((0,1))
        self.speed = 450
        
    def update(self, dt):
        # set bounding collision height and reverse direction
        if self.rect.bottom > 620:
            self.rect.bottom = 620
            self.pos.y = self.rect.y
            self.direction.y *= -1
        if self.rect.top < 100:
            self.rect.top = 100
            self.pos.y = self.rect.y
            self.direction.y *= -1
        
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)

class MovingHorizontalObstacle(StaticObstacle):
    def __init__(self, pos, size, color, groups):
        super().__init__(pos, size, color, groups)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.pos = vec2(self.rect.topleft)
        self.direction = vec2((1,0))
        self.speed = 400
        
    def update(self, dt):
        if self.rect.right > 1150:
            self.rect.right = 1150
            self.pos.x = self.rect.x
            self.direction.x *= -1
        if self.rect.left < 400:
            self.rect.left = 400
            self.pos.x = self.rect.x
            self.direction.x *= -1
        
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.Surface((30,60))
        self.image.fill('cyan')
        self.rect = self.image.get_rect(topleft= (640,360))

        self.pos = vec2(self.rect.topleft)
        self.direction = vec2(1,1)
        self.speed = 200

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.direction.y = -1
        elif keys[pygame.K_s]: self.direction.y = 1
        else: self.direction.y = 0
        
        if keys[pygame.K_a]: self.direction.x = -1
        elif keys[pygame.K_d]: self.direction.x = 1
        else: self.direction.x = 0

    def update(self, dt):
        self.input()
        # normalize the vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos += self.direction * self.speed * dt
        self.rect.topleft = round(self.pos.x), round(self.pos.y)

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.Surface((40,40))
        self.image.fill('red')
        self.rect = self.image.get_rect(center= (640,360))

        self.pos = vec2(self.rect.topleft)
        self.direction = vec2(1,1)
        self.speed = 400


# pygame setup =====================================
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720), vsync=1)

# Game setup =======================================
# Group setup
all_sprites = pygame.sprite.Group()
collision_sprites = pygame.sprite.Group()

# sprite setup
StaticObstacle((100,300), (100,50), 'yellow', [all_sprites, collision_sprites])
StaticObstacle((800,600), (100,200), 'yellow', [all_sprites, collision_sprites])
StaticObstacle((900,200), (200,10), 'yellow', [all_sprites, collision_sprites])
MovingVerticalObstacle((200,300), (200,60), 'green', [all_sprites, collision_sprites])
MovingHorizontalObstacle((850,350), (100,100), 'purple', [all_sprites, collision_sprites])
Player(all_sprites)
Ball(all_sprites)

# delta time
last_time = time.time()


# game loop =========================================
while True:

    # delta time
    dt = time.time() - last_time
    last_time = time.time()

    # event loop ===================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw - update ================================
    screen.fill('gray15')

    all_sprites.update(dt)
    all_sprites.draw(screen)

    debug(f'x, y :{pygame.mouse.get_pos()}')
    debug(f'FPS :{clock.get_fps():.0f}', 40)


    pygame.display.update()
    clock.tick(60)