import pygame
import sys, os, random
import constants
import world

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
        print("new delivery at x: {}, y: {}, pos={}.".format(pp_keys.get('x'), pp_keys.get('y'), pp))
        print("Drop point: x:{}, y:{}, pos={}".format(dp_keys.get('x'), dp_keys.get('y'), dp_keys.get('pos')))

        d = type('obj', (object,), {'pos': pp, 'x': pp_keys.get('x'), 'y': pp_keys.get('y'),
                                    'dp_pos': dp_keys.get('pos'), 'dp_x': dp_keys.get('x'), 'dp_y': dp_keys.get('y')})
        #print(d.__dict__)
        self.deliveries.append(d)
        myrect = pygame.Rect(pp_keys.get('x') * constants.BLOCK_WIDTH, pp_keys.get('y') * constants.BLOCK_HEIGHT,
                             constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
        pygame.draw.rect(self.surface, constants.LIGHTSALMON, myrect)


    def __getitem__(self, item):
        return self.deliveries[item]


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        filepath = os.path.join("data", "img", "obs.png")
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.BLOCK_WIDTH, self.y * constants.BLOCK_HEIGHT)

#class Obstacle(pygame.sprite.Sprite):
class Obstacles:
    #def __init__(self, cells, surface):
    def __init__(self, world_map, surface):
        self.surface = surface
        #self.cells = cells
        self.obstacles = []
        self.map = world_map

        #----------------- Static obstacles -----------------#
        for col, tiles in enumerate(self.map):
            for row, tile in enumerate(tiles):
                if tile == 'o':
                    o = type('obj', (object,), {'x': row, 'y': col})
                    #o = Obstacle(row, col)
                    self.obstacles.append(o)
                    #print(world.World.updateEntity(row, col, 'cell'))
                    world.World.updateEntity(world.World, row, col, 'obs', True)
                    myrect = pygame.Rect(row * constants.BLOCK_WIDTH, col * constants.BLOCK_HEIGHT,
                                         constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
                    pygame.draw.rect(surface, constants.MAROON, myrect)

        #---------------------------------------------------#
        #for i in range(0, 3):
        #    self.generate()

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



