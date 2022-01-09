class Layer:

    def __init__(self):
        self.tiles = dict()

    def get_tile(self, x, y):
        return self.tiles.get((x, y), None)

    def set_tile(self, x, y, tile):
        self.tiles[(x, y)] = tile

    def get_ex_pos(self):
        return self.tiles.keys()

    def has_tiles_in_area(self, x1, y1, x2, y2):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if (x, y) in self.get_ex_pos():
                    return True
        return False

    def get_tile_type(self, x, y):
        try:
            return self.get_tile(x, y).get_type()
        except AttributeError:
            return None
