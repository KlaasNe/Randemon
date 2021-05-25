class Layer:

    def __init__(self):
        self.tiles = dict()

    def get_tile(self, x, y):
        return self.tiles.get((x, y), None)

    def set_tile(self, x, y, tile_name):
        self.tiles[(x, y)] = tile_name

    def has_tiles_in_area(self, x1, y1, x2, y2):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if self.get_tile(x, y) is not None:
                    return True
        return False
