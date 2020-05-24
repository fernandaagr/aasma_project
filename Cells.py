import pygame, os
import constants
import WorldObject
import Company, world, utils, Obstacles


class Cell(pygame.sprite.Sprite):
    """
    Cell and Cells set cells based on .txt with map.
    Use sprite to reset "view" every time agents cross a cell
    """
    def __init__(self, pos, x, y, obs):
        super().__init__()
        #self.pos = pos
        self.x = x
        self.y = y
        self.obstacle = obs

        self.image, self.rect = utils.setImage(self.x, self.y, "cell")

class Cells:
    def __init__(self, world_map, surface):
        super().__init__()
        self.cells = []
        self.surface = surface
        self.obstacles = []
        self.color = constants.SILVER
        self.cp1 = []
        self.cp2 = []
        posCell = 0
        for col, tiles in enumerate(world_map):
            for row, tile in enumerate(tiles):
                if tile == '.' or tile == 'a':
                    posCell+=1
                    #keep this to update sprite when agent cross cell
                    c = Cell(posCell, row, col, obs=False)
                    self.cells.append(c)

                    self.color = constants.SILVER
                    self.setCell(row, col, 'cell', False, False, True, None, '')

                elif tile == 'o':
                    #o = type('obj', (object,), {'x': row, 'y': col})
                    o = Obstacles.Obstacle(row, col)
                    self.obstacles.append(o)

                    self.color = constants.SILVER
                    self.setCell(row, col, 'cell', True, False, False, None, '')
                elif tile == '1':
                    self.color = constants.GRAY
                    cp = Company.Company(row, col, 'cp1')
                    self.cp1.append(cp)
                    self.setCell(row, col, 'cp1', False, False, True, None, '')
                elif tile == '2':
                    self.color = constants.LIGHTLATEGREY
                    cp = Company.Company(row, col, 'cp2')
                    self.cp2.append(cp)
                    self.setCell(row, col, 'cp2', False, False, True, None, '')

    def __getitem__(self, item):
        return self.cells[item]

    def setCell(self, x, y, typeCell, obs=False, delivery=False, isFree=False, marked=None, info=''):
        e = WorldObject.WorldObject(x, y, typeCell, obs, delivery, isFree, marked, info)
        world.objects[x][y] = e

        utils.setRect(x, y, self.surface, self.color)

    def updateCell(self, rand):
        """
        Needed to update view of cell with obstacle (if generted randomly)
        :param rand: random pos to obstacle (rand is the pos on the list of objects of type cell, not on the map)
        """
        pos = self.__getitem__(rand).__dict__.get('pos')
        x = self.__getitem__(rand).__dict__.get('x')
        y = self.__getitem__(rand).__dict__.get('y')

        self.image, self.rect = utils.setImage(x, y, "obs")

        setattr(self.cells[rand], 'obstacle', not self.cells[rand].__dict__.get('obstacle'))
        setattr(self.cells[rand], 'image', self.image)

