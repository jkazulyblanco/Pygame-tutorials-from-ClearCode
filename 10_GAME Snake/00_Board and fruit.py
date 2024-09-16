import pygame, sys, random
from pygame.math import Vector2

class Fruit:
    def __init__(self):
        # position x, y, 
        self.x = random.randint(0, cells-1)
        self.y = random.randint(0, cells-1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        # create rectangle
        fruit_rect = pygame.Rect(int(self.pos.x*TILE), int(self.pos.y*TILE), TILE,TILE)
        # draw the rectangle
        pygame.draw.rect(screen, 'red', fruit_rect)

# Setup ==================================================
pygame.init()
clock = pygame.time.Clock()

TILE = 30
cells = 20
screen = pygame.display.set_mode((cells*TILE, cells*TILE), vsync=1)


# Surfaces ===============================================
fruit = Fruit()


# Game Loop ==============================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Key events =====================================

    # Draw - Update ======================================
    # blit = block image transfer
    screen.fill('goldenrod3')
    fruit.draw_fruit()
    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption(f'SNAKE  {clock.get_fps():.0f}')
    