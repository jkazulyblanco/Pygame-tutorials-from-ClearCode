import pygame
from laser import Laser
# 01 Player
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load('../graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom= pos)
        self.speed = speed
        self.max_x_constraint = constraint # == screen_width
        
        # timer to do once in specific time in milliseconds
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 300

        # instance of laser class
        self.lasers = pygame.sprite.Group()
        # Audio
        self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
        self.laser_sound.set_volume(0.2)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.rect.x += self.speed  
        elif keys[pygame.K_a]: 
            self.rect.x -= self.speed

        # shooting
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, 8, 600)) # laser, pos
        self.laser_sound.play()
        
    
    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()