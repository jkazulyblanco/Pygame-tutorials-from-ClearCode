import pygame, sys

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load('audi.png')
        # to prevent loss of quality when rotate
        self.image = self.original_image
        self.rect = self.image.get_rect(center= (640,360))
        self.angle = 0
        self.rotation_speed = 2.8
        self.direction = 0
        self.forward = pygame.math.Vector2(0,-1)
        self.active = False

    # pygame rotate clockwise
    def set_rotation(self):
        if self.direction == 1:
            self.angle -= self.rotation_speed
        if self.direction == -1:
            self.angle += self.rotation_speed

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.30)
        self.rect = self.image.get_rect(center= self.rect.center)

    def get_rotation(self):
        if self.direction == 1:
            self.forward.rotate_ip(self.rotation_speed) # ip --> in place
        if self.direction == -1:
            self.forward.rotate_ip(-self.rotation_speed) # ip --> in place

    def accelerate(self):
        if self.active:
            self.rect.center += self.forward * 10

    def update(self):
        self.set_rotation()
        self.get_rotation()
        self.accelerate()

# window setup ====================================       
pygame.init()
screen = pygame.display.set_mode((1280,720), vsync=1)        
clock = pygame.time.Clock()

# Surfaces ========================================
bg_track = pygame.image.load('track.png')

car = pygame.sprite.GroupSingle(Car())

# Game Loop =======================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # key events ==============================
        # key down and up to get 0 value when press 2 keys at the same time 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: car.sprite.direction += 1
            if event.key == pygame.K_LEFT: car.sprite.direction -= 1
            if event.key == pygame.K_UP: car.sprite.active = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT: car.sprite.direction -= 1
            if event.key == pygame.K_LEFT: car.sprite.direction += 1
            if event.key == pygame.K_UP: car.sprite.active = False

    # Drawing =====================================
    # screen.fill('black')
    screen.blit(bg_track,(0,0))
    car.draw(screen)

    # Updates =====================================
    car.update()

    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption(f'fps: {clock.get_fps():.0f}')