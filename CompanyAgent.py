import pygame, random, time
import constants
import world, utils
import numpy as np
from BasicAgent import BasicAgent
from reactiveAgent import reactiveAgent
from ProactiveAgent import ProactiveAgent
import math
import collections


class CompanyAgent:
    def __init__(self, x, y, company, numCells, surface, rot):
        super().__init__()
        self.x = x
        self.y = y
        self.surface = surface
        self.name = company
        self.numCells = numCells
        self.agents = []
        self.rot = rot

        self.createAgents(self.numCells)
        # print("Company {} starts in (x: {}, y:{}) and ends in (x: {}, y:{}).".format(self.name, self.x, self.y, self.x, self.y+1))
        # for i,a in enumerate(self.agents):
        #     print("-> [{}] ".format(a.__dict__.get('name')))

    def createAgents(self, numCells):
        x = self.x
        y = self.y
        agentName1 = str("A" + str(1) + "-" + self.name + "")
        agent1 = reactiveAgent(x, y, self.name, self.surface, agentName1, 1, self.rot)
        agentName2 = str("A" + str(2) + "-" + self.name + "")
        agent2 = ProactiveAgent(x, y+1, self.name, self.surface, agentName2, 2, self.rot)
        self.agents.append(agent1)
        self.agents.append(agent2)
        # for i in range(0, numCells):
        #     num = i+1
        #     agentName = str("A"+str(num)+"-"+self.name+"")
        #     agent = BasicAgent(x, y, self.name, self.surface, agentName, num)
        #     self.agents.append(agent)
        #     y+=1

    def whatToDo(self, agentId):
        battery = 0
        hasCargo = False
        x = 0
        y = 0
        currentAgent = self.agents[agentId-1].__dict__
        battery = currentAgent.get('battery')
        hasCargo = currentAgent.get('hasCargo')
        x = currentAgent.get('x')
        y = currentAgent.get('y')
        agentMap = currentAgent.get('myWorldMap')

        print("Agent pos: ({}, {}).".format(x, y))
        if battery <= 25 and hasCargo:
            print("Agent has low battery and its carrying a delivery.")
            # get id and delivery info
            idDelivery = currentAgent.get('idDelivery')
            deliveryInfo = world.deliveries[idDelivery].__dict__
            dx = deliveryInfo.get('dp_x')
            dy = deliveryInfo.get('dp_y')
            print("Has delivery to drop in: ({}, {}). Id={}.".format(dx, dy, deliveryInfo.get('id')))
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
            path = self.bfs_map(agentMap, (x, y), (new_dx, new_dy))
            print(path)
            return path, new_dx, new_dy

        elif battery <= 25 and not hasCargo:
            print("Agent has low battery and none delivery.")
            # compute distances
            coordsPossible = [(self.x, self.y), (self.x, self.y + 1)]
            listDistances = [self.distanceTo(x, y, self.x, self.y), self.distanceTo(x, y, self.x, self.y + 1)]
            indexCoord = listDistances.index(min(listDistances))
            (new_dx, new_dy) = coordsPossible.pop(indexCoord)
            print("Distances: {}".format(listDistances))
            print("Min distance: {}. | Coordinates: ({}, {}).".format(listDistances[indexCoord], new_dx,
                                                                      new_dy))  # will be used to apply floodFill
            # apply bfs to get path
            path = self.bfs_map(agentMap, (x, y), (new_dx, new_dy))
            print(path)
            return path, new_dx, new_dy

    def bfs_map(self, agentMap, o, d):
        """
        Compute path from origin to destination according with agents map.
        :param o: origin coordinates.
        :param d: destination coordinates.
        :return: path from o to d (list with coordinates).
        """
        queue = collections.deque([[o]])
        seen = set([o])
        xd, yd = d
        # building, wall, obs, cp, clear, unknown = 'b', 'w', 'o', 'h', '.', '-'
        building, wall, obs, cp, clear, unknown = 'building', 'wall', 'obs', 'h', '.', '-'
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if x == xd and y == yd:
                return path
            positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]  # right, left, up, down
            for x2, y2 in positions:
                tp = world.World.getWorldObject(world.World, x2, y2).__dict__.get('type')
                # if 0 <= x2 < constants.NUMBER_OF_BLOCKS_WIDE-1 and 0 <= y2 < constants.NUMBER_OF_BLOCKS_HIGH-1 and \
                #         agentMap[y2][x2] != building and agentMap[y2][x2] != wall and agentMap[x2][y2] != unknown and agentMap[y2][x2] != obs \
                #         and (x2, y2) not in seen:
                if 0 <= x2 < constants.NUMBER_OF_BLOCKS_WIDE - 1 and 0 <= y2 < constants.NUMBER_OF_BLOCKS_HIGH - 1 and \
                        tp != building and tp != wall and tp != obs and (x2, y2) not in seen:
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

    # ISSO VAI EM PROACTIVE AGENT, i think #
    def checkSurroundings(self, x, y):
        positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]  # right, left, up, down
        for px, py in positions:
            pass
            # get info about these positions (from agents map or not) to se what's arround.
            # If is a buildings never visited go there,
            # if agent has no cargo, check if he detected a delivery there previously,
            # if is headquarters, check battery to see if needs to recharge,
            # if there is an obstacle in one of the positions avoid,
            # if are free cells move randmoly

        return "Best Action"
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


