import pygame
from math import ceil


class Background(pygame.sprite.Sprite):
    def __init__(self,image, display_height):
        pygame.sprite.Sprite.__init__(self)
        # Create Image and Rect
        self.image = image
        self.rect = self.image.get_rect()

        # Calculate scaled dimensions
        ratio = float(self.rect.size[0]/self.rect.size[1])
        self.height = display_height
        self.width = int(ceil(self.height * ratio))

        # Transform image
        self.image = pygame.transform.scale(self.image,(self.width, self.height))
        self.rect = self.image.get_rect()