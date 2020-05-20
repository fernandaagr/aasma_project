import os
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

NUMBER_OF_BLOCKS_WIDE = 12
NUMBER_OF_BLOCKS_HIGH = 12
BLOCK_HEIGHT = round(SCREEN_HEIGHT/NUMBER_OF_BLOCKS_HIGH)
BLOCK_WIDTH = round(SCREEN_WIDTH/NUMBER_OF_BLOCKS_WIDE)

LIGHTBLUE = (170, 170, 255)
BLACK = (0, 0, 0)
DARKGREY = (150, 150, 150)
LIGHTGREY = (211, 211, 211)
SILVER = (192,192,192)
DARKSLATEGRAY = (47,79,79)
DIMGRAY = (105,105,105)
SLATEGRAY = (112,128,144)
LIGHTSALMON = (255,160,122)
MAROON = (185,122,87)
GRAY = (128,128,128) # cp1
LIGHTLATEGREY = (119,136,153) # cp2


DOWN = "d"
LEFT = "l"
RIGHT = "r"
UP = "u"
ROT = {0: DOWN, 1: UP, 2: LEFT, 3: RIGHT}


#MAPFILE = "map.txt"
MP1 = os.path.join("data","maps","map_delivery.txt")
MP2 = os.path.join("data","maps","map_delivery2.txt")
MP3 = os.path.join("data","maps","map_delivery3.txt")

MAPS = {0: MP1, 1: MP2, 2: MP3}
MAPFILE = os.path.join("data","maps","map_delivery2.txt")
TITLE = "Welcome to Tile World!"