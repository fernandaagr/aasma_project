import pygame, os, random
import constants, utils, world

class Deliveries:
    def __init__(self, buildings, surface):
        self.buildings = buildings
        self.surface = surface
        self.deliveries = []

        self.generate()

    def generateRand(self):
        pp, dp = random.sample(range(0, len(self.buildings.buildings) - 1), 2)
        pp_keys = self.buildings.__getitem__(pp).__dict__
        if pp_keys.get('delivery'):
            pp, dp = self.generateRand()
            return pp, dp
        else:
            return pp, dp

    def generate(self):
        pp, dp = self.generateRand()
        pp_keys = self.buildings.__getitem__(pp).__dict__
        dp_keys = self.buildings.__getitem__(dp).__dict__
        print("- New delivery at x: {}, y: {}, pos={}.".format(pp_keys.get('x'), pp_keys.get('y'), pp))
        print("- Drop point: x:{}, y:{}, pos={}".format(dp_keys.get('x'), dp_keys.get('y'), dp_keys.get('pos')))

        d = type('obj', (object,), {'pos': pp, 'x': pp_keys.get('x'), 'y': pp_keys.get('y'),
                                    'dp_pos': dp_keys.get('pos'), 'dp_x': dp_keys.get('x'), 'dp_y': dp_keys.get('y')})

        self.deliveries.append(d)

        setattr(self.buildings.__getitem__(pp), 'delivery', not self.buildings.__getitem__(pp).__dict__.get('delivery'))
        utils.setRect(pp_keys.get('x'), pp_keys.get('y'), self.surface, constants.MAROON)

    def __getitem__(self, item):
        return self.deliveries[item]

