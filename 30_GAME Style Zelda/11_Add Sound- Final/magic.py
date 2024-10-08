from settings import *

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal':pygame.mixer.Sound('../audio/heal.wav'),
            'flame': pygame.mixer.Sound('../audio/fire.wav')
        }

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal', player.rect.center + pygame.math.Vector2(0,-80), groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            self.sounds['flame'].play()

            if player.status.split('_')[0] == 'right':
                direction = vec2(1,0)
            elif player.status.split('_')[0] == 'left':
                direction = vec2(-1,0)
            elif player.status.split('_')[0] == 'up':
                direction = vec2(0,-1)
            else:
                direction = vec2(0,1)

            # draw images side by side
            for i in range(1,6):
                if direction.x: # horizontal
                    offset_x = (direction.x * i) * TILE
                    x = player.rect.centerx + offset_x + randint(-TILE//3, TILE//3)
                    y = player.rect.centery + randint(-TILE//3, TILE//3)
                    self.animation_player.create_particles('flame', (x,y), groups)
                else: # vertical
                    offset_y = (direction.y * i) * TILE
                    x = player.rect.centerx+ randint(-TILE//3, TILE//3)
                    y = player.rect.centery + offset_y + randint(-TILE//3, TILE//3)
                    self.animation_player.create_particles('flame', (x,y), groups)

