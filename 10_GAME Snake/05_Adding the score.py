import pygame, sys, random
from pygame.math import Vector2

class Snake:
    def __init__(self):
        # position of 3 cells 
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False
        # head positions
        self.head_up = pygame.image.load('graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('graphics/head_left.png').convert_alpha()
        # tail positions
        self.tail_up = pygame.image.load('graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('graphics/tail_left.png').convert_alpha()
        # body positions
        self.body_vertical = pygame.image.load('graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('graphics/body_horizontal.png').convert_alpha()
        # body parts, topright, topleft, bottomright, bottomleft
        self.body_tr = pygame.image.load('graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        # enumetate give a index to each element inside of list
        for index, block in enumerate(self.body):
            # rect for the positioning
            pos_x, pos_y = int(block.x*TILE), int(block.y*TILE)
            block_rect = pygame.Rect(pos_x, pos_y, TILE, TILE)
            
            # what direction of the face heading
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) -1: # select the last
                screen.blit(self.tail, block_rect)
            else: # Know the body's position blocks -- directions
                previous_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                # same row x --> vertical
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                # same col y --> horizontal
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else: # Corners # 
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1: 
                        screen.blit(self.body_tl, block_rect) # x=-1 , y=-1
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1: 
                        screen.blit(self.body_bl, block_rect) # x=-1 , y= 1
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1: 
                        screen.blit(self.body_tr, block_rect) # x= 1 , y=-1
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1: 
                        screen.blit(self.body_br, block_rect) # x= 1 , y= 1
                
    def update_head_graphics(self): # second - first (blocks)
        # know the position of the first block of the body according to the head
        head_relation = self.body[1] - self.body[0] # answer == -1, left of the head
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down
 
    def update_tail_graphics(self): # penultimate - last (blocks)
        # know the position of the last block of the body according to the tail
        tail_relation = self.body[-2] - self.body[-1] # answer == -1, left of the tail
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            # insert at first element 
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            # go from the first elemen to the last -1
            body_copy = self.body[:-1]
            # insert at first element 
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_sound(self):
        self.crunch_sound.play()

class Fruit:
    def __init__(self):
        # position x, y, 
        self.randomize()

    def draw_fruit(self):
        # create rectangle
        fruit_rect = pygame.Rect(int(self.pos.x*TILE), int(self.pos.y*TILE), TILE,TILE)
        # draw the rectangle
        # pygame.draw.rect(screen, 'red', fruit_rect)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        # position x, y, 
        self.x = random.randint(0, cells-1)
        self.y = random.randint(0, cells-1)
        self.pos = Vector2(self.x, self.y)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        # if postion of fruit and first box of snake == head are the same
        if self.fruit.pos == self.snake.body[0]:
            # Reposition the fruit
            self.fruit.randomize()
            # add another block to the snake
            self.snake.add_block()
            # sound
            self.snake.play_sound()

        # avoid the fruit appear in the snake body
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        # check if snake head is not outside between 0 and 20 cells
        if not 0 <= self.snake.body[0].x < cells or not 0 <= self.snake.body[0].y < cells:
            self.game_over()
        # check if snake hits itself
        for block in self.snake.body[1:]: # start in second block until the end
            if block == self.snake.body[0]: # if head hit body
                self.game_over()

    def game_over(self):
        self.snake.direction = Vector2(0,0)
        self.snake.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        # self.fruit.randomize()

    def draw_grass(self):
        grass_color = (15,65,15)
        for row in range(cells):
            if row % 2 == 0:
                for col in range(cells):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*TILE, row*TILE, TILE,TILE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:        
                for col in range(cells):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*TILE, row*TILE, TILE,TILE)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body)-3) # start in 0
        score_surface = game_font.render(score_text, True, 'red')
        score_x = int(TILE*cells -1.5*TILE)
        score_y = int(TILE*1.5)
        score_rect = score_surface.get_rect(center= (score_x, score_y))
        apple_rect = apple.get_rect(midright= (score_rect.left-5, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width+score_rect.width+20, apple_rect.height)
        # draw
        pygame.draw.rect(screen, 'magenta', bg_rect,3,8)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)

        
# Setup ==================================================
pygame.init()
pygame.mixer.pre_init(44100,-16,2,512)
clock = pygame.time.Clock()

TILE = 40
cells = 15
screen = pygame.display.set_mode((cells*TILE, cells*TILE), vsync=1)


# Surfaces ===============================================
apple = pygame.image.load('graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('font/PoetsenOne-Regular.ttf', 25)
main_game = Main()


# Events
SCREEN_UPDATE = pygame.USEREVENT +1
pygame.time.set_timer(SCREEN_UPDATE, 200)

# Game Loop ==============================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Events =====================================
        if event.type == SCREEN_UPDATE:
            main_game.update()
        
        # Key Input ==================================
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1) 
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0) 
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1) 
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)


    # Draw - Update ======================================
    # blit = block image transfer
    screen.fill((10,55,10))

    main_game.draw_elements()

    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption(f'SNAKE  {clock.get_fps():.0f}')
    
    # https://www.youtube.com/watch?v=QFvqStqPCRU