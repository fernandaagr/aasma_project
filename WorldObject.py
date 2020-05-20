class WorldObject:
    def __init__(self, x, y, type, obs=None, delivery=None, info=None):
        #self.pos = pos
        self.x = x
        self.y = y
        self.type = type
        self.delivery = delivery
        self.obs = obs
        self.info = info


    def objectEntity(self):
        return type('obj', (object,), {'pos': self.pos, 'x': self.x, 'y': self.y, 'type': type, 'info': self.info})

    def printEntity(self):
        print("Entity info: pos={}, coods=({}, {}), type={}.".format(self.pos, self.x, self.y, self.type))