import pygame

# Resource Directories
img_dir = 'resources/png/'


def background(self,image):
    return pygame.image.load(img_dir+image).convert()


def player(self,image):
    return pygame.image.load(img_dir+image).convert_alpha()