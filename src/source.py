import pygame

# Resource Directories
img_dir = 'resources/png/'


def background(image):
    return pygame.image.load(img_dir+image).convert()


def player(image):
    return pygame.image.load(img_dir+image).convert_alpha()