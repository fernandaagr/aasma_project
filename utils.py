import constants, os, pygame
def readMap(mapfile):
    """
    Read .txt file with map.
    :param mapfile: path to file
    :return:
    """
    with open(mapfile, 'r') as f:
        world_map = f.readlines()
    world_map = [line.strip() for line in world_map]
    return world_map


def setImage(x, y, name):
    filepath = os.path.join("data", "img", name+".png")
    image = pygame.image.load(filepath).convert_alpha()
    image = pygame.transform.scale(image, (constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT))
    rect = image.get_rect()
    rect = rect.move(x * constants.BLOCK_WIDTH, y * constants.BLOCK_HEIGHT)

    return image, rect


def setRect(x, y, surface, color):
    myrect = pygame.Rect(x * constants.BLOCK_WIDTH+2, y * constants.BLOCK_HEIGHT+1,
                         constants.BLOCK_WIDTH, constants.BLOCK_HEIGHT)
    pygame.draw.rect(surface, color, myrect)
