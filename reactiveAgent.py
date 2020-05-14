import pygame
import sys, os, random
import constants


class reactiveAgent(pygame.sprite.Sprite):
    def __init__(self, world_map, surface):
        super().__init__()
        self.x = -1
        self.y = -1
        self.map = world_map
        self.direction = constants.DOWN
        self.rot = 0  # point down

        for col, tiles in enumerate(self.map):
            for row, tile in enumerate(tiles):
                if tile == 'a':
                    self.x = row
                    self.y = col
                    print("player at: row: {}, col: {}".format(row, col))
            # ---------------------------------------------
        filepath = os.path.join("data", "img", "dog02.png")
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.BLOCK_WIDTH, self.y * constants.BLOCK_HEIGHT)


    #------------------------#
    #        ACTUATORS       #
    #------------------------#
    def move(self, dx=0, dy=0, walls=None, buildings=None, deliveries=None, cells=None):
        #print(self.direction)
        if self.direction == constants.ROT[0]:
            dy = 1
        elif self.direction == constants.ROT[1]:
            dy = -1
        elif self.direction == constants.ROT[2]:
            dx = 1
        elif self.direction == constants.ROT[3]:
            dx = -1

        #if not a wall or building, keep moving
        #self.hasObstacle(dx, dy, cells)
        if not self.isWall(dx, dy, walls) and not self.isBuilding(dx, dy, buildings) and not self.hasObstacle(dx, dy, cells):
            self.x += dx
            self.y += dy
            self.rect = self.rect.move(dx * constants.BLOCK_WIDTH, dy * constants.BLOCK_HEIGHT)
            print("Player has moved. x,y: {},{}. dx={}, dy={}".format(self.x, self.y, dx, dy))

        #if its a building will check for delivery
        elif self.isBuilding(dx, dy, buildings):
            b_keys = buildings.__dict__.keys()
            pos = buildings.getPos(self.x+dx, self.y+dy, buildings)

            #cgeck for delivery
            if(self.hasDelivery(pos, buildings)):
                print("has delivery")
            else:
                #print("no delivery")
                pass

        #rotate otherwise
        elif self.hasObstacle(dx, dy, cells):
            print("desvia")
            self.rotate()

    def rotate(self):
        new_rot = random.randint(0, 3)
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
            self.direction == constants.ROT[2] and new_rot == 0  or self.direction == constants.ROT[3] and new_rot == 1:
            rot_angle = -90
            self.direction = constants.ROT[new_rot]

        self.image = pygame.transform.rotate(self.image, rot_angle)

    def pickUpDelivery(self):
        pass

    def dropDelivery(self):
        pass


    #------------------------#
    #         SENSORS        #
    #------------------------#

    def isWall(self, dx=0, dy=0, walls=None):
        for wall in walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def isBuilding(self, dx=0, dy=0, buildings=None):
        for b in buildings:
            if b.x == self.x + dx and b.y == self.y + dy:
                return True
        return False

    def hasDelivery(self, pos, buildings):
        current = buildings.__getitem__(pos)
        keys = current.__dict__
        if keys.get('delivery') == True:
            print("has delivery")
            return True
        else:
            return False

    def hasObstacle(self, dx, dy, cells):
        pos = cells.getPos(self.x, self.y, cells)
        current = cells.__getitem__(pos)
        keys = current.__dict__
        #print(keys)
        if keys.get('obstacle') == True:
            print("obstacle ahead")
            return True
        else:
            return False