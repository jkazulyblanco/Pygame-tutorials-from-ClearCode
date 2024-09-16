import pygame, sys

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

pygame.init()
clock = pygame.time.Clock()

res = screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode(res)

 # object
crosshair = Crosshair(50,50, 100,100, (255,255,255))

# Create a group and put the object
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()

    crosshair_group.draw(screen)

    clock.tick(60)
    pygame.display.set_caption(f'fps: {clock.get_fps() :.2f}')