import pygame, random, time
import constants
import world, utils
import numpy as np


class ProactiveAgent(pygame.sprite.Sprite):
    tic = 0
    toc = 0
    def __init__(self, x, y, company, surface, name, id):
        super().__init__()
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        # initial position pointing left
        self.direction = constants.ROT[2]
        self.surface = surface
        self.name = name
        self.battery = 50
        self.hasCargo = False
        self.idDelivery = None
        self.myCompany = company
        self.dMade = []
        self.startD = 0
        self.stopD = 0
        self.pause = False
        self.prepared = False
        self.pausedDelivering = []
        self.count = 10  # equilave a 10 iterações ~=1.4189 segundos --> to recharge
        # self.count = 100  # equilave a 100 iterações ~=10 * 1.4189 segundos
        self.image, self.rect = utils.setImage(self.x, self.y, "dogp")
        self.image = pygame.transform.rotate(self.image, -90)
        self.myId = id
        world.World.updateAgentLocation(world.World, self.x, self.y, True)

        print("-> {} at: row: {}, col: {}".format(self.name, self.x, self.y))
        print("-> {}: hasCargo={}, idDelivery={}".format(self.name, self.hasCargo, self.idDelivery))

        self.myWorldMap = np.full([constants.NUMBER_OF_BLOCKS_WIDE, constants.NUMBER_OF_BLOCKS_HIGH], "_")
        self.buildingsDetected = np.empty([constants.NUMBER_OF_BLOCKS_WIDE, constants.NUMBER_OF_BLOCKS_HIGH],
                                          dtype=object)
        self.movingTo = False
        self.path = []
        self.unable = False

    def agentDecision(self):
        self.aheadPosition()
        self.updateMyWorldMap()
        if not self.agentHasDelivery():
            self.agentReactiveDecision()
        else :
            path, dx, dy = world.World.askCompanyWhatToDo(world.World, self.myId)
            self.actionToPerform(path, dx, dy)
            self.agentProActiveDecision()
            pass

    # ------------------------#
    #    REACTIVE BEHAVIOR    #
    # ------------------------#

    def agentReactiveDecision(self):
        if self.isLowBattery():
            print("-> {}-{} - Low battery.".format(self.name, self.myCompany))
            self.stopAgent()
            # communicate with company to know what to do;
            path, dx, dy = world.World.askCompanyWhatToDo(world.World, self.myId)
            self.actionToPerform(path, dx, dy)
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
        #elif self.isBuilding() and self.agentHasDelivery() and self.isDeliveryPoint():
            #self.dropDelivery()
        elif not self.pause and self.isWall() or self.hasObstacle() or self.isBuilding() or not self.isHeadQuarters():
            self.rotate()

     # ------------------------#
    #    PROACTIVE BEHAVIOR    #
    # ------------------------#

    def agentProActiveDecision(self):
        print("CHEGUEI!")
        print(self.movingTo)
        print(len(self.path))
        if self.movingTo and len(self.path) > 0:
            print("moving")
            print(len(self.path))
            self.path.pop()

            print(len(self.path))
            point = self.path[0]
            x, y = point

            self.checkDirectionOfPoints(x, y)
            print("{}, {}, {}".format(self.dx, self.dy, self.direction))
            if not self.pause and not self.isWall() and not self.isBuilding() and not self.hasObstacle() and not self.isAgentInFront():
                # check this because of unknown cells and to avoid objects
                print("deve mover aqui")
                point = self.path.pop(0)
                print("move to: {}".format(point))
                self.moveToCoords(point)
            elif self.isBuilding() and self.isDeliveryPoint():
                print("drop")
                self.dropDelivery()
                self.path.pop(0)
                self.path = []
                self.movingTo = not self.movingTo
            elif not self.pause and self.isWall() or self.hasObstacle() or self.isBuilding():
                print("deve desviar")
                self.movingTo = False
                self.path = []
                self.rotate()
            else:
                print("else")   # cai aqui pq o primeiro da lista é sempre a posição atual
        elif self.movingTo and not self.path:
            print("empty")
            self.movingTo = False
        elif self.unable:
            print("[{}] - Unable to continue.".format(self.name))
            pass

    # ------------------------#
    #        ACTUATORS        #
    # ------------------------#
    def moveToCoords(self, point):
        world.World.updateAgentLocation(world.World, self.x, self.y, False)
        (x, y) = point
        self.checkDirectionOfPoints(x, y)     # check the current point and update self.dx and self.dy
        self.x += self.dx   # agent moves
        self.y += self.dy
        world.World.updateAgentLocation(world.World, self.x, self.y, True)
        self.rect = self.rect.move(self.dx * constants.BLOCK_WIDTH, self.dy * constants.BLOCK_HEIGHT)
        self.battery = self.battery - 1
        print("[{}] has moved. x,y: {},{}. dx={}, dy={}, battery={}".format(self.name, self.x, self.y, self.dx, self.dy,self.battery))

    def checkDirectionOfPoints(self, coordx, coordy):
        """
        Check the next coord points to see in which direction the agent should move.
        Update dx and dy based on the new values.
        :param coordx and coordy: next (x, y) coords.
        """
        if coordx < self.x:     # left
            self.dx = -1
            self.direction = constants.ROT[2]
        elif coordx > self.x:   # right
            self.dx = 1
            self.direction = constants.ROT[3]
        elif coordx == self.x:  # same
            self.dx = 0

        if coordy > self.y:     # down
            self.dy = 1
            self.direction = constants.ROT[0]
        elif coordy < self.y:   # up
            self.dy = -1
            self.direction = constants.ROT[1]
        elif coordy == self.y:  # same
            self.dy = 0


    def actionToPerform(self, path, dx, dy):
        if not path:
            print("Something went wrong with computing a path.")
            self.unable = True
        elif len(path) >= self.getBattery():
            print("Insufficient battery to perform a task.")
        else:
            print("Move to nearest available coordinates: ({}, {})".format(dx, dy))
            self.path = path
            self.movingTo = True
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
        if self.isBuilding():
            self.myWorldMap[(self.x + self.dx), (self.y + self.dy)] = 'b'
        elif self.isWall():
            self.myWorldMap[(self.x + self.dx), (self.y + self.dy)]  = 'w'
        elif self.hasObstacle():
            self.myWorldMap[(self.x + self.dx), (self.y + self.dy)]  = 'o'
        elif self.isHeadQuarters():
            self.myWorldMap[(self.x + self.dx), (self.y + self.dy)]  = 'h'
        else:
            self.myWorldMap[(self.x + self.dx), (self.y + self.dy)] = 'p'

        #print(self.myWorldMap.T)

    def beliefs(self):
        pass

    def plans(self):
        pass


    # ----------------------------- #
    # ----- Auxiliary Methods ----- #
    # ----------------------------- #

    def aheadPosition(self):
        self.dx = 0
        self.dy = 0
        #Deal with agents direction/orientation to where agent should move to
        if self.direction == constants.ROT[0]:
            self.dy = -1
        elif self.direction == constants.ROT[1]:
            self.dy = 1
        elif self.direction == constants.ROT[2]:
            self.dx = -1
        elif self.direction == constants.ROT[3]:
            self.dx = 1

    def updateAgent(self, idDelivery=None):
        self.hasCargo = not self.hasCargo
        self.idDelivery = idDelivery

        print("-> {}-{} updated: hasCargo={}, idDelivery={}".format(self.name, self.myCompany, self.hasCargo, self.idDelivery))

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
        print("-> {}-{} stoped. Battery level: {}".format(self.name, self.myCompany, self.battery))
        self.pause = not self.pause

    def prepareRecharge(self):
        print("-> {}-{} - prepare to recharge.".format(self.name, self.myCompany))
        self.move()
        self.rotate180()
        self.stopAgent()
        self.prepared = not self.prepared

    def recharge(self):
        print("-> {}-{} - recharge.".format(self.name, self.myCompany))
        self.battery = 100
        self.pause = not self.pause
        self.prepared = not self.prepared

    def checkTimeIteration(self):
        if self.count == 0:
            self.count = 10
            return True
        else:
            self.count -= 1
            return False

    def checkForPausesInDelivery(self):
        pause = 0
        if len(self.pausedDelivering) > 0:
            for p in self.pausedDelivering:
                if p.get('id_delivery') == self.idDelivery:
                    pause = pause + world.pauses[p.get('numPause') - 1] # get the pause from world.
            return pause
        return pause

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
        return self.battery == 0

    def isAgentInFront(self):
        return world.World.cellHasAgent(world.World, (self.x + self.dx), (self.y + self.dy))

    def isHeadQuarters(self):
        entity = world.World.getWorldObject(world.World, (self.x + self.dx), (self.y + self.dy)).__dict__
        if entity.get('type') == self.myCompany:
            #self.battery+=10
            return True
        else:
            return False
