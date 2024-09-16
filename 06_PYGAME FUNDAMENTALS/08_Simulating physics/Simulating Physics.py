import pygame, sys, pymunk
# for pymunk, 1 create body, 2 shape, 3 add to space
def create_apple(space, pos):
    # masa - inercia - tipo de cuerpo colision
    body = pymunk.Body(mass= 1, moment=100, body_type= pymunk.Body.DYNAMIC) 
    body.position = pos
    shape = pymunk.Circle(body, 20)
    space.add(body, shape)
    return shape

def draw_apples(apples):
    for apple in apples:
        pos_x = int(apple.body.position.x)
        pos_y = int(apple.body.position.y)
        # pygame.draw.circle(screen, 'black', (pos_x, pos_y), 60)
        apple_rect = apple_surface.get_rect(center= (pos_x, pos_y))
        screen.blit(apple_surface, apple_rect)

def static_ball(space, pos):
    body = pymunk.Body(body_type= pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, 40)
    space.add(body, shape)
    return shape

def draw_static_ball(balls):
    for ball in balls:
        pos_x = int(ball.body.position.x)
        pos_y = int(ball.body.position.y)
        pygame.draw.circle(screen, 'magenta', (pos_x, pos_y), 40)

# Main setup ======================================
pygame.init()
window = screen_width, screen_height = 600,600
screen = pygame.display.set_mode(window, vsync=1)
clock = pygame.time.Clock()

# Surfaces ========================================
space = pymunk.Space()
space.gravity = (0,500) # x=0, y=500
apple_surface = pygame.image.load('ball.png')

apples = []
balls = []
balls.append(static_ball(space,(401,400)))
balls.append(static_ball(space,(301,500)))
balls.append(static_ball(space,(201,450)))


# Game Loop =======================================
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Key events ==============================
        if event.type == pygame.MOUSEBUTTONDOWN:
            apples.append(create_apple(space, event.pos))
        
    # Drawing =====================================
    screen.fill('grey')
    draw_apples(apples)
    draw_static_ball(balls)

    # Updates =====================================
    
    
    space.step(1/50) # Pymunk Loop, simulation
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption(f'fps: {clock.get_fps():.0f}')