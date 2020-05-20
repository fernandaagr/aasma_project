import pygame, os, random
import constants
import world, utils


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

        self.image, self.rect = utils.setImage(self.x, self.y, "obs")

# class Obstacle(pygame.sprite.Sprite):
class Obstacles:
    def __init__(self, world_map, surface):
        self.surface = surface
        self.obstacles = []
        self.map = world_map

        #----------------- Static obstacles -----------------#
        for col, tiles in enumerate(self.map):
            for row, tile in enumerate(tiles):
                if tile == 'o':
                    o = type('obj', (object,), {'x': row, 'y': col})
                    #o = Obstacle(row, col)
                    self.obstacles.append(o)

                    world.World.updateWorldObject(world.World, row, col, 'obs', True)
                    #utils.setRect(row, col, surface, constants.MAROON)

        #---------------------------------------------------#

    def generate(self):
        c = random.randint(0, len(self.cells.cells)-1)
        c_keys = self.cells.__getitem__(c).__dict__
        if c_keys.get('obstacle'):
            print("has obstable already")
            self.generate()
        else:
            print("new obstacle at x: {}, y: {}, pos: {}".format(c_keys.get('x'), c_keys.get('y'), c_keys.get('pos')))
            o = type('obj', (object,), {'rand': c, 'pos': c_keys.get('pos'), 'x': c_keys.get('x'), 'y': c_keys.get('y')})
            self.obstacles.append(o)

    def __getitem__(self, item):
        return self.obstacles[item]
