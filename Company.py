import pygame
import os
import constants


class Company(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.x = x
        self.y = y
        self.name = name

        filepath = os.path.join("data", "img", self.name+".png")
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.BLOCK_WIDTH, self.y * constants.BLOCK_HEIGHT)

