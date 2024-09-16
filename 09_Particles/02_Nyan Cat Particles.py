import pygame, sys, random

class ParticlePrinciple:
    def __init__(self):
        self.particles = []

    def emit(self): # moves and draws Particles
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                # NESTED DATA from self.particles list from particle_circle
                # move, pos_y += direction
                particle[0][1] += particle[2][0]
                # move, pos_x += direction
                particle[0][0] += particle[2][1]
                # shrink, radius -= 0.2
                particle[1] -= 0.2
                # draw circle around particle        position         radius
                pygame.draw.circle(screen, 'white', particle[0], int(particle[1]))

    def add_particles(self): # adds Particles
         pos_x, pos_y = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
         radius = 10
         direction_x = random.randint(-3,3)
         direction_y = random.randint(-3,3)
         particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
         self.particles.append(particle_circle)


    def delete_particles(self): # life time of Particles
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy

class ParticleNyan:
    def __init__(self):
        self.particles = []
        self.size = 20

    def emit(self): # moves and draws Particles
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                # NESTED DATA from self.particles list from particle_rect append
                particle[0].x -= 2
                # draw circle around particle   color, rect    
                pygame.draw.rect(screen, particle[1], particle[0])
        self.draw_nyancat()

    def add_particles(self, offset, color): # adds Particles
         pos_x = pygame.mouse.get_pos()[0]
         pos_y = pygame.mouse.get_pos()[1] + offset
         particle_rect = pygame.Rect(int(pos_x-self.size/2), int(pos_y-self.size/2), self.size,self.size)
         self.particles.append((particle_rect, color))


    def delete_particles(self): # life time of Particles
        particle_copy = [particle for particle in self.particles if particle[0].x > 0]
        self.particles = particle_copy

    def draw_nyancat(self):
        nyan_rect = nyan_surface.get_rect(center= pygame.mouse.get_pos())
        screen.blit(nyan_surface, nyan_rect)

class ParticleStart:
    def __init__(self):
        self.particles = []
        self.surface = pygame.image.load('graphics/star.png').convert_alpha()
        self.width = self.surface.get_rect().width
        self.height = self.surface.get_rect().height

    def emit(self): # moves and draws Particles
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                # NESTED DATA from self.particles list from particles.append
                # move, rect x += direction_x
                particle[0].x += particle[1]
                # move, rect y += direction_y
                particle[0].y += particle[2]
                # shrink, radius -= 0.2
                particle[3] -= 0.2
                screen.blit(self.surface, particle[0])

    def add_particles(self): # adds Particles
         pos_x = pygame.mouse.get_pos()[0] - self.width/2 
         pos_y = pygame.mouse.get_pos()[1] - self.height/2
         direction_x = random.randint(-4,4)
         direction_y = random.randint(-4,4)
         lifetime = random.randint(4,10)
         particle_rect = pygame.Rect(int(pos_x),int(pos_y), self.width, self.height)
         self.particles.append([particle_rect, direction_x, direction_y, lifetime])


    def delete_particles(self): # life time of Particles
        particle_copy = [particle for particle in self.particles if particle[3] > 0]
        self.particles = particle_copy

# setup ==============================================
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500,500), vsync=1)

# Surfaces ===========================================
particle1 = ParticlePrinciple()
particle2 = ParticleNyan()
particle3 = ParticleStart()

nyan_surface = pygame.image.load('graphics/nyan_cat.png').convert_alpha()

# call particle event every 40 milliseconds
PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT, 40)

# Game Loop ==========================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Key events =================================
        if event.type == PARTICLE_EVENT:
            
            particle1.add_particles()
            
            particle2.add_particles(-50, 'red')
            particle2.add_particles(-30, 'orange')
            particle2.add_particles(-10, 'yellow')
            particle2.add_particles(10, 'green')
            particle2.add_particles(30, 'cyan')
            particle2.add_particles(50, 'blue')

            particle3.add_particles()
    
    # Draw - Update ==================================
    screen.fill('black')

    particle1.emit()
    particle3.emit()
    particle2.emit()

    pygame.display.update()
    clock.tick(60)
    pygame.display.set_caption(f'fps: {clock.get_fps():.0f}')