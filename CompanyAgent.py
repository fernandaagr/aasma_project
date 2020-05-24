import pygame, random, time
import constants
import world, utils
import numpy as np
from BasicAgent import BasicAgent
import math
import collections


class CompanyAgent:

    def __init__(self, x, y, company, numCells, surface):
        super().__init__()
        self.x = x
        self.y = y
        self.surface = surface
        self.name = company
        self.numCells = numCells
        self.agents = []
        # for testing, remove later
        self.marked = np.zeros([constants.NUMBER_OF_BLOCKS_WIDE-2, constants.NUMBER_OF_BLOCKS_HIGH-2], dtype=int)

        self.createAgents(self.numCells)
        print("Company {} starts in (x: {}, y:{}) and ends in (x: {}, y:{}).".format(self.name, self.x, self.y, self.x, self.y+1))
        for i,a in enumerate(self.agents):
            print("-> [{}] ".format(a.__dict__.get('name')))

    def createAgents(self, numCells):
        x = self.x
        y = self.y
        for i in range(0, numCells):
            num = i+1
            agentName = str("A"+str(num)+"-"+self.name+"")
            agent = BasicAgent(x, y, self.name, self.surface, agentName, num)
            self.agents.append(agent)
            y+=1

    def whatToDo(self, agentId):
        battery = 0
        hasCargo = False
        x = 0
        y = 0
        print("Agent with id {} want to know what to do!".format(agentId))
        for agent in self.agents:
            if agentId == agent.__dict__.get('myId'):
                battery = agent.__dict__.get('battery')
                hasCargo = agent.__dict__.get('hasCargo')
                x = agent.__dict__.get('x')
                y = agent.__dict__.get('y')

        print("Agent pos: x: {}, y:{}.".format(x, y))
        if battery <= 25 and hasCargo:
            print("if battery and cargo")
            # get id and delivery info
            idDelivery = agent.__dict__.get('idDelivery')  # BUG - as vezes retorna id None, mesmo possuindo o id
            deliveryInfo = world.deliveries[idDelivery].__dict__
            print("Delivery info: {}.".format(deliveryInfo))
            dx = deliveryInfo.get('dp_x')
            dy = deliveryInfo.get('dp_y')
            # compute distances
            coordsPossible = [(self.x, self.y), (self.x, self.y + 1), (dx, dy)]
            listDistances = [self.distanceTo(x, y, self.x, self.y), self.distanceTo(x, y, self.x, self.y + 1),
                             self.distanceTo(x, y, dx, dy)]
            indexCoord = listDistances.index(min(listDistances))
            (new_dx, new_dy) = coordsPossible.pop(indexCoord)
            print("Distances: {}".format(listDistances))
            print("Min distance: {}. | Coordinates: ({}, {}).".format(listDistances[indexCoord], new_dx,
                                                                      new_dy))  # will be used to apply floodFill
            # apply bfs to get path
            path = self.bfs_map((x, y), (new_dx, new_dy))
            print(path)
            # if len(path) >= battery:
            #    print("Insufficient battery to perform task.")
            # else:
            #    print("Move to nearest available coordinates.{}, {}".format(new_dx, new_dy))

        elif battery <= 25 and not hasCargo:
            print("if battery and no cargo")
            # compute distances
            coordsPossible = [(self.x, self.y), (self.x, self.y + 1)]
            listDistances = [self.distanceTo(x, y, self.x, self.y), self.distanceTo(x, y, self.x, self.y + 1)]
            indexCoord = listDistances.index(min(listDistances))
            (new_dx, new_dy) = coordsPossible.pop(indexCoord)
            print("Distances: {}".format(listDistances))
            print("Min distance: {}. | Coordinates: ({}, {}).".format(listDistances[indexCoord], new_dx,
                                                                      new_dy))  # will be used to apply floodFill
            # apply bfs to get path
            path = self.bfs_map((x, y), (new_dx, new_dy))
            print(path)
            # if len(path) >= battery:
            #    print("Insufficient battery to perform task.")
            # else:
            #    print("Move to nearest available coordinates.{}, {}".format(new_dx, new_dy))


    def bfs_map(self, o, d):
        """
        Compute path from origin to destination according with agents map.
        :param o: origin coordinates.
        :param d: destination coordinates.
        :return: path from o to d (list with coordinates).
        """
        queue = collections.deque([[o]])
        seen = set([o])
        xd, yd = d
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if x == xd and y == yd:
                return path
            positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]  # right, left, up, down
            for x2, y2 in positions:
                cellInfo = world.World.getWorldObject(world.World, x2, y2).__dict__
                types = cellInfo.get('type')
                obs = cellInfo.get('obs')
                building, wall = 'building', 'wall'

                if 0 <= x2 < constants.NUMBER_OF_BLOCKS_WIDE-1 and 0 <= y2 < constants.NUMBER_OF_BLOCKS_HIGH-1 and \
                        types != building and not obs and types != wall and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))

    def floodFill(self, ox, oy, dx, dy):
        """
        Receive origin and destination coords and "fill" the map to return all coord that the agent can access to move.
        """
        q = []
        q.append((ox, oy))
        points = []

        update = False
        # este update deve ser feito no mapa do agente
        world.World.updateWorldObject(world.World, ox, oy, 'marked', 0)  # mark origin with 0
        world.World.updateWorldObject(world.World, ox, oy, 'visited', True)
        self.marked[ox-1][oy-1] = 0 # não é necessário, só para testes. Remover depois
        points.append({'x': ox, 'y': oy})
        mark = 1
        while len(q) > 0:
            (x, y) = q.pop()

            if x == dx and y == dy: # if coods of destination return points so far
                print("Destiny: (x: {}, y: {})".format(dx, dy))
                return points
            if ox < 1 or oy < 1 or ox > 10 or oy > 10: # check limits
                print("No more points to move to.")
                return points

            if self.checkIfItsFree(x+1, y):  # right cell
                update = True
                q.append((x+1, y))
                self.updateMark(x+1, y, mark)
                points.append({'x': x+1, 'y': y})
            if self.checkIfItsFree(x-1, y):  # left cell
                update = True
                q.append((x-1, y))
                self.updateMark(x-1, y, mark)
                points.append({'x': x-1, 'y': y})
            if self.checkIfItsFree(x, y+1):  # down cell
                update = True
                q.append((x, y+1))
                self.updateMark(x, y+1, mark)
                points.append({'x': x, 'y': y+1})
            if self.checkIfItsFree(x, y-1):  # upper cell
                update = True
                q.append((x, y-1))
                self.updateMark(x, y-1, mark)
                points.append({'x': x, 'y': y-1})

            if update:
                mark+=1
                update = False

        return points

    def checkSurroundings(self, x, y):
        positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]  # right, left, up, down
        for px, py in positions:
            
        pass

    def updateMark(self, x, y, mark):
        """Update marks from filled cells."""
        world.World.updateWorldObject(world.World, x, y, 'marked', mark)  # mark origin with 0
        self.marked[x-1][y-1] = mark

    def checkIfItsFree(self, x, y):
        """
        Check if position received is free, unmarked and "unvisited" to the agent move.
        """
        object = world.World.getWorldObject(world.World, x, y).__dict__  # -> mudar para mapa do agente
        return object.get('isFree') and object.get('marked') is None and not object.get('visited')

    def distanceTo(self, ox, oy, dx, dy):
        """Compute Euclidian distance between two points."""
        return math.sqrt((dx - ox)**2 + (dy - oy)**2)


