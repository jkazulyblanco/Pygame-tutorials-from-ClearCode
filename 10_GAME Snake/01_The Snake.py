import pygame, sys, random
from pygame.math import Vector2

class Snake:
    def __init__(self):
        # position of 3 cells 
        self.body = [Vector2(5,10), Vector2(6,10), Vector2(7,10)]
        self.direction = Vector2(1,0)

    def draw_snake(self):
        for block in self.body:
            # create rectangle
            pos_x, pos_y = int(block.x*TILE), int(block.y*TILE)
            block_rect = pygame.Rect(pos_x, pos_y, TILE, TILE)
            # draw the rectangle
            pygame.draw.rect(screen, 'darkgreen', block_rect)

    def move_snake(self):
        # go from the first elemen to the last -1
        body_copy = self.body[:-1]
        # insert at first element 
        body_copy.insert(0,body_copy[0] + self.direction)
        self.body = body_copy[:]

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
snake = Snake()


# Events
SCREEN_UPDATE = pygame.USEREVENT +1
pygame.time.set_timer(SCREEN_UPDATE, 150)

# Game Loop ==============================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Events =====================================
        if event.type == SCREEN_UPDATE:
            snake.move_snake()
        
        # Key Input ==================================
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.direction = Vector2(0,-1) 
            if event.key == pygame.K_RIGHT:
                snake.direction = Vector2(1, 0) 
            if event.key == pygame.K_DOWN:
                snake.direction = Vector2(0, 1) 
            if event.key == pygame.K_LEFT:
                snake.direction = Vector2(-1,0) 


    # Draw - Update ======================================
    # blit = block image transfer
    screen.fill('goldenrod3')
    fruit.draw_fruit()
    snake.draw_snake()


    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption(f'SNAKE  {clock.get_fps():.0f}')
    
    # https://www.youtube.com/watch?v=QFvqStqPCRU