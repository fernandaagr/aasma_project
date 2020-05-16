import pygame
import sys, os, random
import constants
import world

class reactiveAgent(pygame.sprite.Sprite):
    def __init__(self, world_map, surface, walls, buildings, obstacles, deliveries):
        super().__init__()
        self.x = -1
        self.y = -1
        self.map = world_map
        self.direction = constants.ROT[0]
        self.rot = 0  # point down
        self.battery = 100

        #
        self.walls = walls
        self.buildings = buildings
        self.obstacles = obstacles
        self.deliveries = deliveries

        self.dx = 0
        self.dy = 0

        #print("Teste: ", world.Buildings.getbuildings(self).__dict__.get('buildings'))
        #t = world.Buildings.getbuildings(self).__dict__.get('buildings')


        #Check .txt for agents. They will always start at the same place (company headquarters) -----> isso vai mudar quando aumentar o número de agents
        for col, tiles in enumerate(self.map):
            for row, tile in enumerate(tiles):
                if tile == 'a':
                    self.x = row
                    self.y = col
                    print("player at: row: {}, col: {}".format(row, col))
            # ---------------------------------------------
        filepath = os.path.join("data", "img", "dog02.png")
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.BLOCK_WIDTH, self.y * constants.BLOCK_HEIGHT)

    # ------------------------#
    #      AGENT DECISION     #
    # ------------------------#
    #Decisão do agent deve ser mais ou menos assim.
    def agentDecision(self):
        self.aheadPosition()
        if not self.isWall() and not self.isBuilding() and not self.hasObstacle():
            self.move()
        elif self.isBuilding() and self.hasDelivery():
            self.pickUpDelivery()
        elif self.hasObstacle() or self.isBuilding():
            self.rotate()

    def aheadPosition(self):
        self.dx = 0
        self.dy = 0
        #Deal with agents direction/orientation to where agent should move to
        if self.direction == constants.ROT[0]:
            self.dy = 1
        elif self.direction == constants.ROT[1]:
            self.dy = -1
        elif self.direction == constants.ROT[2]:
            self.dx = 1
        elif self.direction == constants.ROT[3]:
            self.dx = -1

    #------------------------#
    #        ACTUATORS       #
    #------------------------#
    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.rect = self.rect.move(self.dx * constants.BLOCK_WIDTH, self.dy * constants.BLOCK_HEIGHT)
        self.battery -= 1
        print("Player has moved. x,y: {},{}. dx={}, dy={}, battery={}".format(self.x, self.y, self.dx, self.dy, self.battery))


    def rotate(self):
        new_rot = random.randint(0, 3)#used to rotate to a random direction everytime
        rot_angle = 0
        if self.direction == constants.ROT[0] and new_rot == 1 or self.direction == constants.ROT[1] and new_rot == 0 or \
                self.direction == constants.ROT[2] and new_rot == 3 or self.direction == constants.ROT[3] and new_rot == 2:
            rot_angle = 180
            self.direction = constants.ROT[new_rot]
        elif self.direction == constants.ROT[0] and new_rot == 2 or self.direction == constants.ROT[1] and new_rot == 3 or \
                self.direction == constants.ROT[2] and new_rot == 1 or self.direction == constants.ROT[3] and new_rot == 0:
            rot_angle = 90
            self.direction = constants.ROT[new_rot]
        elif self.direction == constants.ROT[0] and new_rot == 3 or self.direction == constants.ROT[1] and new_rot == 2 or \
            self.direction == constants.ROT[2] and new_rot == 0 or self.direction == constants.ROT[3] and new_rot == 1:
            rot_angle = -90
            self.direction = constants.ROT[new_rot]

        self.image = pygame.transform.rotate(self.image, rot_angle)

    def pickUpDelivery(self):
        print("pickup delivery")
        pos = self.buildings.getPos(self.x+self.dx, self.y+self.dy, self.buildings)         # get pos of building in front of agent
        keys = self.buildings.__getitem__(pos).__dict__                                     # still from building
        id = keys.get('id_delivery')                                                        # get id of delivery that this building has
        delivery = self.deliveries.__getitem__(id).__dict__.get('deliveries')[0].__dict__   # get delivery -> to messy change it later
        #delivery = d.get('deliveries')[0].__dict__
        print("agent as delivery: {}. Pp: {}, Dp:{}".format(delivery.get('id_delivery'), delivery.get('pos'), delivery.get('dp_pos')))

        #update agent
        #update building (remove delivery from it)

        pass

    def dropDelivery(self):
        pass


    #------------------------#
    #         SENSORS        #
    #------------------------#

    def isWall(self):
        for wall in self.walls:
            if wall.x == self.x + self.dx and wall.y == self.y + self.dy:
                return True
        return False

    def isBuilding(self):
        for b in self.buildings:
            if b.x == self.x + self.dx and b.y == self.y + self.dy:
                return True
        return False

    def hasDelivery(self):
        pos = self.buildings.getPos(self.x + self.dx, self.y + self.dy, self.buildings)  # get the position of the building to check  if it has a delivery
        current = self.buildings.__getitem__(pos)
        keys = current.__dict__
        if keys.get('delivery') == True:
            print("has delivery")
            return True
        else:
            return False

    def hasObstacle(self):
        for b in self.obstacles:
            if b.x == self.x + self.dx and b.y == self.y + self.dy:
                print("obstacle ahead, rotate")
                return True
        return False

    def agentHasDelivery(self):
        return False


    #def hasObstacle(self, dx, dy, cells):
    #    pos = cells.getPos(self.x, self.y, cells)
    #    current = cells.__getitem__(pos)
    #    keys = current.__dict__
    #    # print(keys)
    #    if keys.get('obstacle') == True:
    #        print("obstacle ahead")
    #        return True
    #    else:
    #        return False