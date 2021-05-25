class Tile:

    def __init__(self, x, y, tile_name):
        self.x = x
        self.y = y
        self.tile_name = tile_name

    def __str__(self):
        return "tile: " + ', '.join("%s=%s" % item for item in vars(self).items())
