import pygame, random, time
import constants
import world, utils
import numpy as np


class ProactiveAgent:
    def __init__(self, pos, x, y, company, surface):
        super().__init__()

        self.myWorldMap = np.empty([constants.NUMBER_OF_BLOCKS_WIDE, constants.NUMBER_OF_BLOCKS_HIGH], dtype=object)
        world.World.updateAgentLocation(world.World, self.x, self.y, True)

    def agentDecision(self):
        # if .... :
        #    pass
        # else:
        #    self.agentReactiveDecision()
        pass

    # ------------------------#
    #    REACTIVE BEHAVIOR    #
    # ------------------------#

    def agentReactiveDecision(self):
        self.aheadPosition()
        if self.isLowBattery():
            print("-> {}-{} - Low battery.".format(self.name, self.myCompany))
            self.stopAgent()
            # communicate with company to know what to do;
        elif self.isAgentInFront():
            print("Stoped!Agent in front.")
            self.stopAgent()
        elif self.isHeadQuarters() and not self.prepared and self.battery <= 75:
            print("-> {}-{} headquarters to charge.".format(self.name, self.myCompany))
            self.prepareRecharge()
        elif self.prepared and self.checkTimeIteration():
            print("-> {}-{} ready to charge.".format(self.name, self.myCompany))
            self.recharge()
        elif not self.pause and not self.isWall() and not self.isBuilding() and not self.hasObstacle() and not self.isAgentInFront():
            self.move()
        elif self.isBuilding() and self.hasDelivery() and not self.agentHasDelivery():
            self.pickUpDelivery()
        elif self.isBuilding() and self.agentHasDelivery() and self.isDeliveryPoint():
            self.dropDelivery()
        elif not self.pause and self.isWall() or self.hasObstacle() or self.isBuilding() or not self.isHeadQuarters():
            self.rotate()

    # ------------------------#
    #        ACTUATORS        #
    # ------------------------#

    def move(self):
        world.World.updateAgentLocation(world.World, self.x, self.y, False)
        self.x += self.dx
        self.y += self.dy
        world.World.updateAgentLocation(world.World, self.x, self.y, True)
        self.rect = self.rect.move(self.dx * constants.BLOCK_WIDTH, self.dy * constants.BLOCK_HEIGHT)
        self.battery = self.battery - 1
        print("{}-{} has moved. x,y: {},{}. dx={}, dy={}, battery={}".format(self.name, self.myCompany, self.x,
                                                                             self.y, self.dx, self.dy,
                                                                             self.battery))

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
        self.startD = time.perf_counter()
        entity = world.World.getWorldObject(world.World, (self.x + self.dx), (self.y + self.dy)).__dict__ # get entity in front of agent
        id = entity.get('info')                 # get id of delivery that this entity has. if it has a delivery, the 'info' attribute has its id.
        deli = world.deliveries[id].__dict__    # get delivery - for now, the pos and id are the same

        print("-> {}-{} as delivery: {}. Pp: ({}, {}), Dp:({}, {})".format(self.name, self.myCompany, deli.get('id'), deli.get('x'),
                                                                        deli.get('y'), deli.get('dp_x'), deli.get('dp_y')))

        self.updateAgent(deli.get('id'))    # update agent, so it knows it has a cargo and the id


        world.World.updateDelivery(world.World, deli.get('id'), 'agent', self.name+'-'+self.myCompany)  # update delivery, so it knows which agents is delivering
        world.World.updateBuilding(world.World, deli.get('x'), deli.get('y'))   # update building (remove delivery from it) -> set to false in objects, dont remove from deliveries list

        # change color of building -> didnt work in world.py
        utils.setRect(deli.get('x'), deli.get('y'), self.surface, constants.DARKSLATEGRAY)
        # self.image, self.rect = utils.setImage(self.x, self.y, "dog02")

    def dropDelivery(self):
        print("-> {}-{}: droped delivery.".format(self.name, self.myCompany))
        # update delivery
        world.World.updateDelivery(world.World,self.idDelivery, 'finished', 'True')  # update delivery, so it knows which agents is delivering
        # compute time of delivery
        self.stopD = time.perf_counter()
        pauses = self.checkForPausesInDelivery()
        final = self.stopD - self.startD - pauses
        #print("Times: start={}, stop={}, pauses={}, final={}.".format(self.startD, self.stopD, pauses, final))
        self.dMade.append({'id': self.idDelivery, 'time': final})
        # update agent
        self.updateAgent()
        # self.image, self.rect = utils.setImage(self.x, self.y, "dog")

    def updateMyWorldMap(self):
        pass

    def beliefs(self):
        pass

    def plans(self):
        pass