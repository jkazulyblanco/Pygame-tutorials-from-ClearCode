import pygame
# 01 Player
class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        self.image = pygame.Surface((4,20))
        self.image.fill('yellow')
        self.rect = self.image.get_rect(center= pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    # if laser is out of screen
    def destroy(self):
        if self.rect.y <= - 50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()
            # print('destroyer')


    def update(self):
        # negative to movin upwards
        self.rect.y -= self.speed
        self.destroy()