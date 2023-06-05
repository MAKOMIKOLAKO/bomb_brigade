import pygame

class destructable(pygame.sprite.Sprite):

    def __init__(self, pos, size):
        super().__init__() # Inherits properties of pygame.sprite.Sprite

        self.image = pygame.image.load('crates.png')
        self.rect = self.image.get_rect(topleft=pos)


