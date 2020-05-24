import pygame
import constants
import WorldObject
import world, utils

class Walls:
    """
    Set walls based on .txt with map. Always the same.
    """
    def __init__(self, world_map, surface):
        super().__init__()
        self.walls = []

        for col, tiles in enumerate(world_map):
            for row, tile in enumerate(tiles):
                if tile == 'w':
                    w = type('obj', (object,), {'x': row, 'y': col})
                    self.walls.append(w)

                    e = WorldObject.WorldObject(row, col, 'wall', False, False, False, None, '')

                    world.objects[row][col] = e
                    utils.setRect(row, col, surface, constants.BLACK)

    def __getitem__(self, item):
        return self.walls[item]

