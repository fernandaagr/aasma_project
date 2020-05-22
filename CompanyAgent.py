import pygame, random, time
import constants
import world, utils
import numpy as np
from BasicAgent import BasicAgent


class CompanyAgent:
    def __init__(self, x, y, company, numCells, surface):
        super().__init__()
        self.x = x
        self.y = y
        self.surface = surface
        self.name = company
        self.numCells = numCells
        self.agents = []

        self.createAgents(self.numCells)
        print("Company {} starts in (x: {}, y:{}) and ends in (x: {}, y:{}).".format(self.name, self.x, self.y, self.x, self.y+1))
        print(self.agents[0].__dict__)
        agentName01 = self.agents[0].__dict__.get('name')
        agentName02 = self.agents[1].__dict__.get('name')
        print("Has {} agents: [{}] and [{}].".format(self.numCells, agentName01, agentName02))

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
        print("what do I do?")
        print("id {} want to know what to do!".format(agentId))

        for agent in self.agents:
            if agentId == agent.__dict__.get('myId'):
                print("Agent info: ", agent.__dict__)


"""
*vai pegar as informações do agent e decide o q fazer. Pega battery, hasCargo para avaliar a decisão.
        
*battery: calcula a distancia para o headQuarters, se a bateria for insuficiente pede ajuda a um outro agent;
    distanceTo -> para calcular a distancia de um ponto para o outro;
    fazer o get das informações da delivery q o agent tem
           
*se o agent tiver uma delivery calcular a distancia para o drop point e ver se a bateria é suficiente ou se é melhor mandar para o headQuarters

*criar uma variavel boolean para o agent saber se está esperando decisão ou não;
    se estiver esperando continua parado
*
                
"""
