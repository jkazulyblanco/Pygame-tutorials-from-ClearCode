import pygame, sys

class ParticlePrinciple:
    def __init__(self):
        self.particles = []

    def emit(self): # moves and draws Particles
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                # NESTED DATA from self.particles list from particle_circle
                # move, pos_y += direction
                particle[0][1] += particle[2]
                # shrink, radius -= 0.2
                particle[1] -= 0.2
                # draw circle around particle        position         radius
                pygame.draw.circle(screen, 'white', particle[0], int(particle[1]))

    def add_particles(self): # adds Particles
         pos_x, pos_Y = 250,250
         radius = 10
         direction = -3
         particle_circle = [[pos_x, pos_Y], radius, direction]
         self.particles.append(particle_circle)


    def delete_particles(self): # life time of Particles
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy

# setup ==============================================
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500,500))

# Surfaces ===========================================
particle1 = ParticlePrinciple()

# call particle event every 40 milliseconds
PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT, 140)

# Game Loop ==========================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Key events =================================
        if event.type == PARTICLE_EVENT:
            particle1.add_particles()
    
    # Draw - Update ==================================
    screen.fill('black')

    particle1.emit()

    pygame.display.update()
    clock.tick(60)