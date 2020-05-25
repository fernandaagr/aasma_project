import pygame
import sys, random, time
import numpy as np
from reactiveAgent import reactiveAgent
import constants, Cells, Walls, Buildings, Deliveries
import utils
from CompanyAgent import CompanyAgent
import numpy as np

objects = np.empty([constants.NUMBER_OF_BLOCKS_WIDE, constants.NUMBER_OF_BLOCKS_HIGH], dtype=object)
agents = np.zeros([constants.NUMBER_OF_BLOCKS_WIDE, constants.NUMBER_OF_BLOCKS_HIGH], dtype=bool)
deliveries = []
tic = 0
pauses = []


class World:
    """
    Init world.
    """
    com = None
    numDeliveries = 0

    def __init__(self):
        self.start = False
        self.paused = True
        # ---------- Init Interface ---------- #
        pygame.init()
        pygame.display.set_caption("Delivery World")
        self.all_sprites = pygame.sprite.Group()
        self.display_surface = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.display_surface.fill(constants.LIGHTBLUE)

        # self.map = self.readMap(constants.MAPS[random.randint(0, 2)])
        self.map = utils.readMap(constants.MAPFILE)

        # ---------- Init world and objects ---------- #
        # cells, walls, buildings, obstacles and agents position come from map_delivery.txt
        self.cells = Cells.Cells(self.map, self.display_surface)
        self.walls = Walls.Walls(self.map, self.display_surface)
        self.buildings = Buildings.Buildings(self.map, self.display_surface)

        self.pTime = 0
        self.lastP = 0
        self.first = True
        self.startT = 0
        self.stop = 0
        self.numDeliveries = 0
        self.finalTime = 0
        self.pauses = []
        self.numPauses = 0
        # --------------------------------------------------- #
        # colocar um timer para gerar as deliveries
        self.deliveries = []
        print(" ---------- Deliveries ---------- ")

        self.generateNDeliveries(8)

        print(" ------------------------------ ")
        print("num deliveries: ", self.numDeliveries)
        World.numDeliveries = self.numDeliveries

        # isso tbm vai mudar, vai criar os agentes de acordo com a quantidade de cells da company
        # self.agent01 = reactiveAgent(0, 1, 1, 'cp1', self.display_surface, "A1")
        # self.agent02 = reactiveAgent(0, 1, 2, 'cp1', self.display_surface, "A2")

        # ------------------------------------------------- #
        """
        Testes class CompanyAgent
        1)uncomment da linha 73 até 79; 108 até 118; 194 até 204; 237, 238; 292 até 294.
        2)comment: 63, 64; 98 até 106 até 214; 240, 241; 295, 296, 311, 312;  248, 249
        3)main: comment 36 e 37
        """
        cp2 = self.cells.__dict__.get('cp2')
        keys = cp2[0].__dict__
        cp_x = keys.get('x')
        cp_y = keys.get('y')
        cp_name = keys.get('name')
        World.com = CompanyAgent(cp_x, cp_y, cp_name, 2, self.display_surface)

        self.drawGrid()

    # ----------------------------- #
    # ----- Auxiliary Methods ----- #
    # ----------------------------- #
    """
        Methods to help access/manipulate matrix with world objects
    """

    # depois mudar isto. Quando o "jogo" começar esperar o user clicar para iniciar.

    def reactiveAgentDecision(self):
        """
        Agent movement on game loop.
        Based on a random prop will rotate even if does not colide with anything.
        """
        r = random.random()

        # if r <= 0.8:
        #     self.agent02.agentDecision()
        # elif not self.agent02.pause:
        #     self.agent02.rotate()
        #
        # if r <= 0.8:
        #     self.agent01.agentDecision()
        # elif not self.agent01.pause:
        #     self.agent01.rotate()

        agent01 = World.com.__dict__.get('agents')[0]
        agent02 = World.com.__dict__.get('agents')[1]
        if r <= 0.8:
           agent02.agentDecision()
        elif not agent02.pause:
            agent02.rotate()

        if r <= 0.8:
          agent01.agentDecision()
        elif not agent01.pause:
           agent01.rotate()

    def askCompanyWhatToDo(self, agentId):
        print("Contacting company...")
        return World.com.whatToDo(agentId)

    def generateNDeliveries(self, num):
        """Generate and perform necessary updates."""
        for i in range(0, num):
            print("Delivery {})".format(i))
            d = Deliveries.Deliveries(self.buildings, self.display_surface)  # get new delivery
            setattr(d.__dict__.get('deliveries')[0], 'id_delivery', i)       # add id to it

            # get delivery keys and values
            delivery = d.__dict__.get('deliveries')[0].__dict__
            x = delivery.get('x')
            y = delivery.get('y')
            pos = delivery.get('pos')

            # update buildings with delivery and id of delivery -->objects
            self.updateWorldObject(x, y, 'delivery', True)
            self.updateWorldObject(x, y, 'info', delivery.get('id_delivery'))

            # auxiliary list with deliveries
            dd = type('obj', (object,),
                      {'pos': pos, 'x': x, 'y': y, 'dp_x': delivery.get('dp_x'), 'dp_y': delivery.get('dp_y'),
                       'id': delivery.get('id_delivery'), 'finished': False, 'agent': None})
            deliveries.append(dd)
            self.deliveries.append(dd)
            self.numDeliveries += 1

    # -------- Get Methods -------- #
    def getWorldObject(self, x, y):
        """
        Return world object given coordinates.
        """
        return objects[x][y];

    def getFinalTime(self):
        """
        Get final time of execution. Paused time not included.
        :return: finalTime
        """
        return self.stop - self.pTime - self.startT

    def getDeliveriesTime(self, agent):
        print("# ---------------------------------------- #")
        print("-> {}-{}:".format(agent.name, agent.myCompany))
        total = 0
        if len(agent.dMade) > 0:
            for i,d in enumerate(agent.dMade):
                print("{}) id: {} | Time: {}.".format(i+1, d.get('id'), round(d.get('time'), 2)))
                total += d.get('time')
            print("Total: {}".format(round(total, 2)))
            print("Average: {}".format(round(total/len(agent.dMade), 2)))
        else:
            print("No deliveries made.")

    def getPausedTime(self):
        """
        Return pausedTime.
        """
        pausedTime = 0
        for p in self.pauses:
            pausedTime = pausedTime + p
        return pausedTime

    # ------- Update Methods ------- #
    def updateWorldObject(self, x, y, attr, value):
        """
        Update specif world object.
        :param x: and :param y: coordinated of the object in the matrix.
        :param attr: attribute to be updated
        :param value: new value
        """
        setattr(objects[x][y], attr, value)

    def updateAgentLocation(self, x, y, value):
        """
        Update specif world object.
        :param x: and :param y: coordinated of the agent in the matrix.
        :param value: new value
        """
        agents[x][y] = value

    def updateDelivery(self, p, attr, value):
        """
        Update delivery when its picked up or droped.
        :param p: list  of deliveries
        :param attr: attribute to be updated
        :param value: new value
        """
        setattr(deliveries[p], attr, value)
        if attr == 'finished' and value == True:
            World.numDeliveries-=1

    def updateBuilding(self, x, y):
        """
        Update building after delivery is picked.
        """
        setattr(objects[x][y], 'delivery', not objects[x][y].__dict__.get('delivery'))

    def updateClasses(self):
        """
        Update sprites of interface.
        """
        for elem in self.cells:
            self.all_sprites.add(elem)

        for elem in self.cells.__dict__.get('cp1'):
            self.all_sprites.add(elem)

        for elem in self.cells.__dict__.get('cp2'):
            print(elem.__dict__)
            self.all_sprites.add(elem)

        for elem in self.cells.__dict__.get('obstacles'):
            self.all_sprites.add(elem)

        for elem in World.com.__dict__.get('agents'):
           self.all_sprites.add(elem)

        # self.all_sprites.add(self.agent01)
        # self.all_sprites.add(self.agent02)

    def othersUpdates(self):
        """
        Updated in the world.
        """
        # update buildings in case the delivery is finished -> give error if i try to update calling the method in reactiveAgent
        for d in deliveries:
            if d.__dict__.get('finished'):
                setattr(self.buildings.__getitem__(d.__dict__.get('pos')), 'delivery',
                        not self.buildings.__getitem__(d.__dict__.get('pos')).__dict__.get('delivery'))

    # ------- Check Methods ------- #
    def cellHasAgent(self, x, y):
        """
        Return agent given coordinates.
        """
        return agents[x][y];

    def checkEnd(self):
        """
        Not used yet. And doesnt work.
        :return:
        """
        if World.numDeliveries == 0:
            self.stop = time.perf_counter()
            self.finalTime = self.getFinalTime()
            print("Done!")
            return True
        else:
            return False

    def checkForCargoInAgent(self, agent, numPause):
        if agent.hasCargo:
            agent.pausedDelivering.append({
                'id_delivery': agent.idDelivery,
                'numPause': numPause})  # append o número da pause, para usar como index quando fizer o get do time dessa pause

    # ---- Help with the World ---- #
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
                    print("# ---------- QUIT ---------- #")
                    self.stop = time.perf_counter()
                    print("Time execution: {}".format(self.getFinalTime()))
                    print("Time paused: {}".format(self.getPausedTime()))
                    print("Deliveries so far:")
                    # self.getDeliveriesTime(self.agent01)
                    # self.getDeliveriesTime(self.agent02)
                    print("# --------------------------  #")
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:     # SPACE to start/stop agent
                    self.paused = not self.paused

                    # -- Calculate paused time -- #
                    # tentar mudar depois,  too messy
                    global pausedTime
                    if self.paused:
                        global tic
                        tic = time.perf_counter()
                        self.numPauses+=1
                        # when pause check if the agents has any delivery, so they wont return a higher time
                        # self.checkForCargoInAgent(self.agent01, self.numPauses)
                        # self.checkForCargoInAgent(self.agent02, self.numPauses)
                    elif not self.paused and self.first:
                        # do this to start the timer after the user press space for the first time
                        self.lastP = 0
                        self.pTime += self.lastP
                        # pausedTime += self.lastP
                        self.first = False
                        self.startT = time.perf_counter() # quando iniciar pela primeira vez
                    elif not self.paused and not self.first:
                        # when pause other times
                        self.lastP = time.perf_counter() - tic
                        self.pTime += self.lastP
                        self.pauses.append(self.lastP)
                        pauses.append(self.lastP)
                    # --------------------------- #
                    self.start = True

    def drawGrid(self):
        """
        Draw grid to better see movement and map.
        """
        for i in range(constants.NUMBER_OF_BLOCKS_WIDE):
            new_height = round(i * constants.BLOCK_HEIGHT)
            new_width = round(i * constants.BLOCK_WIDTH)
            pygame.draw.line(self.display_surface, constants.LIGHTGREY, (0, new_height), (constants.SCREEN_WIDTH, new_height), 2)
            pygame.draw.line(self.display_surface, constants.LIGHTGREY, (new_width, 0), (new_width, constants.SCREEN_HEIGHT), 2)

    def drawAgents(self):
        self.all_sprites.update()
        self.all_sprites.draw(self.display_surface)

