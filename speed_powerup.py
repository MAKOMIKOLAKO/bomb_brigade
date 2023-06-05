import pygame, random

class speed_powerup(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("speed_powerup.png")
        self.image = pygame.transform.scale(self.image, (50,52.7027027))
        self.rect = self.image.get_rect(topleft=pos)


    def update(self):
        self.rect.x += random.randint(-5,5)
        self.rect.y += random.randint(-5,5)


