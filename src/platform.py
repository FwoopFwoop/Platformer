import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, color, (width,height), (x,y)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width,height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x, self.y = (x,y)
        self.rect.y = self.y
        self.rect.x = 0