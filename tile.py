import pygame

class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, size):
        super().__init__() # Inherits properties of pygame.sprite.Sprite

        #self.image = pygame.image.load('crates.png')
        self.image = pygame.image.load('freecrates.png')
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect(topleft=pos)


