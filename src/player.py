import pygame
from math import ceil


class Player (pygame.sprite.Sprite):
    height, width = 0, 0

    def __init__(self, image, display_height):
        pygame.sprite.Sprite.__init__(self)
        # Create Image and Rectangular Bounds
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        # Calculate desired dimensions based on screen size
        ratio = float(self.rect.size[1]/self.rect.size[0])
        self.height = display_height/6
        self.width = int(ceil(ratio*self.height))

        # Transform image
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()