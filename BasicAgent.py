import pygame, random, time
import constants
import world, utils

class BasicAgent:
    def __init__(self, pos, x, y, company, surface):
        super().__init__()

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
        entity = world.World.getWorldObject(world.World, (self.x + self.dx), (self.y + self.dy)).__dict__ # get entity in front of agent
        id = entity.get('info')                 # get id of delivery that this entity has. if it has a delivery, the 'info' attribute has its id.
        deli = world.deliveries[id].__dict__    # get delivery - for now, the pos and id are the same

        print("{}-{} as delivery: {}. Pp: ({}, {}), Dp:({}, {})".format("A1", self.myCompany, deli.get('id'), deli.get('x'),
                                                                        deli.get('y'), deli.get('dp_x'), deli.get('dp_y')))

        self.updateAgent(deli.get('id'))    # update agent, so it knows it has a cargo and the id
        world.World.updateDelivery(world.World, deli.get('id'), 'agent', 'A1-'+self.myCompany)  # update delivery, so it knows which agents is delivering
        world.World.updateBuilding(world.World, deli.get('x'), deli.get('y'))   # update building (remove delivery from it) -> set to false in objects, dont remove from deliveries list

        # change color of building -> didnt work in world.py
        utils.setRect(deli.get('x'), deli.get('y'), self.surface, constants.DARKSLATEGRAY)

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

    def rotate180(self):
        if self.direction == constants.ROT[0]:
            self.direction = constants.ROT[1]
        elif self.direction == constants.ROT[1]:
            self.direction = constants.ROT[0]
        elif self.direction == constants.ROT[2]:
            self.direction = constants.ROT[3]
        elif self.direction == constants.ROT[3]:
            self.direction = constants.ROT[2]

        self.aheadPosition()
        self.image = pygame.transform.rotate(self.image, 180)

    def stopAgent(self):
        self.rot = 0
        self.rect = self.rect.move(0 * constants.BLOCK_WIDTH, 0 * constants.BLOCK_HEIGHT)
        print("Agent stoped. Battery level: {}".format(self.battery))
        self.pause = not self.pause

    def prepareRecharge(self):
        print("prepare to recharge")
        self.move()
        self.rotate180()
        self.stopAgent()
        self.prepared = not self.prepared

    def recharge(self):
        print("recharge")
        self.battery = 100
        self.pause = not self.pause
        self.prepared = not self.prepared

    def checkTimeIteration(self):
        if self.count == 0:
            self.count = 10
            return True
        else:
            current = time.perf_counter()
            #t = current - world.World.getTime(world.World)
            self.count -= 1
            return False
    #------------------------#
    #         SENSORS        #
    #------------------------#

    def getBattery(self):
        return self.battery

    def isWall(self):
        return world.World.getWorldObject(world.World, (self.x + self.dx),
                                     (self.y + self.dy)).__dict__.get('type') == 'wall'

    def isBuilding(self):
        return world.World.getWorldObject(world.World, (self.x + self.dx),
                                     (self.y + self.dy)).__dict__.get('type') == 'building'

    def hasDelivery(self):
        entity = world.World.getWorldObject(world.World, (self.x + self.dx), (self.y + self.dy)).__dict__
        if entity.get('delivery'):
            print('has delivery')
            return True
        else:
            return False

    def hasObstacle(self):
        entity = world.World.getWorldObject(world.World, (self.x + self.dx), (self.y + self.dy)).__dict__
        if entity.get('type') == 'cell' and entity.get('obs'):
            #print("obstacle")
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

    def isLowBattery(self):
        return self.battery <= 25

    def isHeadQuarters(self):
        entity = world.World.getWorldObject(world.World, (self.x + self.dx), (self.y + self.dy)).__dict__
        if entity.get('type') == self.myCompany:
            #self.battery+=10
            return True
        else:
            return False
