import pygame
import sys, os, random
import constants
from reactiveAgent import reactiveAgent
import worldObjects

class World:
    def __init__(self):

        self.start = False
        self.paused = False
        #init
        pygame.init()
        pygame.display.set_caption("Delivery World")
        self.all_sprites = pygame.sprite.Group()
        self.display_surface = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.display_surface.fill(constants.LIGHTBLUE)


        self.map = self.readMap(constants.MAPFILE)
        self.steps = pygame.time.get_ticks()
        self.cells = Cells(self.map, self.display_surface)
        self.walls = Walls(self.map, self.display_surface)
        self.buildings = Buildings(self.map, self.display_surface)

        self.agent = reactiveAgent(self.map, self.display_surface)

        self.drawGrid()

    def agentMove(self):
        if random.random() <= 0.8:
            self.agent.move(walls=self.walls, buildings=self.buildings)
        else:
            self.agent.rotate()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.key == pygame.K_SPACE:
                    self.start = not self.start



    def readMap(self, mapfile):
        with open(mapfile, 'r') as f:
            world_map = f.readlines()
        world_map = [line.strip() for line in world_map]
        return world_map

    def drawGrid(self):
        for i in range(constants.NUMBER_OF_BLOCKS_WIDE):
            new_height = round(i * constants.BLOCK_HEIGHT)
            new_width = round(i * constants.BLOCK_WIDTH)
            pygame.draw.line(self.display_surface, constants.LIGHTGREY, (0, new_height), (constants.SCREEN_WIDTH, new_height), 2)
            pygame.draw.line(self.display_surface, constants.LIGHTGREY, (new_width, 0), (new_width, constants.SCREEN_HEIGHT), 2)

    def updateClasses(self):
        for elem in self.cells:
            self.all_sprites.add(elem)
        self.all_sprites.add(self.agent)

    def drawAgents(self):
        self.all_sprites.update()
        #self.display_surface.fill((0,0,0))
        self.all_sprites.draw(self.display_surface)


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        filepath = os.path.join("data\img\cell.png")
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.BLOCK_WIDTH, self.y * constants.BLOCK_HEIGHT)


class Cells:
    def __init__(self, world_map, surface):
        super().__init__()
        self.cells = []
        self.map = world_map

        for col, tiles in enumerate(world_map):
            for row, tile in enumerate(tiles):
                if tile == '.' or tile == 'a':
                    c = Cell(row, col)
                    #c = type('obj', (object,), {'x': row, 'y': col})
                    self.cells.append(c)
                    myrect = pygame.Rect(row*constants.BLOCK_WIDTH, col*constants.BLOCK_HEIGHT, constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
                    pygame.draw.rect(surface, constants.SILVER, myrect)
                    #print("row: {}, col: {}".format(row, col))

    def __getitem__(self, item):
        return self.cells[item]


class Walls:
    def __init__(self, world_map, surface):
        super().__init__()
        self.walls = []
        self.map = world_map

        for col, tiles in enumerate(world_map):
            for row, tile in enumerate(tiles):
                if tile == 'w':
                    w = type('obj', (object,), {'x': row, 'y': col})
                    self.walls.append(w)
                    myrect = pygame.Rect(row * constants.BLOCK_WIDTH, col * constants.BLOCK_HEIGHT,
                                         constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
                    pygame.draw.rect(surface, constants.BLACK, myrect)
                    #print("row: {}, col: {}".format(row, col))

    def __getitem__(self, item):
        return self.walls[item]


class Buildings:
    def __init__(self, world_map, surface):
        super().__init__()
        self.buildings = []
        self.map = world_map

        for col, tiles in enumerate(world_map):
            for row, tile in enumerate(tiles):
                if tile == 'b':
                    b = type('obj', (object,), {'x': row, 'y': col})
                    self.buildings.append(b)
                    myrect = pygame.Rect(row * constants.BLOCK_WIDTH, col * constants.BLOCK_HEIGHT,
                                         constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
                    pygame.draw.rect(surface, constants.DARKSLATEGRAY, myrect)
                    #print("row: {}, col: {}".format(row, col))

    def __getitem__(self, item):
        return self.buildings[item]


