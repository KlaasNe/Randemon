class WeightTile:

    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.weight = weight
        self.visited = False
        self.prev = None

    def __str__(self):
        return "WeightTile: " + ', '.join("%s=%s" % item for item in vars(self).items())

    def get_pos(self):
        return self.x, self.y
