import pygame
import sys, os, random
import constants
import world

class reactiveAgent(pygame.sprite.Sprite):


    def __init__(self, pos, x, y, surface):
        super().__init__()
        self.x = x
        self.y = y
        self.pos = pos
        self.dx = 0
        self.dy = 0

        self.direction = constants.ROT[0]
        self.rot = 0  # point down
        self.surface = surface

        self.battery = 100
        self.hasCargo = False
        self.idDelivery = None

        print("player at: row: {}, col: {}".format(self.x, self.y))
        print("Agent: hasCargo={}, idDelivery={}".format(self.hasCargo, self.idDelivery))

        #Check .txt for agents. They will always start at the same place (company headquarters) -----> isso vai mudar quando aumentar o número de agents
        #for col, tiles in enumerate(self.map):
        #    for row, tile in enumerate(tiles):
        #        if tile == 'a':
        #            self.x = row
        #            self.y = col
        #            print("player at: row: {}, col: {}".format(row, col))
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
        elif self.isBuilding() and self.hasDelivery() and not self.agentHasDelivery():
            self.pickUpDelivery()
        elif self.isBuilding() and self.agentHasDelivery() and self.isDeliveryPoint():
            self.dropDelivery()
        elif self.isWall() or self.hasObstacle() or self.isBuilding():
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
        # new
        entity = world.World.getEntity(world.World, (self.x + self.dx), (self.y + self.dy)).__dict__ # get entity in front of agent
        id = entity.get('info')                 # get id of delivery that this entity has. if it has a delivery, the 'info' attribute has its id.
        deli = world.deliveries[id].__dict__    # get delivery - for now, the pos and id are the same

        print("agent as delivery: {}. Pp: ({}, {}), Dp:({}, {})".format(deli.get('id'), deli.get('x'), deli.get('y'),
                                                            deli.get('dp_x'), deli.get('dp_y')))

        self.updateAgent(deli.get('id'))    # update agent, so it knows it has a cargo and the id
        world.World.updateDelivery(world.World, deli.get('id'), 'agent', 'A1')  # update delivery, so it knows which agents is delivering
        world.World.updateBuilding(world.World, deli.get('x'), deli.get('y'))   # update building (remove delivery from it) -> set to false in objects, dont remove from deliveries list

        # change color of building -> didnt work in world.py
        myrect = pygame.Rect(deli.get('x') * constants.BLOCK_WIDTH, deli.get('y') * constants.BLOCK_HEIGHT,
                             constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
        pygame.draw.rect(self.surface, constants.DARKSLATEGRAY, myrect)

    def dropDelivery(self):
        print("drop delivery")
        # update delivery
        world.World.updateDelivery(world.World,self.idDelivery, 'finished', 'True')  # update delivery, so it knows which agents is delivering
        # update agent
        self.updateAgent()

    def updateAgent(self, idDelivery=None):
        self.hasCargo = not self.hasCargo
        self.idDelivery = idDelivery

        print("Agent updated: hasCargo={}, idDelivery={}".format(self.hasCargo, self.idDelivery))


    #------------------------#
    #         SENSORS        #
    #------------------------#

    def isWall(self):
        return world.World.getEntity(world.World, (self.x + self.dx),
                                     (self.y + self.dy)).__dict__.get('type') == 'wall'

    def isBuilding(self):
        return world.World.getEntity(world.World, (self.x + self.dx),
                                     (self.y + self.dy)).__dict__.get('type') == 'building'

    def hasDelivery(self):
        entity = world.World.getEntity(world.World, (self.x + self.dx), (self.y + self.dy)).__dict__
        if entity.get('delivery'):
            print('has delivery')
            return True
        else:
            return False

    def hasObstacle(self):
        entity = world.World.getEntity(world.World, (self.x + self.dx), (self.y + self.dy)).__dict__
        if entity.get('type') == 'cell' and entity.get('obs'):
            print("obstacle")
            return True
        else:
            return False
        # return entityType == 'cell' and hasObs

    def agentHasDelivery(self):
        return self.hasCargo

    def isDeliveryPoint(self):
        entity = world.deliveries[self.idDelivery].__dict__
        if self.x+self.dx == entity.get('dp_x') and self.y+self.dy == entity.get('dp_y'):
            return True
        else:
            return False


