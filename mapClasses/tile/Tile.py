class Tile:

    def __init__(self,reader_name, x, y, mirror=False):
        self.reader_name = reader_name
        self.x = x
        self.y = y
        self.mirror = mirror

    def __eq__(self, other):
        return other is not None \
               and self.x == other.x \
               and self.y == other.y \
               and self.reader_name == other.reader_name \
               and self.mirror == other.mirror

    def __str__(self):
        return "Tile: " + ', '.join("%s=%s" % item for item in vars(self).items())

    def __hash__(self):
        return hash(str(self))
