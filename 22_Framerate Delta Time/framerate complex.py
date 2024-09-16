import pygame, sys, time
from debug import debug

class Test(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # animation
        self.frames = [pygame.image.load(f'frames/{i}.png').convert_alpha() for i in range(1,6)]
        self.frame_index = 0

        # image - rect
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midleft= (0, 360))

        # movement
        self.rotation = 0
        self.direction = 1 
        self.move_speed = 210
        self.animation_speed = 12

         # update dt
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt # update dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def move(self, dt):
        self.pos.x += self.direction * self.move_speed * dt  # update dt
        self.rect.x = round(self.pos.x) # update dt
        self.rect.y = round(self.pos.y) # update dt
        if self.rect.right > 1200 or self.rect.left < 0:
            self.direction *= -1

    def rotate(self, dt):
        self.rotation += 41 * dt # update dt
        self.image = pygame.transform.rotozoom(self.image, self.rotation, 2)

    def update(self, dt):  # update dt
        self.animate(dt)
        self.move(dt)
        self.rotate(dt)


# pygame setup ===========================================
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720), vsync=1)

# Game setup ===========================================

test_group = pygame.sprite.Group(Test())


# current time
previous_time = time.time() # for precision 

# game loop =========================================
while True:
    # dt = clock.tick(60) / 1000 # return miliseconds 0.017 = 60
    
    dt = time.time() - previous_time # for precision
    previous_time = time.time() # for precision

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Draw - Update ===================================
    screen.fill('gray15')

    test_group.update(dt) # update dt
    test_group.draw(screen)

    # debug message
    debug(f'milisecons: {dt:.4f}')
    debug(f'FPS :{clock.get_fps():.0f}', 70)

    pygame.display.update()
    clock.tick(60)
    