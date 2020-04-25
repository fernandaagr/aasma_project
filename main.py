import pygame
import sys, os, random
import constants
from world import World

def main():
    myWorld = World()
    myWorld.updateClasses()

    while True:
        clock = pygame.time.Clock()     # Setup the clock for a decent framerate
        pygame.display.flip()           # Flip everything to the display
        clock.tick(5)                   # Ensure program maintains a rate of n frames per second

        myWorld.handleEvents()
        myWorld.drawAgents()
        pygame.display.update()

        if myWorld.start == True:
            myWorld.agentMove()


if __name__ == "__main__":
    main()