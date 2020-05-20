import pygame
import constants
import WorldObject
import world, utils


class Building(pygame.sprite.Sprite):
    def __init__(self, pos, x, y, delivery):
        super().__init__()
        self.x = x
        self.y = y
        self.pos = pos
        self.delivery = delivery

        self.image, self.rect = utils.setImage(self.x, self.y, "building")

    def changeImage(self):
        self.image, self.rect = utils.setImage(self.x, self.y, "building")

class Buildings:
    """
        Set buildings based on .txt with map.
        """
    def __init__(self, world_map, surface):
        super().__init__()
        self.buildings = []
        pos = 0
        for col, tiles in enumerate(world_map):
            for row, tile in enumerate(tiles):
                if tile == 'b':
                    pos+=1
                    b = type('obj', (object,), {'pos': pos, 'x': row, 'y': col, 'delivery': False})
                    #b = Building(pos, row, col, False)
                    self.buildings.append(b)

                    e = WorldObject.WorldObject(row, col, 'building', False, False, '')
                    world.objects[row][col] = e
                    utils.setRect(row, col, surface, constants.DARKSLATEGRAY)

    def __getitem__(self, item):
        return self.buildings[item]



