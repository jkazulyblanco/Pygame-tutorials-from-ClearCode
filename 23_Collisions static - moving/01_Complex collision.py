# 01 complex collision

import pygame, sys, time
from pygame.math import Vector2 as vec2
from debug import debug

class StaticObstacle(pygame.sprite.Sprite):
    def __init__(self, pos, size, color, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft= pos)
        self.old_rect = self.rect.copy() # 01

class MovingVerticalObstacle(StaticObstacle):
    def __init__(self, pos, size, color, groups):
        super().__init__(pos, size, color, groups)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.pos = vec2(self.rect.topleft)
        self.direction = vec2((0,1))
        self.speed = 450
        self.old_rect = self.rect.copy() # 01
        
    def update(self, dt):
        self.old_rect = self.rect.copy() # 01
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
        self.old_rect = self.rect.copy() # 01
        
    def update(self, dt):
        self.old_rect = self.rect.copy() # 01
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
    def __init__(self, groups, obstacles):
        super().__init__(groups)
        self.image = pygame.Surface((30,60))
        self.image.fill('cyan')
        self.rect = self.image.get_rect(topleft= (640,360))
        self.old_rect = self.rect.copy() # 01

        self.pos = vec2(self.rect.topleft)
        self.direction = vec2(1,1)
        self.speed = 200
        self.obstacles = obstacles # 01

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.direction.y = -1
        elif keys[pygame.K_s]: self.direction.y = 1
        else: self.direction.y = 0
        
        if keys[pygame.K_a]: self.direction.x = -1
        elif keys[pygame.K_d]: self.direction.x = 1
        else: self.direction.x = 0

    def collision(self, direction): # 01 best collision
        # which object overlap
        collision_sprites = pygame.sprite.spritecollide(self, self.obstacles, False)
        if collision_sprites:
            if direction == 'horizontal':
                for sprite in collision_sprites:
                    # collision on the right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x
                    # collision on the left
                    elif self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x
            elif direction == 'vertical':
                for sprite in collision_sprites:
                    # collision on the bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                    # collision on the top
                    elif self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y
                    
    def update(self, dt):
        self.old_rect = self.rect.copy() # 01
        self.input()
        # normalize the vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Collision update by direction
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)
        self.collision('vertical')

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, obstacles, player):
        super().__init__(groups)
        
        self.image = pygame.Surface((40,40))
        self.image.fill('red')
        self.rect = self.image.get_rect(center= (640,360))
        self.old_rect = self.rect.copy() # 01

        self.pos = vec2(self.rect.topleft)
        self.direction = vec2(1,1)
        self.speed = 600
        

        self.obstacles = obstacles
        self.player = player

    def collision(self, direction): # 01 best collision
        # which object overlap
        collision_sprites = pygame.sprite.spritecollide(self, self.obstacles, False)
        
        if self.rect.colliderect(self.player.rect):
            collision_sprites.append(self.player)
        
        if collision_sprites:
            if direction == 'horizontal':
                for sprite in collision_sprites:
                    # collision on the right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.direction.x *= -1
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x
                    # collision on the left
                    elif self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.direction.x *= -1
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x
            elif direction == 'vertical':
                for sprite in collision_sprites:
                    # collision on the bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.direction.y *= -1
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                    # collision on the top
                    elif self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.direction.y *= -1
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y


    def window_collision(self, direction):
        if direction == 'horizontal':
            if self.rect.left <= 0 or self.rect.right >= 1280:
                self.direction.x *= -1
                self.pos.x = self.rect.x
        elif direction == 'vertical':
            if self.rect.top <= 0 or self.rect.bottom >= 720:
                self.direction.y *= -1        
                self.pos.y = self.rect.y

    def update(self, dt):
        self.old_rect = self.rect.copy() # 01
        
        # normalize the vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Collision update by direction
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')
        self.window_collision('horizontal')
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)
        self.collision('vertical')
        self.window_collision('vertical')


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
player = Player(all_sprites, collision_sprites) #01
ball = Ball(all_sprites, collision_sprites, player)

# delta time
last_time = time.time()


# game loop =========================================
while True:

    # delta time
    dt = time.time() - last_time
    last_time = time.time()
    if dt > 0.05: continue

    # event loop ===================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw - update ================================
    screen.fill('gray15')

    all_sprites.update(dt)
    
    # debug
    # for sprite in all_sprites.sprites():
    #     pygame.draw.rect(screen, 'red', sprite.old_rect)

    all_sprites.draw(screen)

    debug(f'x, y :{pygame.mouse.get_pos()}')
    debug(f'FPS :{clock.get_fps():.0f}', 40)


    pygame.display.update()
    clock.tick(60)