import pygame
import sys, os, random
import constants
from reactiveAgent import reactiveAgent
from worldObjects import Deliveries, Obstacles
import Entity
import numpy as np

objects = np.empty([constants.NUMBER_OF_BLOCKS_WIDE, constants.NUMBER_OF_BLOCKS_HIGH], dtype=object)
deliveries = []
pos = 0
class World:
    """
    Init world.
    """
    def __init__(self):
        self.start = False
        self.paused = False
        #---------- Init Interface ----------#
        pygame.init()
        pygame.display.set_caption("Delivery World")
        self.all_sprites = pygame.sprite.Group()
        self.display_surface = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.display_surface.fill(constants.LIGHTBLUE)

        #self.map = self.readMap(constants.MAPS[random.randint(0, 2)])
        self.map = self.readMap(constants.MAPFILE)

        #---------- Init world and objects ----------#
        #cells, walls, buildings, obstacles and agents position come from map_delivery.txt
        self.cells = Cells(self.map, self.display_surface)
        self.walls = Walls(self.map, self.display_surface)
        self.buildings = Buildings(self.map, self.display_surface)

        self.deliveries = []
        for i in range(0, 4):
            print("{})".format(i))
            d = Deliveries(self.buildings, self.display_surface)    # get new delivery
            setattr(d.__dict__.get('deliveries')[0], 'id_delivery', i) # add id to it
            #self.deliveries.append(d)
            #p = d.__dict__.get('deliveries')[0].__dict__.get('pos')
            #self.buildings.updateDel(p, i)

            # get delivery keys and values
            delivery = d.__dict__.get('deliveries')[0].__dict__
            x = delivery.get('x')
            y = delivery.get('y')

            # update buildings with delivery and id of delivery
            self.updateEntity(x, y, 'delivery', True)
            self.updateEntity(x, y, 'info', delivery.get('id_delivery'))

            # auxiliar list with deliveries
            dd = type('obj', (object,), {'x': x, 'y': y, 'dp_x': delivery.get('dp_x'), 'dp_y': delivery.get('dp_y'),
                                         'id': delivery.get('id_delivery'), 'finished': False, 'agent': None})
            deliveries.append(dd)


        #create static obstacles
        #self.obstacles = Obstacles(self.map, self.display_surface)

        #----------- create obstacles randomly ---------------------#
        #self.obstacles = Obstacle(self.cells, self.display_surface)
        #for i in range(len(self.obstacles.obstacles)):
        #    rand = self.obstacles.__getitem__(i).__dict__.get('rand')
        #    pos = self.obstacles.__getitem__(i).__dict__.get('pos')
        #    x = self.obstacles.__getitem__(i).__dict__.get('x')
        #    y = self.obstacles.__getitem__(i).__dict__.get('y')

        #    self.cells.updateCell(rand)
        # -----------------------------------------------------------#

        self.agent = reactiveAgent(0, 1, 1, self.display_surface)
        print("Agent: ", self.agent.__dict__)

        self.drawGrid()

    def getEntity(self, x, y):
        return objects[x][y];

    def updateEntity(self, x, y, attr, value):
        print("updated entity")
        setattr(objects[x][y], attr, value)

    def updateDelivery(self, p, attr, value):
        print("updated delivery")
        setattr(deliveries[p], attr, value)
        print(deliveries[p].__dict__)

    def updateBuilding(self, x, y):
        print("update building")
        setattr(objects[x][y], 'delivery', not objects[x][y].__dict__.get('delivery'))
        # myrect = pygame.Rect(x * constants.BLOCK_WIDTH, y * constants.BLOCK_HEIGHT,
        #                     constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
        # pygame.draw.rect(self.display_surface, constants.DARKSLATEGRAY, myrect)


    # depois mudar isto. Quando o "jogo" começar esperar o user clicar para iniciar.
    def reactiveAgentDecision(self):
        """
        Agent movement on game loop.
        Based on a random prop will rotate even if does not colide with anything.

        ->agentDecision() deve vir aqui<-

        :parameters -> used in agents sensors
        """
        r = random.random()
        if r <= 0.8:
            self.agent.agentDecision()
        else:
            self.agent.rotate()

    def handleEvents(self):
        """
        Handle events when press keys.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           # press ESC to quit the program
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:     # SPACE to start/stop agent
                    self.start = not self.start

    def readMap(self, mapfile):
        """
        Read .txt file with map.
        :param mapfile: path to file
        :return:
        """
        with open(mapfile, 'r') as f:
            world_map = f.readlines()
        world_map = [line.strip() for line in world_map]
        return world_map

    def drawGrid(self):
        """
        Draw grid to better see movement. FIX.
        """
        for i in range(constants.NUMBER_OF_BLOCKS_WIDE):
            new_height = round(i * constants.BLOCK_HEIGHT)
            new_width = round(i * constants.BLOCK_WIDTH)
            pygame.draw.line(self.display_surface, constants.LIGHTGREY, (0, new_height), (constants.SCREEN_WIDTH, new_height), 2)
            pygame.draw.line(self.display_surface, constants.LIGHTGREY, (new_width, 0), (new_width, constants.SCREEN_HEIGHT), 2)

    def updateClasses(self):
        """
        Update sprites of interface.
        """
        for elem in self.cells:
            self.all_sprites.add(elem)

        #for elem in self.obstacles:
        #    self.all_sprites.add(elem)

        self.all_sprites.add(self.agent)

    def drawAgents(self):
        self.all_sprites.update()
        self.all_sprites.draw(self.display_surface)

    def getbuildings(self):
        return self.buildings


class Cell(pygame.sprite.Sprite):
    """
    Cell and Cells set cells based on .txt with map.
    Use sprite to reset "view" every time agents cross a cell
    """
    def __init__(self, pos, x, y, obs):
        super().__init__()
        self.pos = pos
        self.x = x
        self.y = y
        self.obstacle = obs
        filepath = os.path.join("data", "img", "cell.png")
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.BLOCK_WIDTH, self.y * constants.BLOCK_HEIGHT)


class Cells:
    def __init__(self, world_map, surface):
        super().__init__()
        self.cells = []
        self.map = world_map
        self.surface = surface
        self.agents = []
        self.obstacles = []
        posCell = 0
        for col, tiles in enumerate(world_map):
            for row, tile in enumerate(tiles):
                if tile == '.' or tile == 'a':
                    posCell+=1
                    global pos
                    pos+=1
                    c = Cell(posCell, row, col, obs=False)
                    #c = type('obj', (object,), {'x': row, 'y': col})
                    self.cells.append(c)

                    e = Entity.Entity(pos, row, col, 'cell', False, False, '')
                    #objects.append(e)
                    objects[row][col] = e
                    myrect = pygame.Rect(row*constants.BLOCK_WIDTH, col*constants.BLOCK_HEIGHT, constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
                    pygame.draw.rect(surface, constants.SILVER, myrect)
                    #print("row: {}, col: {}".format(row, col))

                if tile == 'o':
                    o = type('obj', (object,), {'x': row, 'y': col})
                    #o = Obstacle(row, col)
                    self.obstacles.append(o)

                    e = Entity.Entity(pos, row, col, 'cell', True, False, '')
                    # objects.append(e)
                    objects[row][col] = e
                    #print(world.World.updateEntity(row, col, 'cell'))
                    #world.World.updateEntity(world.World, row, col, 'obs', True)
                    myrect = pygame.Rect(row * constants.BLOCK_WIDTH, col * constants.BLOCK_HEIGHT,
                                         constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
                    pygame.draw.rect(surface, constants.MAROON, myrect)

    def __getitem__(self, item):
        return self.cells[item]

    def updateCell(self, rand):
        """
        Needed to update view of cell with obstacle (if generted randomly)
        :param rand: random pos to obstacle (rand is the pos on the list of objects of type cell, not on the map)
        """
        pos = self.__getitem__(rand).__dict__.get('pos')
        x = self.__getitem__(rand).__dict__.get('x')
        y = self.__getitem__(rand).__dict__.get('y')

        filepath = os.path.join("data", "img", "obs.png")
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * constants.BLOCK_WIDTH, y * constants.BLOCK_HEIGHT)

        setattr(self.cells[rand], 'obstacle', not self.cells[rand].__dict__.get('obstacle'))
        setattr(self.cells[rand], 'image', self.image)

class Walls:
    """
    Set walls based on .txt with map. Always the same.
    """
    def __init__(self, world_map, surface):
        super().__init__()
        self.walls = []
        self.map = world_map

        for col, tiles in enumerate(world_map):
            for row, tile in enumerate(tiles):
                if tile == 'w':
                    w = type('obj', (object,), {'x': row, 'y': col})
                    self.walls.append(w)

                    e = Entity.Entity(None, row, col, 'wall', False, False, '')
                    # objects.append(e)
                    objects[row][col] = e
                    myrect = pygame.Rect(row * constants.BLOCK_WIDTH, col * constants.BLOCK_HEIGHT,
                                         constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
                    pygame.draw.rect(surface, constants.BLACK, myrect)
                    #print("row: {}, col: {}".format(row, col))

    def __getitem__(self, item):
        return self.walls[item]

class Buildings:
    """
        Set buildings based on .txt with map.
        """
    def __init__(self, world_map, surface):
        super().__init__()
        self.buildings = []
        self.map = world_map

        posBuil = 0
        for col, tiles in enumerate(world_map):
            for row, tile in enumerate(tiles):
                if tile == 'b':
                    b = type('obj', (object,), {'pos': posBuil, 'x': row, 'y': col, 'delivery': False})
                    posBuil+=1
                    global pos
                    pos += 1
                    self.buildings.append(b)

                    e = Entity.Entity(pos, row, col, 'building', False, False, '')
                    #objects.append(e)
                    objects[row][col] = e
                    myrect = pygame.Rect(row * constants.BLOCK_WIDTH, col * constants.BLOCK_HEIGHT,
                                         constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
                    pygame.draw.rect(surface, constants.DARKSLATEGRAY, myrect)
                    #print("row: {}, col: {}".format(row, col))

    def __getitem__(self, item):
        return self.buildings[item]


    def getPos(self, x, y, buildings):
        """
        Get pos of the building given coordinates.
        """
        for i in range(len(buildings.buildings)):
            current = buildings.__getitem__(i).__dict__
            if current.get('x') == x and current.get('y') == y:
                return current.get('pos')
                break
            else:
                pass
        return 0

    def updateDel(self, p, id_delivery):
        """
        Update building cell if its has delivery. Just change the color for now.
        :param pos: pos of delivery (in which building)
        :return:
        """
        setattr(self.buildings[p], 'delivery', not self.__getitem__(p).__dict__.get('delivery'))
        setattr(self.buildings[p], 'id_delivery', id_delivery)


