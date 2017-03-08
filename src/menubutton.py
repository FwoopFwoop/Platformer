import pygame
import color


class MenuButton(pygame.sprite.Sprite):
    def __init__(self, (display_width, display_height), y, color=color.black, text='', text_color=color.white):
        pygame.sprite.Sprite.__init__(self)

        self.height = display_height/8
        self.width = self.height * 3
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(color)

        self.font = pygame.font.SysFont("monospace", 24)
        self.textSurf = self.font.render(text, 1, text_color)
        self.image.blit(self.textSurf, ((self.width-self.textSurf.get_width())/2,
                (self.height-self.textSurf.get_height())/2))

        self.rect = self.image.get_rect()
        self.rect.x = (display_width-self.width)/2
        self.rect.y = y