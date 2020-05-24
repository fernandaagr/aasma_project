import pygame
import sys, os, random
import constants
from world import World
import time
from datetime import datetime

def main():
    myWorld = World()
    myWorld.updateClasses()
    start = time.perf_counter()
    running = True

    #try:
    while running:
        clock = pygame.time.Clock()     # Setup the clock for a decent framerate
        pygame.display.flip()           # Flip everything to the display
        clock.tick(8)                   # Ensure program maintains a rate of n frames per second

        myWorld.handleEvents()
        myWorld.drawAgents()
        pygame.display.update()
        myWorld.othersUpdates()

        if myWorld.start:
            if myWorld.paused:
                pass
            elif not myWorld.paused:
                myWorld.reactiveAgentDecision()

        if myWorld.checkEnd():
            # antes disso tem de pedir aos agents para voltar para o headQuarters, ou não
            # running = False
            myWorld.paused = True
    # get time of deliveries ------> mudar para loop depois
    myWorld.getDeliveriesTime(myWorld.agent01)
    myWorld.getDeliveriesTime(myWorld.agent02)
    for i,a in enumerate(myWorld.com.__dict__.get('agents')[i]):
        myWorld.getDeliveriesTime(myWorld, a)

    print("Final execution time: {}.".format(round(myWorld.getFinalTime(), 2)))
    print("Paused time: {}.".format(round(myWorld.getPausedTime(), 2)))

    #except Exception as ex:
    #    stop = time.perf_counter()
    #    final = stop - start - myWorld.getPausedTime()
    #    print("# ------ Exception ------ #")
    #    print("Time: {}".format(final))
    #    print(ex)
    #    print("# ----------------------- #")
    #    sys.exit(1)


if __name__ == "__main__":
    main()