import pygame
import sys, os, random
import constants
import world

class Delivery():
    def __init__(self, buildings, surface):
        self.buildings = buildings
        self.surface = surface
        self.deliveries = []

        d = random.randint(0, len(self.buildings.buildings) - 1)
        d_keys = self.buildings.__getitem__(d).__dict__
        if d_keys.get('delivery') == True:
            print("has delivery already")
            self.generate()
        else:
            for i in range(0, 4):
                self.generate()

    def generate(self):
        d = random.randint(0, len(self.buildings.buildings) - 1)
        d_keys = self.buildings.__getitem__(d).__dict__
        if d_keys.get('delivery') == True:
            print("has delivery already")
            self.generate()
        else:
            print("new delivery at x: {}, y: {}".format(d_keys.get('x'), d_keys.get('y')))
            d = type('obj', (object,), {'pos': d, 'x': d_keys.get('x'), 'y': d_keys.get('y')})
            self.deliveries.append(d)
            myrect = pygame.Rect(d_keys.get('x') * constants.BLOCK_WIDTH, d_keys.get('y') * constants.BLOCK_HEIGHT,
                                 constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
            pygame.draw.rect(self.surface, constants.LIGHTSALMON, myrect)

    def __getitem__(self, item):
        return self.deliveries[item]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, cells, surface):
        self.surface = surface
        self.cells = cells
        self.obstacles = []

        for i in range(0, 3):
            self.generate()

    def generate(self):
        c = random.randint(0, len(self.cells.cells)-1)
        c_keys = self.cells.__getitem__(c).__dict__
        if c_keys.get('obstacle') == True:
            print("has obstable already")
            self.generate()
        else:
            print("new obstacle at x: {}, y: {}, pos: {}".format(c_keys.get('x'), c_keys.get('y'), c_keys.get('pos')))
            o = type('obj', (object,), {'rand': c, 'pos': c_keys.get('pos'), 'x': c_keys.get('x'), 'y': c_keys.get('y')})
            self.obstacles.append(o)
            #myrect = pygame.Rect(c_keys.get('x') * constants.BLOCK_WIDTH, c_keys.get('y') * constants.BLOCK_HEIGHT,
            #                     constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
            #pygame.draw.rect(self.surface, constants.MAROON, myrect)

    def __getitem__(self, item):
        return self.obstacles[item]



